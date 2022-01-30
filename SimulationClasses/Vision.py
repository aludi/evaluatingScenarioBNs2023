from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

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