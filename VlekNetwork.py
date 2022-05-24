import random
import csv
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np
from collections import defaultdict


import csv
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np
import os
from collections import defaultdict


class VlekNetwork(Model):

    def __init__(self, runs, train):
        self.path = "/experiments/VlekNetwork/"
        self.train = train
        self.run = runs
        self.mark_and_jane()



    def mark_and_jane(self):  # this is the basic game with independent agents.
        kbFull = [
            ([], "jane_and_mark_fight", 20, 0),
            ([], "jane_has_knife", 70, 0),
            (["jane_and_mark_fight", "jane_has_knife"], "jane_stabs_mark_with_knife", 1, 1),
            (["jane_stabs_mark_with_knife"], "mark_dies", 70, 2),
            (["jane_and_mark_fight", "jane_has_knife"], "jane_threatens_mark_with_knife", 3, 1),
            (["jane_threatens_mark_with_knife"], "mark_hits_jane", 90, 2), #90
            (["mark_hits_jane"], "jane_drops_knife", 50, 3), # 50
            (["jane_drops_knife"], "mark_falls_on_knife", 10, 4),    #1
            (["mark_falls_on_knife"], "mark_dies_by_accident", 60, 5), #60
            (["mark_dies_by_accident"], "mark_dies", 100, 6)

            ]

        kb1 = [
            ([], "jane_and_mark_fight", 20, 0),
            ([], "jane_has_knife", 70, 0),
            (["jane_and_mark_fight", "jane_has_knife"], "jane_stabs_mark_with_knife", 1, 1),
            (["jane_stabs_mark_with_knife"], "mark_dies", 70, 2)
            ]
        kb2 = [
            ([], "jane_and_mark_fight", 20, 0),
            ([], "jane_has_knife", 70, 0),
            (["jane_and_mark_fight", "jane_has_knife"], "jane_threatens_mark_with_knife", 3, 1),
            (["jane_threatens_mark_with_knife"], "mark_hits_jane", 90, 2),  # 90
            (["mark_hits_jane"], "jane_drops_knife", 50, 3),  # 50
            (["jane_drops_knife"], "mark_falls_on_knife", 10, 4),  # 1
            (["mark_falls_on_knife"], "mark_dies_by_accident", 60, 5),  # 60
            (["mark_dies_by_accident"], "mark_dies", 100, 6)

            ]


        block = {"jane_stabs_mark_with_knife" : "jane_threatens_mark_with_knife",  # mutually exclusive
            "jane_threatens_mark_with_knife" : "jane_stabs_mark_with_knife"}

        for kb in [kbFull, kb1, kb2]:
            if kb == kbFull:
                name_x = "KBFull"
            elif kb == kb1:
                name_x = "KB1"
            else:
                name_x = "KB2"
            freq_dict = defaultdict(int)
            current_inf_dict = {}
            j = 0
            output_list = []
            while j < self.run:
                current_inf = []
                for fact_tup in kb:
                    a, b, c, d = fact_tup
                    current_inf_dict[b] = 0
                i = 0
                while i < 10:
                    for fact_tup in kb:
                        prem, conc, prob, time_idx = fact_tup
                        flag = True
                        for p_x in prem:
                            if p_x not in current_inf:
                                flag = False
                        if flag and random.randint(0, 100) <= prob and conc not in current_inf and time_idx == i:
                            try:
                                if block[conc] not in current_inf:
                                    current_inf.append(conc)
                                    current_inf_dict[conc] = 1
                            except KeyError:    # no blockers
                                current_inf.append(conc)
                                current_inf_dict[conc] = 1
                    #print(current_inf)

                    random.shuffle(kb)
                    i = i + 1

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

            current_inf_dict[conc] = 1


            csv_columns = current_inf_dict.keys()

            csv_file = os.getcwd() + self.path + f"{self.train}/{name_x}.csv"

            with open(csv_file, 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(csv_columns)
                for data in output_list:
                    #print(data)
                    writer.writerow(data)