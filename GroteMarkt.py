from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace, HexGrid, MultiGrid
from SimulationClasses.StreetAgent import StreetAgent
import numpy as np
import csv
import random

class MoneyAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        accessible = []
        for i in possible_steps:
            if self.model.extended_grid[i] == "OPEN":
                accessible.append(i)
        new_position = self.random.choice(accessible)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other_agent = self.random.choice(cellmates)
            other_agent.wealth += 1
            self.wealth -= 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()

class Dagobert(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 100

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other_agent = self.random.choice(cellmates)
            other_agent.wealth -= 1
            self.wealth += 1

    def step(self):
        #self.move()
        if self.wealth > 0:
            self.give_money()




class MoneyModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.extended_grid = self.make_extended_grid(width, height)
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents-1):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            x, y = self.initial_xy()
            # Add the agent to a random grid cell
            #x = self.random.randrange(self.grid.width)
            #y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        a = Dagobert(self.num_agents, self)
        self.schedule.add(a)
        # Add the agent to a random grid cell
        x, y = self.initial_xy()
        self.grid.place_agent(a, (x, y))


        self.running = True

    def initial_xy(self):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        if self.extended_grid[(x, y)] == "CLOSED":
            self.initial_xy()
        return (x, y)

    def make_extended_grid(self, width, height):
        dict = {}
        it = 0
        with open('groteMarkt.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for i in csv_reader:
                for j in range(len(i)):
                    if i[j] == '0':
                        dict[(it, j)] = "CLOSED"
                    else:
                        dict[(it, j)] = "OPEN"
                it += 1
        return dict

    def step(self):
        self.schedule.step()