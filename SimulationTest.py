from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
from SimulationClasses.StreetAgent import StreetAgent
from SimulationClasses.Walkway import Walkway
from SimulationClasses.House import House
from Reporters import Reporters
import numpy as np
import matplotlib.pyplot as plt


class StolenLaptop(Model):

    def __init__(self, N_agents, N_houses, width, height, reporters):
        self.running = True
        self.current_id = -1
        self.num_agents = N_agents
        self.num_houses = N_houses
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.houses = []
        self.agents = []
        self.walkways = []

        # reporters -> meta
        self.reporters = reporters
        self.reporters.history_dict[self.reporters.run] = {}
        self.reporters.initialize_event_dict(self.reporters.history_dict[self.reporters.run]) # initalize current run tracker with 0

        '''
        I want a house that belongs to 1 agent,
        and another agent walking past
        '''
        for i in range(self.num_agents):
            a = House(self.next_id(), self)
            self.schedule.add(a)
            self.grid.place_agent(a, (a.x, a.y))
            self.houses.append(a)


        road = Walkway(self.next_id(), self)
        self.schedule.add(road)
        self.grid.place_agent(road, (road.x, road.y))
        self.walkways.append(road)

        # house owner
        a = StreetAgent(self.next_id(), self)
        a.goal = "STAND STILL"
        a.set_name("watson")
        self.schedule.add(a)
        #x = self.grid.width - 1
        #y = self.grid.height - 1
        x = self.random.randrange(self.grid.width)
        y = self.grid.height-1
        self.grid.place_agent(a, (x, y))
        self.agents.append(a)
        self.houses[0 % 2].set_owner(a)
        a.set_vision(radius=0)
        a.set_goodie(pos=(a.owns_house.x, a.owns_house.y))
        a.goodies = []

        # thief
        a = StreetAgent(self.next_id(), self)
        a.goal = "WALK ROAD"
        self.schedule.add(a)
        a.set_name("moriaty")
        #x = self.grid.width - 1
        #y = road.y
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(a, (x, y))
        self.agents.append(a)
        self.houses[1 % 2].set_owner(a)
        a.set_vision(radius=3)

    def step(self):
        '''Advance the model by one step.'''
        #for a in self.agents:
        #    print(a.name, a.goal)
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


