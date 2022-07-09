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
                if object.name == "moriarty" and object.owns_house != self.owner:
                    self.model.reporters.increase_evidence_counter_once("E_s_spotted_by_house")

                elif object.name == "moriarty" and object.goodies == [object.target]:
                    self.model.reporters.increase_evidence_counter_once("E_s_spotted_with_goodie")


class SecurityCamera(Agent):
    def __init__(self, unique_id, model, radius, position):
        super().__init__(unique_id, model)
        self.radius = radius
        (x, y) = position
        self.model.grid.place_agent(self, (x, y))
        self.model.schedule.add(self)


    def step(self):
        neighbors = self.model.grid.get_neighbors(pos=self.pos, moore=True, radius=self.radius)
        seen_victim = False
        seen_thief = False
        victim = None
        thief = None
        old_location_victim = 0
        old_location_thief = 0
        for object in neighbors:
            if type(object).__name__ == "MoneyAgent":
                if object.unique_id == 0 and self.calculate_line_of_sight(object) == "SEEN": #potential victim
                    seen_victim = True
                    victim = object
                    old_location_victim = object.pos
                elif object.unique_id == 1 and self.calculate_line_of_sight(object) == "SEEN": # potential thief
                    seen_thief = True
                    thief = object
                    old_location_thief = object.pos
                    if object.value_of_good > 0:    # the thief has stolen
                        pass
                        # sometimes the thief is stupid and we can see that they stole the thing on camera
                        #if random.randrange(0, 100000) > 9980:
                            #self.model.reporters.increase_evidence_counter_once(
                            #    f"E_camera_sees_object_0_1")
                            #self.model.reporters.increase_evidence_counter_once(
                                #f"E_camera_sees_object_1_0")
        if seen_victim and seen_thief:
            # the thief and victim were within the same camera range
            #self.model.reporters.increase_evidence_counter_once(f"E_camera_{str(victim.unique_id)}_{str(thief.unique_id)}")
            #print(self.model.reporters.relevant_events)
            self.model.reporters.increase_evidence_counter_once(f"E_camera_{str(thief.unique_id)}")


            # we might see the thief steal
            #print(thief.steal_state)
            if thief.steal_state == "STEALING":
                #print("stealing")
                self.model.reporters.increase_evidence_counter_once(
                    f"E_camera_seen_stealing_{str(thief.unique_id)}_{str(victim.unique_id)}")




    def calculate_line_of_sight(self, other_agent):
        #print("calculating line of sight")
        #print(self.pos, other_agent.pos)
        (x0, y0) = self.pos
        (x1, y1) = other_agent.pos
        dx = x0 - x1
        dy = y0 - y1
        D = 2*dy - dx
        y = y0
        #print(x0, x1)
        for x in range(x0, x1):
            #print(x, y)
            if self.model.extended_grid[self.pos] == "CLOSED":
                return "UNSEEN"
            if D > 0:
                y = y+1
                D = D - 2*dx
            if D == D + 2*dy:
                break
        return "SEEN"




