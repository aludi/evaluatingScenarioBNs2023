from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

class Vision(Agent):

    def __init__(self, unique_id, model, agent, radius, position):
        super().__init__(unique_id, model)
        self.owner = agent
        (a, b) = position
        #if model.raining and radius > 1:    # if it rains we don't see as well (cameras also don't?)
        #    radius = radius - 1
        self.radius = radius
        self.model.grid.place_agent(self, (a, b))

    def get_new_position(self):
        return self.owner.pos

    def be_moved(self):
        (new_a, new_b) = self.owner.pos[0], self.owner.pos[1]
        self.model.grid.move_agent(self, (new_a, new_b))


    def step(self):
        neighbors = []
        (new_a, new_b) = self.owner.pos[0], self.owner.pos[1]
        neighbors = self.model.grid.get_neighbors(pos=(new_a, new_b), moore=True, radius=self.radius)
        rm_list = []
        for object_ in neighbors:
            if type(object_).__name__=="House":
                if object_.has_curtains() == True and type(self).__name__ != "Camera":
                    for item in neighbors:
                        if item.pos in object_.position_covered_by_house(): # then its invisible
                            rm_list.append(item)

        for item in rm_list:
            neighbors.remove(item)
        self.owner.update_objects_in_vision(neighbors)