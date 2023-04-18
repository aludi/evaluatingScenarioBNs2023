from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import ContinuousSpace, HexGrid, MultiGrid
from SimulationClasses.StreetAgent import StreetAgent
from SimulationClasses.Camera import SecurityCamera
from Reporters import Reporters
import numpy as np
import csv
import random

class MoneyAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, goal_state, model):
        super().__init__(unique_id, model)
        self.wealth = 1
        self.goal = goal_state
        self.thresholds = [random.random(), random.random(), random.random()]    # talk sing dance
        self.thresholds.sort()
        self.cooldown_time = random.randint(10, 15)
        self.state_timer = 10
        self.state = "HANG AROUND"
        self.position_list = []
        ### Personal details
        self.age = random.randrange(16, 95)
        self.name = self.pick_a_name()
        self.role = None
        ### theft and property
        self.value_of_good = random.randrange(0, 1000)
        self.risk_threshold = random.randrange(200, 5000) # will steal if opportunity
        self.age_threshold = random.randrange(16, 100) # minimum age an agent will steal from
        self.steal_state = "N"
        self.target = None
        self.temp_goal = None
        self.ag_text = ":)"

    def pick_a_name(self):
        first_names = ["ursula", "neil", "ada", "naomi", "margaret",
                 "gerda", "nick", "china", "becky", "douglas",
                 "octavia", "jeff", "hella", "hilary", "aafke", "john",
                 "terry"]
        last_names = ["cornflower", "olive", "daisy", "tulip",
                      "violet", "lemon", "orange", "apple", "pear",
                      "maroon", "plum"]

        name = random.choice(first_names) + " " + random.choice(last_names)
        return name
    
    
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


        #pass
        #self.model.extended_grid[i] == "OPEN":

    def calculate_psych_report(self, victim_val, victim_ag, self_val, self_age):
        ''' a psychologist is going to estimate if the victim fits the profile
        we create two normal distributions, one around the victim valueable and
        one about the age, draw from them as an estimation of what the threshold
        is for the suspect. If the drawn value is below the actual value, the psych
        report has estimated wrongly
        '''

        if random.randint(0, 9) > 8:
            return 0
        else:
            return 1
        '''est_risk_threshold = np.random.normal(victim_val, 100)
        est_age_threshold = np.random.normal(victim_ag, 20)
        #print(est_risk_threshold, self_val)
        #print(est_age_threshold, self_age)

        
        if est_risk_threshold > self_val and self_age < est_age_threshold:
            #print("\t\t correct")
            return 1    # psych correctly estimated who the suspect wants to rob
        else:
            #print("\t\t not correct")

            return 0 # incorrect assessment0'''

    def witness_valuable(self):
        '''
        Wtinesses might lie with some fixed probability. In this case,
        a probability of 0.1 because why would you lie?
        '''

        if np.random.randint(0, 10) < 9:
            return 1    # victim does not lie
        else:
            return 0 # victim lies

    def witness_vulnerable(self):
        '''
        Wtinesses might lie about being vulnerable with some fixed probability. In this case,
        a probability of 0.20
        "i don't know why the thief would target me", kind of stuff.
        '''

        if np.random.randint(0, 5) < 4:
            return 1    # victim does not lie
        else:
            return 0 # victim lies





    def step(self):
        if self.pos == self.goal:
            self.state = "GOAL"
            self.steal_state = "DONE"
            self.value_of_good = -1
            self.ag_text = ""


        else:

            # at every step, you have a very very very small probability of dropping your object
            if self.steal_state != "LOSER" and self.unique_id != 1:  # we don't care if the thief drops object
                x = np.random.randint(0, 100000)
                if x >= 99500:
                    self.model.reporters.set_evidence_straight(f"object_dropped_accidentally_{str(self.unique_id)}", 1)
                    self.value_of_good = -1
                    self.model.reporters.set_evidence_straight(f"E_object_gone_{str(self.unique_id)}", 1)

            if self.steal_state == "SUCCESS":
                self.steal_state = "N"

            if self.steal_state == "STEALING":
                self.state = "FAST MOVE TO GOAL"
                #print("stealing")
                if self.target is not None:
                    if self.target.steal_state == "DONE" or self.target.value_of_good == -1:
                        if self.target.value_of_good != -1:
                            self.model.reporters.set_evidence_straight(f"E_object_gone_0", 0)
                        self.target = None
                        self.steal_state = "N"
                        self.model.reporters.set_evidence_straight(f"E_camera_seen_stealing_1_0", 0)  # catching fail condition

                    if self.target is not None:
                        if self.target.value_of_good >= self.risk_threshold: # the agent might have been robbed before you got there
                            self.model.reporters.set_evidence_straight(f"stealing_{str(self.unique_id)}_0", 1)
                            self.model.reporters.set_evidence_straight(f"E_object_gone_0", 1)
                            self.value_of_good += self.target.value_of_good
                            self.target.value_of_good = 0
                            self.target.steal_state = "LOSER"
                            self.steal_state = "SUCCESS"
                        else:
                            self.steal_state = "N"
                            self.model.reporters.set_evidence_straight(f"E_object_gone_0", 0)
                            self.model.reporters.set_evidence_straight(f"E_camera_seen_stealing_1_0", 0) # catching fail condition



            if self.steal_state == "SNEAK":
                self.model.reporters.set_evidence_straight(f"sneak_{str(self.unique_id)}_0", 1)
                self.model.reporters.set_evidence_straight(f"E_sneak_{str(self.unique_id)}_0", 1)

                self.state = "FAST MOVE TO GOAL"
                #print("sneaking")
                if self.target is not None:
                    if self.target.steal_state == "DONE":
                        self.target = None
                        self.steal_state = "N"

                if self.target is not None:
                    if self.pos == self.target.pos:
                        #print("I'm in the same place as my target")
                        self.steal_state = "STEALING"

            if self.steal_state == "MOTIVE":
                self.model.reporters.set_evidence_straight(f"motive_{str(self.unique_id)}_0", 1)
                self.model.reporters.set_evidence_straight(f"E_psych_report_{str(self.unique_id)}_0",
                                                           self.calculate_psych_report(self.target.value_of_good, self.target.age,
                                                                                       self.risk_threshold,
                                                                                       self.age_threshold))

                self.state = "FAST MOVE TO GOAL"
                # print("I want to steal")


                if self.target.steal_state == "DONE":
                    self.target = None
                    self.steal_state = "N"

                elif self.target.pos != self.pos:
                    self.steal_state = "SNEAK"


                else:
                    self.steal_state = "STEALING"



            # check the neighbors for their values

            all_neighbors = self.model.grid.get_neighbors(pos=self.pos, moore=True,
                                                          radius=10)  # agents see around them with radius 5
            neighbors = []
            for i in all_neighbors:
                if self.model.extended_grid[i.pos] == "OPEN":
                    neighbors.append(i)


            # an agent will try to steal from a neighbor if the neighbor is old enough, if
            # the neighbor has valuable goods, and if the agent is not currently stealing from
            # someone else.
            #print("taking steps")
            for agent in neighbors:

                if str(type(agent)) == "<class 'GroteMarkt.MoneyAgent'>":
                    #print(self.unique_id, agent.unique_id, agent)
                    if self.unique_id == 1:
                        if self.calculate_line_of_sight(agent) == "UNSEEN":
                            continue
                        print(self.model.reporters)
                        print(self.model.reporters.pure_frequency_event_dict)

                        self.model.reporters.set_evidence_straight(f"seen_{str(self.unique_id)}_{str(agent.unique_id)}", 1)

                        if agent.value_of_good > self.risk_threshold:
                            self.model.reporters.set_evidence_straight(f"know_valuable_{str(self.unique_id)}_{str(agent.unique_id)}", 1)
                            self.model.reporters.set_evidence_straight(
                                    f"E_valuable_{str(self.unique_id)}_{str(agent.unique_id)}", 1)


                        if agent.age > self.age_threshold:
                            self.model.reporters.set_evidence_straight(f"know_vulnerable_{str(self.unique_id)}_{str(agent.unique_id)}", 1)
                            self.model.reporters.set_evidence_straight(f"E_vulnerable_{str(self.unique_id)}_{str(agent.unique_id)}", 1)


                        #if self.steal_state == "N" or self.steal_state == "LOSER":
                        #    self.model.reporters.set_evidence_straight(f"able_to_steal_{str(self.unique_id)}_{str(agent.unique_id)}", 1)

                        if agent.value_of_good > self.risk_threshold and \
                            agent.age > self.age_threshold and \
                                (self.steal_state == "N" or self.steal_state == "LOSER"):
                            self.steal_state = "MOTIVE"
                            self.target = agent
                            self.temp_goal = agent.pos
                            self.state = "FAST MOVE TO GOAL"










            # if they see that they're surrounded by other agents, they're more likely to hang out.
            # at every step, agents check if they're near other agents,
            # and want to hang around in a crowd if that's the case.
            #print(self.state)
            if self.state == "HANG AROUND":
                self.hang_around()
            elif self.state == "MOVE TO GOAL":
                self.move_to_goal(radius=1)
            elif self.state == "ESCAPE":
                self.hang_around()
            else:
                self.move_to_goal(radius=1)




            if self.state_timer > self.cooldown_time and self.state != "ESCAPE":
                self.state_timer = 0
                t = random.random()
                #print(t, self.thresholds[2])
                if t > self.thresholds[2]: # max speed
                    self.state = "FAST MOVE TO GOAL"

                elif t > self.thresholds[1]:
                    self.state = "MOVE TO GOAL"

                else:
                    self.state = "HANG AROUND"

                if len(neighbors) > 20:  # 20 agents nearby is a crowd.
                    t = random.random()
                    if t > 0.25:
                        self.state = "HANG AROUND"

            if self.state_timer > self.cooldown_time and self.state == "ESCAPE":
                t = random.randrange(0, 20)
                if t > 17:
                    self.state = "HANG AROUND"


        self.position_list.append(self.pos)

        self.state_timer += 1

        if self.state != "ESCAPE":
            if len(self.position_list) > 10:
                y = len(self.position_list)
                count_dict = {}
                #print(self.position_list[y-10: -1])
                for x in self.position_list[y-10: -1]:
                    if x not in count_dict.keys():
                        count_dict[x] = 0
                    else:
                        count_dict[x] += 1

                for key in count_dict.keys():
                    if count_dict[key] > 3:
                        self.state = "ESCAPE"
                        #print(self.unique_id, "ESCAPE")

        if self.steal_state == "LOSER":
            self.ag_text = ":("

        elif self.steal_state == "STEALING":
            self.ag_text = "..💰"

        elif self.steal_state == "MOTIVE":
            self.ag_text = "👀"

        elif self.steal_state == "SNEAK":
            self.ag_text = "🐆"

        elif self.steal_state == "N":
            self.ag_text = ":)"


    def move(self):
        radius = 1
        if self.state == "ESCAPE":
            radius = 2
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=True, radius=radius
        )
        accessible = []
        for i in possible_steps:
            if self.model.extended_grid[i] == "OPEN":
                accessible.append(i)
        new_position = self.random.choice(accessible)
        self.model.grid.move_agent(self, new_position)

    def move_to_goal(self, radius):
        if radius == 1:
            self.state = "MOVE TO GOAL"
        elif radius != 1:
            self.state = "FAST MOVE TO GOAL"
        if self.pos == self.goal:
            new_position = self.pos
        else:
            if self.target is not None:
                if self.steal_state == "SNEAK":
                    goal = self.target.pos
                    radius = 2
                else:
                    goal=self.goal
            else:
                goal = self.goal

            hx, hy = goal
            accessible = []
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                radius=radius,
                moore=True, include_center=False)
            for i in possible_steps:
                if self.model.extended_grid[i] == "OPEN":
                    accessible.append(i)

            #print("current location", self.pos, "goal", self.goal)
            bestx, besty = 100, 100
            best = bestx*besty
            #print(accessible)
            for step in accessible:
                stepx, stepy = step
                if ((hx - stepx) ** 2 + (hy - stepy) ** 2 < best):
                    best = (hx - stepx) ** 2 + (hy - stepy) ** 2
                    bestx, besty = stepx, stepy


            if (bestx, besty) == (100, 100):
                try:
                    new_position = self.random.choice(accessible)
                except IndexError:
                    #print("TODO - later")
                    '''print(self.pos)
                    print(accessible)
                    print(possible_steps)'''
                    new_position = self.random.choice(possible_steps)

            else:
                new_position = (bestx, besty)
        #print("besrt new location", new_position)


        self.model.grid.move_agent(self, new_position)

    def hang_around(self):
        self.state = "HANG AROUND"
        self.move()

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other_agent = self.random.choice(cellmates)
            other_agent.wealth += 1
            self.wealth -= 1



