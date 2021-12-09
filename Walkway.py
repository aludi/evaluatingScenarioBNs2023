from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

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
