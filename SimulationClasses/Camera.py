from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
from SimulationClasses.Vision import Vision

class Camera(Agent):

    def __init__(self, unique_id, model, agent, radius, position):
        super().__init__(unique_id, model)
        self.radius = radius
        self.owner = agent  # the owner of a camera is a house
        (x, y) = position
        self.model.grid.place_agent(self, (x, y))
        self.vision = Vision(self.model.next_id(), self.model, self, radius, self.pos)
        self.model.schedule.add(self)




    def step(self):
        (new_a, new_b) = self.owner.pos[0], self.owner.pos[1]
        neighbors = self.model.grid.get_neighbors(pos=(new_a, new_b), moore=True, radius=self.radius)

        for object in neighbors:
            if type(object).__name__ == "StreetAgent":
                if object.name == "moriaty" and object.owns_house != self.owner:
                    self.model.reporters.increase_evidence_counter_once("spotted_by_camera")