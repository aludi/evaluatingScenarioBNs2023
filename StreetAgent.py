from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random
from Vision import Vision
from Goodie import Goodie

class StreetAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.seen_goodie = 0
        self.owner = self
        self.name = None
        self.owns_house = None
        self.seen_objects = None
        self.target = None # target for stealing
        self.risk_threshold = random.randint(0, 1000)
        self.breaking_and_entering_skill = random.randint(0, 10)
        self.goal = "WALK ROAD"
        self.goodies = []
        self.objects_seen = {}
        self.observed = False

    def set_name(self, name):
        self.name = name

    def set_vision(self, radius):
        self.vision = Vision(self.model.next_id(), self.model, self, radius, self.pos)

    def set_goodie(self, pos):
        self.goodie = Goodie(self.model.next_id(), self.model, self, pos)
        self.goodies.append(self.goodie)


    def pot_steal_object(self, object_fact):
        (class_name, obj, unique_id, step_, owner) = object_fact
        if owner != self.unique_id: # potential steal
            # now we want to steal,
            self.seen_goodie = 1
            self.model.reporters.increase_counter_once("seen_object")
            # calculate stealing
            if (obj.value*1) > self.risk_threshold:  # Probability of getting away with it is 1 :) interesting C/B calculation here
                self.goal = "BREAK AND ENTER"
                self.target = obj
                obj.set_is_target_of(self)
                self.model.reporters.increase_counter("target_object")
            else:
                self.goal = "GO HOME"

    def update_objects_in_vision(self, objects):
        list_objects = []
        for object in objects:
            fact_tuple = (type(object).__name__, object, object.unique_id, self.model.schedule.steps, object.owner.unique_id)
            if type(object).__name__ == "Goodie":
                if self.target is None:
                    self.pot_steal_object(fact_tuple)
            list_objects.append(fact_tuple)

        self.objects_seen[self.model.schedule.steps] = list_objects
        # this means: this agent saw an object of TYPE, with number X, at time T, and with owner Y.

    def set_house_owner(self, house):
        self.owns_house = house

    def get_house(self):
        return self.owns_house

    def check_position(self, step):
        pos = step
        for house in self.model.houses:
            if self.unique_id == house.owner.unique_id: # if you own the house you can enter
                return True
            if house.compromised is True:   # everyone can enter a compromised house
                return True
            else:
                if pos in house.covers_pos: # you can't enter a house
                    return False

        return True # you can move anywhere else

    def move_step_to_goal(self, goal):
        hx, hy = goal
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, include_center=False)
        bestx, besty = 100, 100
        best = 100
        for step in possible_steps:
            stepx, stepy = step
            if ((hx - stepx) ** 2 + (hy - stepy) ** 2 < best) and self.check_position(step):
                best = (hx - stepx) ** 2 + (hy - stepy) ** 2
                bestx, besty = stepx, stepy

        if (bestx, besty) == (100, 100):
            #print("no best move", self.name)    # move randomly
            #print("RANDOM MOVE", self.name)    # move randomly

            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False)
            new_position = self.random.choice(possible_steps)
            return new_position

        #print("\t agent loc ", self.name, self.pos)
        #print("\t goal step", self.name, bestx, besty)
        #print("\t goal loc", self.name, hx, hy)


        return bestx, besty


    def go_home(self):
        a_house = self.get_house()
        hx, hy = a_house.x, a_house.y
        bestx, besty = self.move_step_to_goal((hx, hy))


        if (bestx, besty) == (hx, hy):
            # we are home
            pass
        else:
            self.move_agent_and_attributes(bestx, besty)

    def move_agent_and_attributes(self, new_x, new_y):
        self.model.grid.move_agent(self, (new_x, new_y))
        self.vision.be_moved()
        for goodie in self.goodies:
            goodie.be_moved((new_x, new_y))

    def check_observed(self):
        time = self.model.schedule.steps
        tuple_list = self.objects_seen[time]
        for item in tuple_list:
            a, b, c, d, e = item
            if a == "StreetAgent" and c is not self.unique_id:
                # see the other owner and go hide
                if self.observed == False:
                    self.model.reporters.increase_counter("observed")
                self.observed = True
                return True # go home
        return False    # keep stelaing

    def step(self):
        self.vision.step()
        goal = self.goal
        if goal == "GO HOME":
            door_x, door_y = self.get_house().door_location

            if self.target is not None:
                if self.pos == self.target.position and self.check_observed() == True:
                    self.model.reporters.increase_counter_once("unsuccessful_stolen")
                    self.model.reporters.decrease_counter_once("successful_stolen")

            if self.pos is not (door_x, door_y):
                self.go_home()
            else:
                pass
        elif goal == "WALK ROAD":
            (new_x, new_y) = self.move_step_to_goal((4, 4))
            self.model.grid.move_agent(self, (new_x, new_y))
            self.vision.be_moved()

        elif goal == "STAND STILL":  # headstart
            if self.model.schedule.steps > 3:
                self.goal = "GO HOME"

        elif goal == "BREAK AND ENTER":
            target_house = self.target.owner.owns_house
            (new_x, new_y) = self.move_step_to_goal(target_house.door_location)
            self.model.grid.move_agent(self, (new_x, new_y))
            self.vision.be_moved()

            # when in adjacent area, compromise house
            # print(self.breaking_and_entering_skill)
            if self.check_observed():  # if you can't steal, then go home without
                self.goal = "GO HOME"
                self.model.reporters.increase_counter_once("unsuccessful_stolen")
                self.model.reporters.decrease_counter_once("successful_stolen")


            if (new_x, new_y) in target_house.door_adjacent and self.breaking_and_entering_skill > 5:
                target_house.set_compromised()
                self.model.reporters.increase_counter_once("compromise_house")
                self.goal = "STEAL"

            if self.breaking_and_entering_skill < 5 and (new_x, new_y) in target_house.door_adjacent:   # if you can't steal, then go home without
                self.goal = "GO HOME"
                self.model.reporters.increase_counter_once("unsuccessful_stolen")
                self.model.reporters.decrease_counter_once("successful_stolen")



        elif goal == "STEAL":

            # move to target and take it
            (new_x, new_y) = self.move_step_to_goal(self.target.position)
            self.model.grid.move_agent(self, (new_x, new_y))
            self.vision.be_moved()


            if self.check_observed():   # if you can't steal, then go home without
                self.goal = "GO HOME"
                self.model.reporters.increase_counter_once("unsuccessful_stolen")
                self.model.reporters.decrease_counter_once("successful_stolen")



            if self.pos == self.target.position:
                self.goodies.append(self.target)
                self.goal = "GO HOME"
                if self.model.reporters.get_report_of_event("unsuccessful_stolen") != 1:
                    self.model.reporters.increase_counter_once("successful_stolen")  # TODO: double counting if observed after stolen...


        elif goal == "FLEE":
            (new_x, new_y) = self.move_step_to_goal((13, 4))
            self.move_agent_and_attributes(new_x, new_y)

