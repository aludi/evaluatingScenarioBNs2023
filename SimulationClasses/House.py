from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
from SimulationClasses.Camera import Camera


class House(Agent):
    def __init__(self, unique_id, model, i_place, curtains_p):
        super().__init__(unique_id, model)
        self.width = 3
        self.height = 2
        self.x = (i_place*10 + 3)
        self.y = 2
        self.door_location = (i_place*10 + 3, 3)
        self.door_adjacent = self.circle_around_door()
        self.owner = None
        self.compromised = False    # if the stealing agent has compromised the house, they can get in.
        self.covers_pos = self.position_covered_by_house()
        self.adjacent_included = self.circle_around_house()
        if curtains_p < 33:
            self.curtains = True
        else:
            self.curtains = False
        self.camera = Camera(self.model.next_id(), self.model, self, 2, self.door_location)

    def has_curtains(self):
        return self.curtains

    def set_owner(self, agent):
        house = self
        self.owner = agent
        agent.set_house_owner(house)

    def get_owner(self):
        return self.owner

    def set_compromised(self):
        self.compromised = True

    def position_covered_by_house(self):
        min_x = self.x - 2 # why? TODO
        min_y = self.y - 1
        max_x = self.x + self.width
        max_y = self.y + self.height

        list_of_positions = []

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                list_of_positions.append((i, j))

        return list_of_positions

    def circle_around_door(self):
        door_x, door_y = self.door_location
        min_x = door_x - 1
        max_x = door_x + 1

        list_of_positions = []

        for i in range(min_x, max_x):
            list_of_positions.append((i, door_y + 1))

        return list_of_positions

    def circle_around_house(self):
        min_x = self.x - 3  # why? TODO
        min_y = self.y - 2
        max_x = self.x + self.width + 1
        max_y = self.y + self.height + 1

        list_of_positions = []

        for i in range(min_x, max_x):
            for j in range(min_y, max_y):
                list_of_positions.append((i, j))

        return list_of_positions



    def step(self):
        pass
