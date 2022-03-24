from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace, HexGrid, MultiGrid
from SimulationClasses.StreetAgent import StreetAgent
import numpy as np
import csv
import random

class MoneyAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, goal_state, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.goal = goal_state
        self.thresholds = [random.random(), random.random(), random.random()]    # talk sing dance
        self.thresholds.sort()
        self.cooldown_time = random.randint(10, 15)
        self.state_timer = 10
        self.state = "HANG AROUND"
        self.position_list = []
        ### Personal details
        self.age = random.randrange(16, 95)
        self.name = self.pick_a_name()
        ### theft and property
        self.value_of_good = random.randrange(0, 1000)
        self.risk_threshold = random.randrange(500, 5000) # will steal if opportunity
        self.age_threshold = random.randrange(60, 100) # minimum age an agent will steal from
        self.steal_state = "N"
        self.target = None
        self.temp_goal = None
        self.ag_text = ":)"

    def pick_a_name(self):
        first_names = ["ursula", "neil", "ada", "naomi", "margaret",
                 "gerda", "nick", "china", "becky", "douglas",
                 "octavia", "jeff", "hella", "hilary", "aafke", "john",
                 "terry"]
        last_names = ["cornflower", "olive", "daisy", "tulip",
                      "violet", "goldenrod", "lemon", "orange",
                      "maroon", "plum"]

        name = random.choice(first_names) + " " + random.choice(last_names)
        return name

    def step(self):
        if self.pos == self.goal:
            self.state = "GOAL"
            self.steal_state = "DONE"
            self.value_of_good = -1
            self.ag_text = ""


        else:
            # check the neighbors for their values

            all_neighbors = self.model.grid.get_neighbors(pos=self.pos, moore=True,
                                                          radius=2)  # agents see around them with radius 3
            neighbors = []
            for i in all_neighbors:
                if self.model.extended_grid[i.pos] == "OPEN":
                    neighbors.append(i)


            # an agent will try to steal from a neighbor if the neighbor is old enough, if
            # the neighbor has valuable goods, and if the agent is not currently stealing from
            # someone else.
            for agent in neighbors:
                if agent.value_of_good > self.risk_threshold and \
                    agent.age > self.age_threshold and \
                        (self.steal_state == "N" or self.steal_state == "LOSER"):
                    self.steal_state = "MOTIVE"
                    self.target = agent
                    self.temp_goal = agent.pos
                    self.state = "FAST MOVE TO GOAL"

            if self.steal_state == "MOTIVE":
                self.state = "FAST MOVE TO GOAL"
                #print("I want to steal")
                if self.target.steal_state == "DONE":
                    self.target = None
                    self.steal_state = "N"

                if self.target.pos != self.pos:
                    self.steal_state = "SNEAK"
                else:
                    self.steal_state = "STEALING"

            if self.steal_state == "SNEAK":
                self.state = "FAST MOVE TO GOAL"
                #print("sneaking")
                if self.target is not None:
                    if self.target.steal_state == "DONE":
                        self.target = None
                        self.steal_state = "N"

                if self.target is not None:
                    if self.pos == self.target.pos:
                        #print("I'm in the same place as my target")
                        self.steal_state = "STEALING"

            if self.steal_state == "STEALING":
                self.state = "FAST MOVE TO GOAL"
                #print("stealing")
                if self.target is not None:
                    if self.target.steal_state == "DONE":
                        self.target = None
                        self.steal_state = "N"

                    if self.target is not None:
                        self.value_of_good += self.target.value_of_good
                        self.target.value_of_good = 0
                        self.target.steal_state = "LOSER"
                        self.steal_state = "N"

            '''if self.target is not None:
                print(self.steal_state, self.unique_id, self.target.unique_id, self.pos, self.temp_goal)
            else:
                print(self.steal_state, self.unique_id, None)'''







            # if they see that they're surrounded by other agents, they're more likely to hang out.
            # at every step, agents check if they're near other agents,
            # and want to hang around in a crowd if that's the case.
            #print(self.state)
            if self.state == "HANG AROUND":
                self.hang_around()
            elif self.state == "MOVE TO GOAL":
                self.move_to_goal(radius=1)
            elif self.state == "ESCAPE":
                self.hang_around()
            else:
                self.move_to_goal(radius=2)




            if self.state_timer > self.cooldown_time and self.state != "ESCAPE":
                self.state_timer = 0
                t = random.random()
                #print(t, self.thresholds[2])
                if t > self.thresholds[2]: # max speed
                    self.state = "FAST MOVE TO GOAL"

                elif t > self.thresholds[1]:
                    self.state = "MOVE TO GOAL"

                else:
                    self.state = "HANG AROUND"

                if len(neighbors) > 20:  # 20 agents nearby is a crowd.
                    t = random.random()
                    if t > 0.25:
                        self.state = "HANG AROUND"

            if self.state_timer > self.cooldown_time and self.state == "ESCAPE":
                t = random.randrange(0, 20)
                if t > 17:
                    self.state = "HANG AROUND"


        self.position_list.append(self.pos)

        self.state_timer += 1

        if self.state != "ESCAPE":
            if len(self.position_list) > 10:
                y = len(self.position_list)
                count_dict = {}
                #print(self.position_list[y-10: -1])
                for x in self.position_list[y-10: -1]:
                    if x not in count_dict.keys():
                        count_dict[x] = 0
                    else:
                        count_dict[x] += 1

                for key in count_dict.keys():
                    if count_dict[key] > 3:
                        self.state = "ESCAPE"
                        #print(self.unique_id, "ESCAPE")

        if self.steal_state == "LOSER":
            self.ag_text = ":("

        elif self.steal_state == "STEALING":
            self.ag_text = "..💰"

        elif self.steal_state == "MOTIVE":
            self.ag_text = "👀"

        elif self.steal_state == "SNEAK":
            self.ag_text = "🐆"

        elif self.steal_state == "N":
            self.ag_text = ":)"


    def move(self):
        radius = 1
        if self.state == "ESCAPE":
            radius = 2
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True, radius=radius
        )
        accessible = []
        for i in possible_steps:
            if self.model.extended_grid[i] == "OPEN":
                accessible.append(i)
        new_position = self.random.choice(accessible)
        self.model.grid.move_agent(self, new_position)

    def move_to_goal(self, radius):
        if radius == 1:
            self.state = "MOVE TO GOAL"
        elif radius != 1:
            self.state = "FAST MOVE TO GOAL"
        if self.pos == self.goal:
            new_position = self.pos
        else:
            if self.target is not None:
                if self.steal_state == "SNEAK":
                    goal = self.target.pos
                    radius = 2
                else:
                    goal=self.goal
            else:
                goal = self.goal

            hx, hy = goal
            accessible = []
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                radius=radius,
                moore=True, include_center=False)
            for i in possible_steps:
                if self.model.extended_grid[i] == "OPEN":
                    accessible.append(i)

            #print("current location", self.pos, "goal", self.goal)
            bestx, besty = 100, 100
            best = bestx*besty
            #print(accessible)
            for step in accessible:
                stepx, stepy = step
                if ((hx - stepx) ** 2 + (hy - stepy) ** 2 < best):
                    best = (hx - stepx) ** 2 + (hy - stepy) ** 2
                    bestx, besty = stepx, stepy


            if (bestx, besty) == (100, 100):
                try:
                    new_position = self.random.choice(accessible)
                except IndexError:
                    print("TODO - later")
                    '''print(self.pos)
                    print(accessible)
                    print(possible_steps)'''
                    new_position = self.random.choice(possible_steps)

            else:
                new_position = (bestx, besty)
        #print("besrt new location", new_position)


        self.model.grid.move_agent(self, new_position)

    def hang_around(self):
        self.state = "HANG AROUND"
        self.move()

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other_agent = self.random.choice(cellmates)
            other_agent.wealth += 1
            self.wealth -= 1



