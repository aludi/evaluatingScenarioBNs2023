from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

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
