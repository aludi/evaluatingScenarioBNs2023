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
            #print(self.reporters.pure_frequency_event_dict)
        self.print_frequencies()

    def conditional_frequencies(self, parent, child):
        # hardcoded for now: F(compromize house) given a value for target object
        # iterate over all of history
        count_neg = 0
        count_pos = 0
        pos_occ_count = 0
        neg_occ_count = 0

        for i in range(0, self.runs):
            val_parent = self.reporters.history_dict[i][parent]
            val_child = self.reporters.history_dict[i][child]
            if val_parent == 1:
                pos_occ_count += 1
            else:
                neg_occ_count += 1
            if val_parent == 0 and val_child == 1:
                count_neg += 1
            elif val_parent == 1 and val_child == 1:
                count_pos += 1


        print(parent, " AND ", child, (count_pos/pos_occ_count)*100)
        print("NOT", parent, " AND ", child, (count_neg/neg_occ_count)*100)

    def print_frequencies(self):
        print("\t Nice frequencies")
        for key in self.reporters.pure_frequency_event_dict.keys():
            print(key, (self.reporters.pure_frequency_event_dict[key] / self.runs)*100)

        self.conditional_frequencies("seen_object", "observed")
        print("\n")
        self.conditional_frequencies("observed", "unsuccessful_stolen")
        self.conditional_frequencies("observed", "no_stealing")

if __name__ == "__main__":
    Experiment()