class Background(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        ### theft and property
        self.value_of_good = -1
        self.risk_threshold = None
        self.steal_state = "N"
        self.target = None

    def step(self):
        pass

class BN(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        ### theft and property
        self.value_of_good = -1
        self.risk_threshold = None
        self.steal_state = "N"
        self.target = None

    def step(self):
        pass





class GroteMarktModel(Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, topic, reporters, scenario, output_file, torus=False):
        self.current_id = 0
        scenario = 2
        self.num_agents = N  # hardcoded with scenario
        self.topic = topic
        self.grid = MultiGrid(width, height, torus)
        self.extended_grid, self.accessible_list = self.make_extended_grid(width, height)
        self.possible_goal_states = self.get_possible_goal_states()
        self.schedule = RandomActivation(self)
        self.scenario = scenario
        self.model_description = self.set_model_text_explanation()
        self.output_file = output_file
        #print("num agents", N)
        # Create agents
        self.create_agents(self.scenario)


        a = Background(self.num_agents+1, self)
        self.schedule.add(a)
        # Add the agent to a random grid cell
        x, y = self.initial_xy()
        self.grid.place_agent(a, (x, y))

        a = BN(self.num_agents + 2, self)
        self.schedule.add(a)
        # Add the agent to a random grid cell
        x, y = self.initial_xy()
        self.grid.place_agent(a, (x, y))

        self.time = 0
        self.running = True

        # reporters -> meta
        if reporters is None:
            self.reporters = self.set_reporters()
        else:
            self.reporters = reporters
        self.reporters.history_dict[self.reporters.run] = {}
        self.reporters.initialize_event_dict(self.reporters.history_dict[self.reporters.run])  # initalize current run tracker with 0


        # place the security cameras scattered throughout the simulation
        #print(self.schedule.get_agent_count())

        for i in range(0, 5):
            SecurityCamera(self.num_agents + 10 + i, model=self, radius=5, position=(self.initial_xy()))



    def set_model_text_explanation(self):
        if self.scenario == 1:
            model_text = "State of nature: agents move towards goal and every agent can steal from any agent. " \
                         "Usually agents don't steal."
        elif self.scenario == 2:
            model_text = "There are two agents, a thief and a victim."
        elif self.scenario == 3:
            model_text = "There are more than two agents, but there's only one thief that will only target a specific victim."
        elif self.scenario == 4:
            model_text = "There is one designated victim, all the agents can steal from them."

        return model_text

    def set_reporters(self):
        if self.scenario == 1:
            self.num_agents = 4
        elif self.scenario == 2:
            self.num_agents = 2
        elif self.scenario == 3:
            self.num_agents = 6
        elif self.scenario == 4:
            self.num_agents = 6

        n = self.num_agents

        base_rel_events = ["seen",
                           "know_valuable",
                           "know_vulnerable",
                           "object_dropped_accidentally",
                           "motive",
                           "sneak",
                           "stealing",
                           "E_valuable",
                           "E_vulnerable",
                           "E_psych_report",
                           "E_camera",
                           "E_sneak",
                           "E_camera_seen_stealing",
                           "E_camera_sees_object",
                           "E_object_gone"]

        # create reporters automatically
        rel_events = []
        n = 2

        for i in range(1, n):
            for k in range(0, 1):
                for j in base_rel_events:  # "motive, sneak and stealing are 2 place predicates
                    if j in ["object_dropped_accidentally", "E_object_gone"]:
                        str1 = f"{j}_{str(i - 1)}"
                        rel_events.append(str1)
                    elif j in ["E_camera"]:
                        str1 = f"{j}_{str(i)}"
                        rel_events.append(str1)
                    else:
                        if i != k:
                            str1 = f"{j}_{str(i)}_{str(k)}"
                            # str2 = i + "_credibility"
                            rel_events.append(str1)
        return Reporters(rel_events)

    def create_agents(self, scenario):
        if scenario == 1:   # scenario 1 is
            for i in range(self.num_agents-1):
                a = MoneyAgent(i, random.choice(self.possible_goal_states), self)
                self.schedule.add(a)
                a.role = "thief"
                x, y = self.initial_xy()
                self.grid.place_agent(a, (x, y))

        elif scenario == 2:   # one old agent, and one thief
            # old agent
            old_agent = self.make_old_agent()
            #self.make_thief()
            self.make_thief_near_old_agent(old_agent) # make thief near old agent

        elif scenario == 3: # one thief, many innocents, but how do you know?
            old_agent = self.make_old_agent()
            self.make_thief_near_old_agent(old_agent) # make thief near old agent
            self.make_innocent_near_old_agent(old_agent, self.num_agents)

        elif scenario == 4:
            old_agent = self.make_old_agent()
            self.make_potential_thieves_near_old_agent(old_agent, self.num_agents)


    def make_innocent_near_old_agent(self, old_agent, N):
        all_neighbors = old_agent.model.grid.get_neighborhood(pos=old_agent.pos, moore=True, radius=3)
        neighbors = []
        for i in all_neighbors:
            if old_agent.model.extended_grid[i] == "OPEN":
                neighbors.append(i)
        for j in range(2, N):
            a = MoneyAgent(j, random.choice(self.possible_goal_states), self)
            self.schedule.add(a)
            x, y = random.choice(neighbors)  # pick from neighbors instead of entire map
            self.grid.place_agent(a, (x, y))
            a.age = random.randrange(13, 76)  # old agent
            a.value_of_good = -1  # not a tempting target
            a.risk_threshold = 4000 #random.randrange(0, 2000)  # will never steal risky
            a.age_threshold = 79  # will never steal even from old people (redundant)
            a.role = "innocent"

    def make_potential_thieves_near_old_agent(self, old_agent, N):  # they only steal from the old agent
        all_neighbors = old_agent.model.grid.get_neighborhood(pos=old_agent.pos, moore=True, radius=3)
        neighbors = []
        for i in all_neighbors:
            if old_agent.model.extended_grid[i] == "OPEN":
                neighbors.append(i)
        for j in range(1, N):
            a = MoneyAgent(j, random.choice(self.possible_goal_states), self)
            self.schedule.add(a)
            x, y = random.choice(neighbors)  # pick from neighbors instead of entire map
            self.grid.place_agent(a, (x, y))
            a.age = random.randrange(13, 76)  # old agent
            a.value_of_good = -1  # not a tempting target
            a.risk_threshold = random.randrange(0, 2000)  # will never steal risky
            a.age_threshold = 79  # will never steal even from old people (redundant)
            a.role = "thief"


    def make_old_agent(self):
        a = MoneyAgent(0, random.choice(self.possible_goal_states), self)
        self.schedule.add(a)
        x, y = self.initial_xy()
        self.grid.place_agent(a, (x, y))
        a.age = random.randint(60, 90)  # old agent
        a.value_of_good = random.randint(500, 1000)  # super tempting target
        a.risk_threshold = 5000  # will never steal risky
        a.age_threshold = 100  # will never steal even from old people (redundant)
        a.role = "victim"
        return a

    def make_thief(self):
        # thief
        a = MoneyAgent(1, random.choice(self.possible_goal_states), self)
        self.schedule.add(a)
        x, y = self.initial_xy()
        self.grid.place_agent(a, (x, y))
        a.age = 25  # young agent
        a.value_of_good = 0  # not tempting target
        a.risk_threshold = random.randint(800, 1200)  # steals sometimes
        a.age_threshold = random.randint(50, 100)  # would steal from anyone older than 50
        a.role = "thief"

    def make_thief_near_old_agent(self, old_agent):
        all_neighbors = old_agent.model.grid.get_neighborhood(pos=old_agent.pos, moore=True, radius=10)
        neighbors = []
        for i in all_neighbors:
            if old_agent.model.extended_grid[i] == "OPEN":
                neighbors.append(i)

        # thief
        a = MoneyAgent(1, random.choice(self.possible_goal_states), self)
        self.schedule.add(a)
        x, y = random.choice(neighbors)  # pick from neighbors instead of entire map
        self.grid.place_agent(a, (x, y))
        a.age = 25  # young agent
        a.value_of_good = 0  # not tempting target
        a.risk_threshold = random.randint(800, 1200)  # steals sometimes
        a.age_threshold = random.randint(50, 100)  # would steal from anyone older than 50
        a.role = "thief"



    def initial_xy(self):
        (x,y) = random.choice(self.accessible_list)
        return (x, y)

    def make_extended_grid(self, width, height):
        dict = {}
        it = 1
        w = width
        h = height
        accesible_list = []
        with open(self.topic+str('.csv')) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for j in csv_reader:
                for i in range(len(j)):
                    if j[i] == str(0):
                        dict[(i, h-it)] = "CLOSED"
                    else:
                        dict[(i, h-it)] = "OPEN"
                        accesible_list.append((i, h-it))
                it += 1
        return dict, accesible_list

    def get_possible_goal_states(self):
        n = []
        for (x, y) in self.accessible_list:
            if (x == self.grid.width-1 or x == 0 or y == 0 or y == self.grid.height-1):
                n.append((x, y))
        return n

    def step(self):
        self.schedule.step()
        self.time += 1
        #print(self.reporters.pure_frequency_event_dict)