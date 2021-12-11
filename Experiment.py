'''
From here we run the whole experiment,
for like 100 runs.

also define some global probabily stuff here, later
TODO

'''

from Reporters import Reporters
from SimulationTest import StolenLaptop

class Experiment():

    def __init__(self): # TODO: compromise house is strange
        self.runs = 10 # to test
        self.reporters = Reporters()
        for i in range(0, self.runs):
            print("RUN", i)
            model = StolenLaptop(N_agents=2, N_houses=2, width=16, height=9, reporters=self.reporters)
            for j in range(20):
                model.step()
            self.reporters.increase_run()


        for key in self.reporters.history_dict:
            print(key, self.reporters.history_dict[key])

        print(self.reporters.pure_frequency_event_dict)




if __name__ == "__main__":
    Experiment()



