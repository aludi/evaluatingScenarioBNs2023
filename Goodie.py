from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

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
