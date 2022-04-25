import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np

class CredibilityGame(Model):

    def __init__(self, N_agents, reporters, subtype, output_file):
        self.output_file = output_file
        if subtype == "basicGame":
            self.basic_game(N_agents, reporters)
        elif subtype == "strangeGame":
            self.strange_game(N_agents, reporters)



    def basic_game(self, N_agents, reporters):  # this is the basic game with independent agents.
        n = N_agents
        ground_truth = random.randint(0, 1)  # 50/50 proportion is not great
        reporters.set_value_directly("agent_steals", ground_truth)
        agent_dict = {}
        for i in range(n):
            agent_statement = random.randrange(0, 100)
            if i%3 == 0:    # one every 3rd agent is a lier
                if agent_statement < 80: #agents lie with 80% probability
                    agent_statement = 1 - ground_truth
                else:
                    agent_statement = ground_truth
            else:           # the other agents are mistaken sometimes.
                if agent_statement < 20: #agents are mistaken with 20% probability
                    agent_statement = 1 - ground_truth
                else:
                    agent_statement = ground_truth

            #print(f"agent {i} says {agent_statement}")
            reporters.set_value_directly(f"E_{i}_says_stolen", agent_statement)

            agent_dict[i] = agent_statement

        '''for i in range(n):
            if agent_dict[(i + 1) % n] != agent_dict[i]:
                pass
                #print(f"agent {i} disagrees with agent {(i + 1) % n}")
            else:
                pass
                #print(f"agent {i} agrees with agent {(i + 1) % n}")
                
'''

    def strange_game(self, N_agents, reporters):  # this is the basic game with independent agents.
        n = N_agents
        ground_truth = random.randint(0, 1)  # 50/50 proportion is not great
        reporters.set_value_directly("agent_steals", ground_truth)
        agent_dict = {}
        for i in range(n):
            agent_statement = random.randrange(0, 100)
            if i % 2 == 0:  # one every 3rd agent is a lier
                if agent_statement < 90:  # agents lie with 80% probability
                    agent_statement = 1 - ground_truth
                else:
                    agent_statement = ground_truth
            else:  # the other agents are mistaken sometimes.
                if agent_statement < 50:  # agents are mistaken with 20% probability
                    agent_statement = 1 - ground_truth
                else:
                    agent_statement = ground_truth

            # print(f"agent {i} says {agent_statement}")
            reporters.set_value_directly(f"E_{i}_says_stolen", agent_statement)

            agent_dict[i] = agent_statement


    def step(self):
        pass




