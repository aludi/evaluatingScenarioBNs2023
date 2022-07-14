from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace, HexGrid, MultiGrid
from SimulationClasses.StreetAgent import StreetAgent
from SimulationClasses.Camera import SecurityCamera
from Reporters import Reporters
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import numpy as np
import csv
import random


class WalkAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model, name):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.name = name
        self.anger = 0
        self.anger_slope = random.uniform(0, 1)
        self.target = None
        self.knife = False
        self.knife_ag = None
        self.dead = False



    def update_anger_level_find_target(self):
        #print(self.model.schedule.steps)
        y = self.anger_slope*self.model.schedule.steps

        knife = "none"
        other = "none"

        all_neighbors = self.model.grid.get_neighbors(pos=self.pos, moore=True, radius=24)
        for i in all_neighbors:
            if type(i) == Knife:
                knife = i
            if type(i) == WalkAgent and i != self:
                other = i
        #print(y, self.name, self.target)

        if self.name == "jane" and y > 3:
            self.anger = 1
            self.target = other
        if self.name == "mark" and y > 2:
            self.anger = 1
            self.target = other
        if self.name == "jane" and y > 10:
            self.anger = 2
            self.target = knife
        if self.name == "mark" and y > 35:
            self.anger = 2
            self.target = knife
        if self.name == "jane" and y > 17:
            self.anger = 3
            self.target = other
        if self.name == "mark" and y > 100:
            self.anger = 3
            self.target = other


    def move_step_to_goal(self, goal):
        if goal is None:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False)
            new_position = self.random.choice(possible_steps)
            return new_position

        hx, hy = goal.pos
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, include_center=False)
        bestx, besty = 100, 100
        best = 100
        for step in possible_steps:
            stepx, stepy = step
            if ((hx - stepx) ** 2 + (hy - stepy) ** 2 < best):
                best = (hx - stepx) ** 2 + (hy - stepy) ** 2
                bestx, besty = stepx, stepy

        if (bestx, besty) == (100, 100):
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False)
            new_position = self.random.choice(possible_steps)
            return new_position
        return (bestx, besty)

    def check_position(self):

        #print(self.name, self.target)
        if self.dead:
            self.target = self

        if self.target is None:
            pass
        else:
            if self.pos == self.target.pos:
                if type(self.target) == Knife:
                    #print(self.target, self.target.owner)
                    if self.target.owner == "none":
                        self.target.owner = self
                        self.knife_ag = self.target
                        self.knife = True
                        if self.name == "jane":
                            self.model.reporters.set_evidence_straight("jane_has_knife", 1)
                            self.model.reporters.set_evidence_straight("E_prints", 1)


                elif type(self.target) == WalkAgent and self.knife and self.anger > 2:
                    #print(self.pos, self.target.pos)
                    #print(f"{self.name} stabbed {self.target.name}")
                    self.model.reporters.set_evidence_straight("jane_stabs_mark_with_knife", 1)
                    self.model.reporters.set_evidence_straight("E_stab_wounds", 1)
                    #if random.randrange(0, 10) <= 7:
                    #    self.model.reporters.set_evidence_straight("E_testimony", 1)


                    self.model.stab = True

                    # if mark is unlucky he dies
                    if random.randrange(0, 100) > 60:
                        #print(f"{self.target.name} dies")
                        self.model.reporters.set_evidence_straight("mark_dies", 1)
                        self.model.reporters.set_evidence_straight("E_forensic", 1)
                    self.model.running = False



    def step(self):
        self.check_position()
        self.update_anger_level_find_target()
        #print("Hi, I am name " + str(self.name) + " and i'm angry ", str(self.anger))

        self.model.grid.move_agent(self, self.move_step_to_goal(self.target))
        if self.knife:
            self.knife_ag.be_moved()
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id


class Knife(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.owner = "none"

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def be_moved(self):
        #print("kife owner", self.owner.name)
        self.model.grid.move_agent(self, self.owner.pos)

    def step(self):
        pass



class WalkThrough(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, reporters, torus):
        self.num_agents = N
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.knife_in_sim = False
        self.stab = False
        names = ["jane", "mark"]
        # Create agents
        for i in range(self.num_agents):
            a = WalkAgent(i, self, names[i])
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))


        if random.randrange(0, 100) > 20:   # sometimes there's no knife
            a = Knife(self.num_agents+1, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.knife_in_sim = True

        self.running = True

        self.reporters = reporters
        self.reporters.history_dict[self.reporters.run] = {}
        self.reporters.initialize_event_dict(self.reporters.history_dict[self.reporters.run])  # initalize current run tracker with 0

    def step(self):
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id
        self.schedule.step()

        fight = 0
        for agent in self.schedule.agents:
            if type(agent) == WalkAgent:
                if agent.anger > 0:
                    fight += 1


        #print(self.schedule.steps)
        if self.schedule.steps > 8 and fight == 0:
            self.running = False
            return "x"

        if self.schedule.steps > 8 and self.knife_in_sim == False:
            #print(self.schedule.steps, 'in here')
            self.running = False
            return "x"

        if self.stab == True:
            return "x"


        if fight > 1:
            self.reporters.set_evidence_straight("jane_and_mark_fight", 1)
        if fight > 0:
            self.reporters.set_evidence_straight("E_neighbor", 1)


def set_reporters():
    rel_events = ["jane_and_mark_fight",
                       "jane_has_knife",
                       "jane_stabs_mark_with_knife",
                       "mark_dies",
                       "E_neighbor",
                       "E_prints",
                       "E_stab_wounds",
                       "E_forensic"]

    return Reporters(rel_events)



def agent_portrayal(agent):
    colors = ["yellow", "orange", "red", "purple"]
    if type(agent) == WalkAgent:

        if agent.dead == True:
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "black",
                         "r": 0.5}
        else:
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": colors[agent.anger],
                         "r": 0.5,
                         "text": agent.name,
                         "text_color": "black"}


    elif type(agent) == Knife:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "r": 0.25,
                     "Layer": 0,
                     "Color": "blue"
                     }
    return portrayal

'''
reporters = set_reporters()
print(reporters.relevant_events)
grid = CanvasGrid(agent_portrayal, 8, 3, 500, 250)
server = ModularServer(WalkThrough,
                       [grid],
                       "My Model",
                       {'N': 2, 'width':8, 'height':3, 'reporters':reporters, 'torus':True})
server.launch()
'''
