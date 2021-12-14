'''
From here we run the whole experiment,
for like 100 runs.

also define some global probabily stuff here, later
TODO

'''

from Reporters import Reporters
from SimulationTest import StolenLaptop


class Experiment():

    def __init__(self):  # TODO: compromise house is strange
        self.runs = 5000  # to test
        self.reporters = Reporters()
        for i in range(0, self.runs):
            model = StolenLaptop(N_agents=2, N_houses=2, width=16, height=9, reporters=self.reporters)
            for j in range(20):
                model.step()
            if self.reporters.get_report_of_event('successful_stolen') == 0 and self.reporters.get_report_of_event(
                    'unsuccessful_stolen') == 0:
                # the agent decided to not steal, either because he didn't know there was something to steal,
                # of because the cost-benefit was not worth it.
                self.reporters.increase_counter_once("no_stealing")
        self.print_frequencies()

    def conditional_frequencies(self, parents, child):
        relevant_dict = self.reporters.history_dict
        conditional_dict = {}
        for i in range(0, self.runs):
            parent_index = ""
            for key in parents: # we only want to look at the values for the parents
                val_parent = relevant_dict[i][key]
                parent_index += str(key[0:3]) + str(val_parent)
            # then we get a key like 010010 or whatever
            try:
                full = parent_index + str(child[0:3]) + str(relevant_dict[i][child])
                conditional_dict[full] += 1
            except KeyError:
                full = parent_index + str(child[0:3]) + str(relevant_dict[i][child])
                conditional_dict[full] = 1
        print("Conditionals for CHILD ", child)
        for key in conditional_dict.keys():
            print("\t", key, conditional_dict[key])
        print()

        #print(conditional_dict)


    def print_bayesian_net_probs(self):
        print()
        self.conditional_frequencies([], "seen_object")
        self.conditional_frequencies(["seen_object"], "target_object")
        self.conditional_frequencies(["seen_object", "target_object"], "compromise_house")
        self.conditional_frequencies(["seen_object"], "observed")
        self.conditional_frequencies(["seen_object", "target_object", "compromise_house", "observed"], "unsuccessful_stolen")
        self.conditional_frequencies(["seen_object", "target_object", "compromise_house", "observed"], "successful_stolen")
        self.conditional_frequencies(["seen_object", "target_object", "compromise_house", "observed"], "no_stealing")
        print()



    def print_frequencies(self):
        print("\t Nice frequencies")
        for key in self.reporters.pure_frequency_event_dict.keys():
            print(key, (self.reporters.pure_frequency_event_dict[key] / self.runs)*100, 100-(self.reporters.pure_frequency_event_dict[key] / self.runs)*100)
        print("________________________________________")
        self.print_bayesian_net_probs() # TODO to do this automatically



if __name__ == "__main__":
    Experiment()
