from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np
import matplotlib.pyplot as plt


class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id
        self.move()
        if self.wealth > 0:
            self.give_money()



class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.running = True
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()


class Vision(Agent):

    def __init__(self, unique_id, model, agent, position):
        super().__init__(unique_id, model)
        self.owner = agent
        (a, b) = position
        self.radius = 4
        self.model.grid.place_agent(self, (a, b))

    def get_new_position(self):
        return self.owner.pos

    def be_moved(self):
        (new_a, new_b) = self.owner.pos[0], self.owner.pos[1]
        self.model.grid.move_agent(self, (new_a, new_b))


    def step(self):
        (new_a, new_b) = self.owner.pos[0], self.owner.pos[1]
        neighbors = self.model.grid.get_neighbors(pos=(new_a, new_b), moore=True, radius=self.radius)
        self.owner.update_objects_in_vision(neighbors)


class Goodie(Agent):
    def __init__(self, unique_id, model, agent, position):
        super().__init__(unique_id, model)
        self.type_ = "laptop"
        self.owner = agent
        (a, b) = position
        self.position = (a, b)
        self.model.grid.place_agent(self, (a, b))

    def be_moved(self):
        (new_a, new_b) = self.owner.pos[0], self.owner.pos[1]
        self.model.grid.move_agent(self, (new_a, new_b))

    def step(self):
        if self.position == (self.owner.get_house().x, self.owner.get_house().y):   # in house
            pass




class StreetAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.seen_goodie = 0
        self.owner = self
        self.owns_house = None
        self.seen_objects = None


    def set_vision(self):
        position = self.pos
        self.vision = Vision(self.model.next_id(), self.model, self, position)
        self.goodie = Goodie(self.model.next_id(), self.model, self, position)

    def update_objects_in_vision(self, objects):
        print("\t\t", self.unique_id)
        for object in objects:
            fact_tuple = (type(object).__name__, object.unique_id, self.model.schedule.steps, object.owner.unique_id)
            print(fact_tuple)
            # this means: this agent saw an object of TYPE, with number X, at time T, and with owner Y.
        pass

    def set_house_owner(self, house):
        self.owns_house = house

    def get_house(self):
        return self.owns_house

    def go_home(self):
        a_house = self.get_house()
        hx, hy = a_house.x, a_house.y
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, include_center=False)
        bestx, besty = 100, 100
        best = 100
        for step in possible_steps:
            stepx, stepy = step
            if (hx - stepx)**2 + (hy - stepy)**2 < best:
                best = (hx - stepx)**2 + (hy - stepy)**2
                bestx, besty = stepx, stepy

        if (bestx, besty) == (hx, hy):
            # we are home
            pass
        else:
            self.move_agent_and_attributes(bestx, besty)


    def move_agent_and_attributes(self, new_x, new_y):
        self.model.grid.move_agent(self, (new_x, new_y))
        self.vision.be_moved()
        self.goodie.be_moved()


    def step(self):
        self.vision.step()
        # The agent's step will go here.
        if self.pos is not (self.get_house().x, self.get_house().y):
            self.go_home()
        else:
            pass

        self.goodie.step()


class Walkway(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.width = self.model.grid.width
        self.height = 1
        self.x = 0
        self.y = 6
        self.owner = self


    def step(self):
        pass



class House(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.width = 5
        self.height = 3
        self.x = (unique_id*10 + 4)
        self.y = 2
        self.owner = None

    def set_owner(self, agent):
        house = self
        self.owner = agent
        agent.set_house_owner(house)

    def get_owner(self):
        return self.owner

    def step(self):
        pass



class Street(Model):
    """A model with some number of agents."""
    def __init__(self, N_agents, N_houses, width, height):

        self.running = True
        self.current_id = -1
        self.num_agents = N_agents
        self.num_houses = N_houses
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.houses = []
        self.agents = []
        self.walkways = []



        # Create agents
        for i in range(self.num_agents):
            a = House(self.next_id(), self)
            self.schedule.add(a)
            self.grid.place_agent(a, (a.x, a.y))
            self.houses.append(a)


        for i in range(self.num_houses):
            a = StreetAgent(self.next_id(), self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.agents.append(a)
            self.houses[i % 2].set_owner(a)
            a.set_vision()


        road = Walkway(self.next_id(), self)
        self.schedule.add(road)
        self.grid.place_agent(road, (road.x, road.y))
        self.walkways.append(road)

        a.vision.step()

        # make agents walk towards their own house




    def step(self):
        '''Advance the model by one step.'''

        self.schedule.step()




'''all_wealth = []
for j in range(100):
    m = MoneyModel(2, 20, 10)
    for i in range(20):
        m.step()

    for a in m.schedule.agents:
        all_wealth.append(a.wealth)
'''

'''
agent_counts = np.zeros((m.grid.width, m.grid.height))
for cell in m.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count
plt.imshow(agent_counts, interpolation='nearest')
plt.colorbar()
plt.show()

print(range(max(all_wealth)+1))
plt.hist(all_wealth, bins=range(max(all_wealth)+1))
plt.show()
'''
