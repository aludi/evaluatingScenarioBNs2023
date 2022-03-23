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
        ### theft and property
        self.value_of_good = random.randrange(0, 1000)
        self.risk_threshold = random.randrange(900, 5000) # will steal if opportunity
        self.steal_state = "N"
        self.target = None
        self.ag_text = ":)"


    def step(self):
        if self.pos == self.goal:
            self.state = "GOAL"
            self.steal_state = "DONE"
            self.ag_text = ""


        else:
            if self.steal_state == "LOSER":
                self.ag_text = ":("

            elif self.steal_state == "STEALING":
                self.ag_text = "..💰"

            elif self.steal_state == "N":
                self.ag_text = ":)"


            all_neighbors = self.model.grid.get_neighbors(pos=self.pos, moore=True, radius=2) #agents see around them with radius 3
            neighbors = []
            for i in all_neighbors:
                if self.model.extended_grid[i.pos] == "OPEN":
                    neighbors.append(i)

            if self.target is not None:
                if self.target.pos == self.pos:
                    self.steal_state = "STEALING"
                    # stealing from the target!!
                    self.value_of_good += self.target.value_of_good
                    self.target.value_of_good = 0
                    self.target.steal_state = "LOSER"


                if self.target not in neighbors and self.target.pos != self.pos:
                    self.steal_state = "N"
                    self.target = None

            # check the neighbors for their values
            for agent in neighbors:
                if agent.value_of_good > self.risk_threshold and self.steal_state != "STEALING":
                    self.steal_state = "MOTIVE"
                    self.target = agent
                    self.ag_text = "8}"


            # if they see that they're surrounded by other agents, they're more likely to hang out.
            # at every step, agents check if they're near other agents,
            # and want to hang around in a crowd if that's the case.

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
                for x in self.position_list[y-10: -1]:
                    if x not in count_dict.keys():
                        count_dict[x] = 0
                    else:
                        count_dict[x] += 1

                for key in count_dict.keys():
                    if count_dict[key] > 3:
                        self.state = "ESCAPE"
                        #print(self.unique_id, "ESCAPE")


    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True
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
            hx, hy = self.goal
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
                    #print(bestx, besty)

            if (bestx, besty) == (100, 100):
                new_position = self.random.choice(accessible)
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



class Dagobert(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 100
        ### theft and property
        self.value_of_good = random.randrange(0, 1000)
        self.risk_threshold = random.randrange(400, 1000)  # will steal if opportunity
        self.steal_state = "N"
        self.target = None

    def step(self):
        pass





class MoneyModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, torus=False):
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus)
        self.extended_grid, self.accessible_list = self.make_extended_grid(width, height)
        self.possible_goal_states = self.get_possible_goal_states()
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents-1):
            a = MoneyAgent(i, random.choice(self.possible_goal_states), self)
            self.schedule.add(a)
            x, y = self.initial_xy()
            self.grid.place_agent(a, (x, y))

        a = Dagobert(self.num_agents, self)
        self.schedule.add(a)
        # Add the agent to a random grid cell
        x, y = self.initial_xy()
        self.time = 0
        self.grid.place_agent(a, (x, y))




        self.running = True

    def initial_xy(self):
        (x,y) = random.choice(self.accessible_list)
        return (x, y)

    def make_extended_grid(self, width, height):
        dict = {}
        it = 1
        w = width
        h = height
        accesible_list = []
        with open('groteMarkt.csv') as csv_file:
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
            if (x == 24 or x == 0 or y == 0 or y == 24):
                n.append((x, y))
        return n

    def step(self):
        self.schedule.step()
        self.time += 1