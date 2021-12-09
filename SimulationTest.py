from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
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

    def __init__(self, unique_id, model, agent, radius, position):
        super().__init__(unique_id, model)
        self.owner = agent
        (a, b) = position
        self.radius = radius
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
        self.value = 500
        self.owner = agent
        (a, b) = position
        self.position = (a, b)
        self.target_of = None
        self.model.grid.place_agent(self, (a, b))

    def be_moved(self, position):
        (new_a, new_b) = position
        self.model.grid.move_agent(self, (new_a, new_b))

    def set_is_target_of(self, agent):
        self.target_of = agent

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
        self.target = None # target for stealing
        self.risk_threshold = random.randint(0, 1000)
        self.goal = "WALK ROAD"
        self.goodies = []
        self.objects_seen = {}


    def set_vision(self, radius):
        self.vision = Vision(self.model.next_id(), self.model, self, radius, self.pos)

    def set_goodie(self, pos):
        self.goodie = Goodie(self.model.next_id(), self.model, self, pos)
        self.goodies.append(self.goodie)


    def pot_steal_object(self, object_fact):
        (class_name, obj, unique_id, step_, owner) = object_fact
        print(obj.type_, obj.value, owner, self.unique_id)
        if owner != self.unique_id: # potential steal
            # calculate stealing
            print("RISKY", obj.value, self.risk_threshold)
            if (obj.value*1) > self.risk_threshold:  # Probability of getting away with it is 1 :) interesting C/B calculation here
                self.goal = "STEAL"
                self.target = obj
                obj.set_is_target_of(self)
            else:
                print("TOO RISKY")
                self.goal = "GO HOME"




    def update_objects_in_vision(self, objects):
        list_objects = []
        for object in objects:
            print(type(object).__name__, object, object.unique_id, self.model.schedule.steps, object.owner)
            fact_tuple = (type(object).__name__, object, object.unique_id, self.model.schedule.steps, object.owner.unique_id)
            #print(fact_tuple)
            if type(object).__name__ == "Goodie":
                self.pot_steal_object(fact_tuple)
            list_objects.append(fact_tuple)

        self.objects_seen[self.model.schedule.steps] = list_objects
        # this means: this agent saw an object of TYPE, with number X, at time T, and with owner Y.

    def set_house_owner(self, house):
        self.owns_house = house

    def get_house(self):
        return self.owns_house

    def move_step_to_goal(self, goal):
        hx, hy = goal
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, include_center=False)
        bestx, besty = 100, 100
        best = 100
        for step in possible_steps:
            stepx, stepy = step
            if (hx - stepx) ** 2 + (hy - stepy) ** 2 < best:
                best = (hx - stepx) ** 2 + (hy - stepy) ** 2
                bestx, besty = stepx, stepy

        return bestx, besty


    def go_home(self):
        a_house = self.get_house()
        hx, hy = a_house.x, a_house.y
        bestx, besty = self.move_step_to_goal((hx, hy))
        if (bestx, besty) == (hx, hy):
            # we are home
            pass
        else:
            self.move_agent_and_attributes(bestx, besty)

    def move_agent_and_attributes(self, new_x, new_y):
        self.model.grid.move_agent(self, (new_x, new_y))
        self.vision.be_moved()
        for goodie in self.goodies:
            goodie.be_moved((new_x, new_y))

    def step(self):
        self.vision.step()
        goal = self.goal
        if goal == "GO HOME":
            if self.pos is not (self.get_house().x, self.get_house().y):
                self.go_home()
            else:
                pass
        elif goal == "WALK ROAD":
            (new_x, new_y) = self.move_step_to_goal((4, 4)) # TODO problem
            self.model.grid.move_agent(self, (new_x, new_y))
            self.vision.be_moved()

        elif goal == "STAY STILL":
            pass

        elif goal == "STEAL":
            # move to target and take it
            (new_x, new_y) = self.move_step_to_goal(self.target.position)
            self.model.grid.move_agent(self, (new_x, new_y))
            self.vision.be_moved()
            if self.pos == self.target.position:
                self.goodies.append(self.target)
                self.goal = "GO HOME"

        elif goal == "FLEE":
            (new_x, new_y) = self.move_step_to_goal((13, 4))
            self.move_agent_and_attributes(new_x, new_y)


class Walkway(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.width = self.model.grid.width
        self.height = 1
        self.x = 0
        self.y = 4
        self.owner = self


    def step(self):
        pass



class House(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.width = 5
        self.height = 3
        self.x = (unique_id*10 + 3)
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


class StolenLaptop(Model):

    def __init__(self, N_agents, N_houses, width, height):
        self.running = True
        self.current_id = -1
        self.num_agents = N_agents
        self.num_houses = N_houses
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.houses = []
        self.agents = []
        self.walkways = []

        '''
        I want a house that belongs to 1 agent,
        and another agent walking past
        '''
        for i in range(self.num_agents):
            a = House(self.next_id(), self)
            self.schedule.add(a)
            self.grid.place_agent(a, (a.x, a.y))
            self.houses.append(a)

        print(self.houses)

        road = Walkway(self.next_id(), self)
        self.schedule.add(road)
        self.grid.place_agent(road, (road.x, road.y))
        self.walkways.append(road)

        # house owner
        a = StreetAgent(self.next_id(), self)
        a.goal = "STAY STILL"
        self.schedule.add(a)
        x = self.grid.width - 1
        y = self.grid.height - 1
        self.grid.place_agent(a, (x, y))
        self.agents.append(a)
        self.houses[0 % 2].set_owner(a)
        a.set_vision(radius=0)
        a.set_goodie(pos=(a.owns_house.x, a.owns_house.y))

        # thief
        a = StreetAgent(self.next_id(), self)
        a.goal = "WALK ROAD"
        self.schedule.add(a)
        x = self.grid.width - 1
        y = road.y
        self.grid.place_agent(a, (x, y))
        self.agents.append(a)
        self.houses[1 % 2].set_owner(a)
        a.set_vision(radius=4)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()



class Street(Model):
    """A model with some number of agents."""
    def __init__(self, N_agents, N_houses, width, height):

        self.running = True
        self.current_id = -1
        self.num_agents = N_agents
        self.num_houses = N_houses
        self.grid = MultiGrid(width, height, torus=True)
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
            a.goal = "GO HOME"
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.agents.append(a)
            self.houses[i % 2].set_owner(a)
            a.set_vision(radius=4)
            a.set_goodie(pos=(x,y))

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
