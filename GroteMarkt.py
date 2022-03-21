from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace
from SimulationClasses.StreetAgent import StreetAgent
import numpy as np

import random

class GroteMarkt(Model):
    """
    Flocker model class. Handles agent creation, placement and scheduling.
    """

    def __init__(
        self,
        width=100,
        height=100,
    ):
        """
        Create a new Flockers model.
        Args:
            population: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            separation: What's the minimum distance each Boid will attempt to
                    keep from any other
            cohere, separate, match: factors for the relative importance of
                    the three drives."""

        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.make_map()
        self.make_agents()
        self.running = True

    def make_map(self):
        pos = np.array((0,0))
        a = Map(1, self, pos)
        self.space.place_agent(a, pos)
        self.schedule.add(a)

    def make_agents(self):
        x = self.random.random() * self.space.x_max
        y = self.random.random() * self.space.y_max
        pos = np.array((x, y))
        for i in range(2, 5):
            st = Test(i, self, pos)
            self.space.place_agent(st, pos)
            self.schedule.add(st)


    def step(self):
        self.schedule.step()

class Map(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)

    def step(self):
        pass


class Test(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)

    def step(self):
        x, y = self.pos
        print(x, y)
        x_new = (x + random.choice([1, -1])*self.random.random())
        y_new = (y + random.choice([1, -1])*self.random.random())
        print(x_new, y_new)
        self.pos = np.array((x_new, y_new))
