'''
These functions report the frequencies of
the relevant events. They belong to the
simulationTest class.

Print these reporters on the webpage later as well.
'''

class Reporters():

    def __init__(self):
        #self.belongs_to_experiment = experiment
        self.pure_frequency_event_dict = {}
        self.history_dict = {}
        self.run = 0

        self.history_dict[self.run] = {}

        self.initialize_event_dict(self.pure_frequency_event_dict)
        self.initialize_event_dict(self.history_dict[self.run])


    def initialize_event_dict(self, dict_):
        relevant_events = ["seen_object", "target_object", "compromise_house",
                           "observed", "successful_stolen", "unsuccessful_stolen"]
        for key in relevant_events:
            dict_[key] = 0

    def increase_counter(self, event):
        self.pure_frequency_event_dict[event] += 1
        self.history_dict[self.run][event] += 1

    def increase_run(self):
        self.run += 1
        self.history_dict[self.run] = {}
        self.initialize_event_dict(self.history_dict[self.run])

