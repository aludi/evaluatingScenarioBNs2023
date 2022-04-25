import random
import csv
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np
from collections import defaultdict


class VlekNetwork(Model):

    def __init__(self, N_agents, reporters, output_file):
        self.output_file = output_file


    def scn1(self, N_agents, reporters):  # this is the basic game with independent agents.




        '''n = N_agents
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
'''


kb = [
    ([], "jane and mark fight", 20),
    ([], "jane has knife", 70),
    (["jane and mark fight", "jane has knife"], "jane stabs mark with knife", 1),
    (["jane stabs mark with knife"], "mark dies", 70),
    (["jane and mark fight", "jane has knife"], "jane threatens mark with knife", 3),
    (["jane threatens mark with knife"], "mark hit jane", 90),
    (["mark hits jane"], "jane drops knife", 50),
    (["jane drops knife"], "mark falls on knife", 1),
    (["mark falls on knife"], "mark dies by accident", 60),
    (["mark dies by accident"], "mark dies", 100),

    ]

block = {"jane stabs mark with knife":"jane threatens mark with knife",  # mutually exclusive
    "jane threatens mark with knife":"jane stabs mark with knife"}

freq_dict = defaultdict(int)
current_inf_dict = {}



j = 0


output_list = []
while j < 2:
    current_inf = []
    for fact_tup in kb:
        a, b, c = fact_tup
        current_inf_dict[b] = 0
    i = 0
    while i < 100:
        for fact_tup in kb:
            prem, conc, prob = fact_tup
            flag = True
            for p_x in prem:
                if p_x not in current_inf:
                    flag = False
            if flag and random.randint(0, 100) <= prob and conc not in current_inf:
                try:
                    if block[conc] not in current_inf:
                        current_inf.append(conc)
                        current_inf_dict[conc] = 1
                except KeyError:    # no blockers
                    current_inf.append(conc)
                    current_inf_dict[conc] = 1





        random.shuffle(kb)
        i = i + 1

    print(current_inf)
    print(current_inf_dict)
    print("\n")
    l = []
    for key in current_inf_dict.keys():
        l.append(current_inf_dict[key])

    output_list.append(l)

    #print(current_inf_dict)


    try:
        freq_dict[str(current_inf)] += 1
    except KeyError:
        freq_dict[str(current_inf)] = 0
    j += 1

'''for key in sorted(freq_dict, key=freq_dict.get, reverse=True):
    print(key, freq_dict[key])'''



current_inf_dict[conc] = 1

csv_columns = current_inf_dict.keys()
csv_file = "VlekOutcomes.csv"

with open(csv_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_columns)
    for data in output_list:

        #print(data)
        writer.writerow(data)