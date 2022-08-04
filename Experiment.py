'''
From here we run the whole experiment,
for like 100 runs.

also define some global probabily stuff here, later
TODO

'''
from itertools import product, combinations
import re
import os
import pickle

from Reporters import Reporters
from SimulationTest import StolenLaptop
import csv
#from CredibilityGame import CredibilityGame
from GroteMarkt import MoneyModel
#from VlekNetwork import VlekNetwork
#from WalkThrough import WalkThrough

from CreateMap import CreateMap
import pandas as pd


class Experiment():

    def __init__(self, scenario, runs, train, param_dict=None): #subtype=None):
        self.scenario = scenario
        self.train = train
        print("experiment scenario", scenario)
        self.runs = runs
        #self.csv_file_name = csv_file_name #"CredibilityGameOutcomes.csv"    # can take 2 shapes: "{experiment name}{Outcomes}.csv" and "{experiment name}{Test}.csv"
        self.bnDir = f"experiments/{scenario}/BNs"
        if scenario == "VlekNetwork":
            VlekNetwork(runs=runs, train=train)

        if scenario == "StolenLaptop" or scenario == "StolenLaptopVision" or scenario == "StolenLaptopPrivate":
            # iteration
            iterate_experiment = []
            if scenario == "StolenLaptop" or scenario == "StolenLaptopPrivate":
                iterate_experiment = [2]
            else:
                iterate_experiment = [2, 3, 4, 5, 6]
            print("scenario is stolen laptop")

            for camera_vision in iterate_experiment:
                rel_events = ["lost_object", "know_object", "target_object", "motive", "compromise_house",
                                        "flees_startled", "successful_stolen", "raining", "curtains",
                                        "E_object_is_gone",
                                        "E_broken_lock",
                                        "E_disturbed_house",
                                        "E_s_spotted_by_house",
                                        "E_s_spotted_with_goodie",
                                        "E_private"]



                self.reporters = Reporters(relevant_events = rel_events)
                for i in range(0, self.runs-1):
                    model = StolenLaptop(N_agents=2, N_houses=2, width=16, height=9, camera_vision=camera_vision, reporters=self.reporters, output_file = f"experiments/{scenario}/{self.train}")
                    for j in range(30):
                        model.step()
                    self.reporters.increase_run()
                #print("temporal", self.reporters.temporal_list, self.reporters.temporal_dict)



                '''
                
                f = open(f"experiments/{scenario}/{train}/{scenario}_temporal.pkl", "wb")
                pickle.dump(self.reporters.temporal_dict, f)
                f.close()
                f = open(f"experiments/{scenario}/{train}/{scenario}_relevantEvents.pkl", "wb")
                pickle.dump(self.reporters.relevant_events, f)
                f.close()
                f = open(f"experiments/{scenario}/{train}/{scenario}_evidenceList.pkl", "wb")
                pickle.dump(self.reporters.evidence_list, f)
                f.close()
                '''
                print("SCENARIO", scenario)
                if scenario == "StolenLaptop" or scenario == "StolenLaptopPrivate":
                    #print("who?")
                    self.generate_csv_report(file_path=f"experiments/{scenario}/{train}/{scenario}.csv")  # use these csvs for automatic BN structure determination
                    ### save temporal data to file
                    if train == "train":
                        self.pickle_relevant(scenario, train, scenario)  # pickles temporal dict, event dict and evidence list
                else:
                    self.generate_csv_report(file_path=f"experiments/{scenario}/{train}/{scenario}_param_{camera_vision}.csv")
                    ### save temporal data to file
                    #print("in here")
                    print(f"{scenario}_param_{camera_vision}")
                    if train == "train":
                        self.pickle_relevant(scenario, train, f"{scenario}_param_{camera_vision}")  # pickles temporal dict, event dict and evidence list
                self.print_frequencies()
                #self.print_frequencies_latex()



        if scenario == "CredibilityGame":
            self.n = 4
            n = self.n
            rel_events = ["agent_steals"]
            # create reporters automatically
            for i in range(0, n):
                str1 = f"E_{i}_says_stolen"
                #str2 = i + "_credibility"
                rel_events.append(str1)
                #rel_events.append(str2)

            self.reporters = Reporters(relevant_events=rel_events)
            for i in range(0, self.runs-1):
                CredibilityGame(N_agents=n, reporters=self.reporters, subtype=subtype, output_file = f"experiments/{scenario}/{self.train}")
                self.reporters.increase_run()

            self.generate_csv_report(f"experiments/{scenario}/{self.train}")
            self.print_frequencies()

        if scenario == "WalkThrough":
            rel_events = ["jane_and_mark_fight",
                          "jane_has_knife",
                          "jane_stabs_mark_with_knife",
                          "mark_dies",
                          "E_neighbor",
                          "E_prints",
                          "E_stab_wounds",
                          "E_forensic"]

            self.reporters = Reporters(relevant_events=rel_events)
            for i in range(0, self.runs - 1):
                # print(self.scenario)
                #print("i", i)

                model = WalkThrough(N=2, width=8, height=2, reporters=self.reporters, torus=True)

                for j in range(100):
                    a = model.step()
                    if a == 'x':
                        break
                    #print(a)
                self.reporters.increase_run()
                ### save temporal data to file

            # print(self.reporters.history_dict)

            print(self.reporters.pure_frequency_event_dict)

            self.generate_csv_report(file_path=f"experiments/{scenario}/{train}/{scenario}.csv")
            self.pickle_relevant(scenario, train,
                                 scenario)  # pickles temporal dict, event dict and evidence list



        if scenario == "GroteMarkt" or scenario == "GroteMarktMaps" or scenario == "GroteMarktPrivate":

            if scenario == "GroteMarkt" or "GroteMarktPrivate":
                iterate_experiment = ["groteMarkt.png"]
            else:
                iterate_experiment = ["groteMarkt.png", "Selwerd.png", "zuidCentrum.png","kattediep.png", "wall.png"]
            #iterate_experiment = ["groteMarkt.png", "Selwerd.png", "zuidCentrum.png", "kattediep.png", "wall.png"]
            print(scenario, iterate_experiment)
            for map in iterate_experiment:
                print(map)
                if type(map) == str:
                    map_name = os.getcwd()+f"/experiments/{scenario}/maps/" + map
                    coverage = None
                else:
                    map_name = os.getcwd()+f"/experiments/{scenario}/maps/random_"+str(map)
                    coverage = map

                self.subtype = param_dict["subtype"]
                #self.csv_file_name = "GroteMarktOutcomes.csv"

                self.scenario = param_dict["subtype"]
                #print(self.scenario)

                if self.scenario == 1:
                    self.n = 10
                elif self.scenario == 2:
                    self.n = 2
                elif self.scenario == 3:
                    self.n = 6
                elif self.scenario == 3:
                    self.n = 6

                self.n = 2

                n = self.n
                self.scenario = 2       # we are only experimenting with scenario 2!!!!


                base_rel_events = [
                "seen",
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
                                str1 = f"{j}_{str(i-1)}"
                                rel_events.append(str1)
                            elif j in ["E_camera"]:
                                str1 = f"{j}_{str(i)}"
                                rel_events.append(str1)
                            else:
                                if i != k:
                                    str1 = f"{j}_{str(i)}_{str(k)}"
                                    # str2 = i + "_credibility"
                                    rel_events.append(str1)

                y = 50
                C = CreateMap(map_name, coverage, y)
                x = int(y * C.rel)
                #print("x value", x, "y value", y)
                #print(rel_events)
                self.reporters = Reporters(relevant_events=rel_events)
                for i in range(0, self.runs-1):
                    #print(self.scenario)
                    #print("i", i)
                    model = MoneyModel(N=n, width=x, height=y, topic=map_name, reporters=self.reporters, scenario=self.scenario, output_file = f"experiments/{scenario}/{self.train}", torus=False)

                    for j in range(100):
                        model.step()
                    self.reporters.increase_run()
                    ### save temporal data to file


                #print(self.reporters.history_dict)

                #print(self.reporters.pure_frequency_event_dict)
                if scenario == "GroteMarkt" or scenario == "GroteMarktPrivate":
                    self.generate_csv_report(file_path=f"experiments/{scenario}/{train}/{scenario}.csv")
                    self.find_minimal_set(file_path=f"experiments/{scenario}/{train}/{scenario}.csv")

                    if train == "train":
                        self.pickle_relevant(scenario, train, scenario)  # pickles temporal dict, event dict and evidence list

                else:
                    print("in fucking here?")
                    self.generate_csv_report(file_path=f"experiments/{scenario}/{train}/{scenario}_map_{str(map)}.csv")
                    if train == "train":
                        self.pickle_relevant(scenario, train, f"{scenario}_map_{str(map)}")  # pickles temporal dict, event dict and evidence list



    def pickle_relevant(self, scenario, train, name):
        ### save temporal data to file
        print(name)
        f = open(f"experiments/{scenario}/pickleJar/{name}_temporal.pkl", "wb")
        pickle.dump(self.reporters.temporal_dict, f)
        f.close()
        f = open(f"experiments/{scenario}/pickleJar/{name}_relevantEvents.pkl", "wb")
        pickle.dump(self.reporters.relevant_events, f)
        f.close()
        f = open(f"experiments/{scenario}/pickleJar/{name}_evidenceList.pkl", "wb")
        pickle.dump(self.reporters.evidence_list, f)
        f.close()

    def generate_csv_report(self, file_path): # drop columns here
        history_list = []
        print(file_path)
        #print("history dict", self.reporters.history_dict)
        for key in self.reporters.history_dict.keys():
            history_list.append(self.reporters.history_dict[key])


        csv_columns = self.reporters.relevant_events
        print(csv_columns)
        if "StolenLaptopPrivate" in file_path:
            csv_columns.remove("flees_startled")
            csv_columns.remove("E_private")

        if "GroteMarkt" in file_path:
            csv_columns.remove("E_camera_sees_object_1_0")
            print(file_path)

            if file_path == "experiments/GroteMarkt/train/GroteMarkt.csv":
                pass
            elif "GroteMarktPrivate" or "GroteMarktMaps" in file_path:
                print("in here")
                csv_columns.remove("E_valuable_1_0")
                csv_columns.remove("E_vulnerable_1_0")
                csv_columns.remove("E_sneak_1_0")
                csv_columns.remove("know_valuable_1_0")
                csv_columns.remove("know_vulnerable_1_0")
                csv_columns.remove("seen_1_0")

        csv_file = file_path
        #csv_file = os.getcwd() + self.path + f"{self.train}/{file_name}.csv"
        #print(csv_file)
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns, extrasaction='ignore')
                writer.writeheader()
                for data in history_list:
                    writer.writerow(data)
        except IOError:
            print("I/O error line 170 experiment")

    def calc_minimal_set(self, scn, file_path):

        df = pd.read_csv(file_path)
        all_ev = ["E_psych_report_1_0", "E_camera_1", "E_camera_seen_stealing_1_0", "E_object_gone_0"]
        com = [["E_psych_report_1_0"], ["E_camera_1"], ["E_camera_seen_stealing_1_0"], ["E_object_gone_0"]]
        for i in range(2, len(all_ev) + 1):
            for item in combinations(all_ev, i):
                com.append(list(item))

        min_set = -1

        for x in com:
            # print(x)
            val = list(product([0, 1], repeat=len(x)))
            for t in val:
                s = f""
                for i in range(0, len(x)):
                    # create query
                    s += f"{x[i]} == {t[i]} &"
                y = df.query(s[:-1])  # remove trailing &
                steal = y["stealing_1_0"].mean()
                drop = y["object_dropped_accidentally_0"].mean()
                # print(steal)
                # print(drop)
                if steal == 1 and scn == "steal":
                    print("\t minimal set steal : ", s[:-1])
                    min_set = s[:-1]
                if drop == 1 and scn == "drop":
                    print("\t minimal set drop : ", s[:-1])
                    min_set = s[:-1]
                if steal == 0 and drop == 0 and scn == "nothing":
                    print("\t minimal set nothing : ", s[:-1])
                    min_set = s[:-1]

                if min_set != -1:
                    return min_set



    def find_minimal_set(self, file_path):
        dict_r = {}
        #for scn in ["steal", "drop", "nothing"]:
        #    dict_r[scn] = self.calc_minimal_set(scn, file_path)
        return dict_r



    def generate_empty_tables(self, parents, child):
        comb = product([1, 0], repeat=len(parents)+1)
        list_of_possible_combinations = []
        for i in list(comb):
            new_str = ""
            for j in range(0, len(parents)+1):
                if j >= len(parents):
                    new_str += str(child[0:3]) + str(i[j])
                else:
                    new_str += str(parents[j][0:3]) + str(i[j])
            list_of_possible_combinations.append(new_str)
        conditional_dict = {}
        for item in list_of_possible_combinations:
            conditional_dict[item] = 0
        return conditional_dict


    def conditional_frequencies(self, parents, child):
        conditional_dict = self.generate_empty_tables(parents, child)
        relevant_dict = self.reporters.history_dict
        for i in range(0, self.runs):
            parent_index = ""
            for key in parents: # we only want to look at the values for the parents
                val_parent = relevant_dict[i][key]
                parent_index += str(key[0:3]) + str(val_parent)


            full = parent_index + str(child[0:3]) + str(relevant_dict[i][child])

            conditional_dict[full] += 1

        '''print("Conditionals for CHILD ", child)
        for key in conditional_dict.keys():
            print("\t", key, (conditional_dict[key]/self.runs) * 100)
        print()'''

        #print(conditional_dict)

    def generate_empty_tables_full(self, parents, child, var=2):
        comb = product([1, 0], repeat=len(parents))
        list_of_possible_combinations = []
        dict_ = {}
        list_of_dicts = []
        for i in list(comb):
            #print(i)
            dict_ = {}

            for j in range(0, len(parents)):
                dict_[parents[j]] = i[j]
                #print(parents[j], i[j])
            dict_[child] = tuple([0]*var)
            dict_["count"] = 0
            list_of_dicts.append(dict_)
        return list_of_dicts

    def conditional_frequencies_dict(self, parents, child, var=2):
        conditional_dict = self.generate_empty_tables_full(parents, child, var)
        relevant_dict = self.reporters.history_dict

        for i in range(0, self.runs):
            parent_index = ""
            #print(relevant_dict[i])
            for dict_ in conditional_dict:
                #print(dict_)
                correct_condition = True

                for key in dict_.keys():
                    var_name, value = key, dict_[key]
                    #print(var_name, value)

                    if var_name != child and var_name != "count":
                        #print("rel dict", relevant_dict[i][var_name], relevant_dict[i][var_name] != value)

                        if relevant_dict[i][var_name] != value: # we are in the right one if this is false for all of them
                            correct_condition = False
                            break
                #print(correct_condition)
                if correct_condition == True:
                    dict_["count"] += 1
                    #print("found the relevant condition")
                    #print(dict_)
                    if relevant_dict[i][child] == 1:
                        #print("child is true")
                        (pos, neg) = dict_[child]
                        dict_[child] = (pos + 1, neg)
                    else:
                        #print("child is false")
                        (pos, neg) = dict_[child]
                        dict_[child] = (pos, neg + 1)

        #print(conditional_dict)
        return conditional_dict

    def print_bayesian_net_probs(self):
        print()
        self.conditional_frequencies([], "seen_object")
        self.conditional_frequencies(["seen_object"], "target_object")
        self.conditional_frequencies(["seen_object", "target_object"], "motive")
        self.conditional_frequencies(["seen_object", "target_object"], "compromise_house")
        self.conditional_frequencies(["seen_object", "target_object", "compromise_house"], "observed")
        self.conditional_frequencies(["seen_object", "target_object", "compromise_house", "observed"], "unsuccessful_stolen")
        self.conditional_frequencies(["seen_object", "target_object", "compromise_house", "observed"], "successful_stolen")
        self.conditional_frequencies(["seen_object", "target_object", "compromise_house", "observed"], "no_stealing")
        print()






    def print_frequencies(self):
        print("\t Nice frequencies")
        for key in self.reporters.pure_frequency_event_dict.keys():
            print(key, (self.reporters.pure_frequency_event_dict[key] / self.runs)*100, 100-(self.reporters.pure_frequency_event_dict[key] / self.runs)*100)
        print("________________________________________")
        #self.print_bayesian_net_probs() # TODO to do this automatically

    def print_frequencies_latex(self):
        print("\t Nice frequencies")
        print(f"event & frequency true \% & frequency false \% \\\\")
        print("\hline")
        for key in self.reporters.pure_frequency_event_dict.keys():
            l_key = key.replace("_", "\_")
            print(f"{l_key} & {round((self.reporters.pure_frequency_event_dict[key] / self.runs)*100, 0)} & "
                  f"{round(100-(self.reporters.pure_frequency_event_dict[key] / self.runs)*100, 0)} \\\\")
        print("________________________________________")
        #self.print_bayesian_net_probs() # TODO to do this automatically



if __name__ == "__main__":
    #Experiment("StolenLaptop")
    #Experiment("CredibilityGame")
    Experiment("GroteMarkt")