class Background(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        ### theft and property
        self.value_of_good = -1
        self.risk_threshold = None
        self.steal_state = "N"
        self.target = None

    def step(self):
        pass






class MoneyModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, topic, torus=False):
        self.num_agents = N
        self.topic = topic
        self.grid = MultiGrid(width, height, torus)
        self.extended_grid, self.accessible_list = self.make_extended_grid(width, height)
        self.possible_goal_states = self.get_possible_goal_states()
        self.schedule = RandomActivation(self)
        # Create agents
        self.create_agents(scenario=2)


        a = Background(self.num_agents+1, self)
        self.schedule.add(a)
        # Add the agent to a random grid cell
        x, y = self.initial_xy()
        self.time = 0
        self.grid.place_agent(a, (x, y))
        self.running = True

    def create_agents(self, scenario):
        if scenario == 1:
            for i in range(self.num_agents-1):
                a = MoneyAgent(i, random.choice(self.possible_goal_states), self)
                self.schedule.add(a)
                x, y = self.initial_xy()
                self.grid.place_agent(a, (x, y))

        if scenario == 2:   # one old agent, and one thief
            # old agent
            a = MoneyAgent(0, random.choice(self.possible_goal_states), self)
            self.schedule.add(a)
            x, y = self.initial_xy()
            self.grid.place_agent(a, (x, y))
            a.age = 80 # old agent
            a.value_of_good = 1000 # super tempting target
            a.risk_threshold = 5000 # will never steal risky
            a.age_threshold = 100   # will never steal even from old people (redundant)
            print(a.pos)

            all_neighbors = a.model.grid.get_neighborhood(pos=a.pos, moore=True, radius=3)  # agents see around them with radius 3
            print(all_neighbors)
            neighbors = []
            for i in all_neighbors:
                if a.model.extended_grid[i] == "OPEN":
                    neighbors.append(i)

            # thief
            a = MoneyAgent(1, random.choice(self.possible_goal_states), self)
            self.schedule.add(a)
            x, y = random.choice(neighbors)
            self.grid.place_agent(a, (x, y))
            a.age = 25  # young agent
            a.value_of_good = 0  # not tempting target
            a.risk_threshold = 1  # will always try to steal
            a.age_threshold = 0  # will steal from a baby


    def initial_xy(self):
        (x,y) = random.choice(self.accessible_list)
        return (x, y)

    def make_extended_grid(self, width, height):
        dict = {}
        it = 1
        w = width
        h = height
        accesible_list = []
        with open(self.topic+str('.csv')) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for j in csv_reader:
                for i in range(len(j)):
                    if j[i] == str(0):
                        dict[(i, h-it)] = "CLOSED"
                    else:
                        dict[(i, h-it)] = "OPEN"
                        accesible_list.append((i, h-it))
                it += 1
        return dict, accesible_list

    def get_possible_goal_states(self):
        n = []
        for (x, y) in self.accessible_list:
            if (x == self.grid.width-1 or x == 0 or y == 0 or y == self.grid.height-1):
                n.append((x, y))
        return n

    def step(self):
        self.schedule.step()
        self.time += 1