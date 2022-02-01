'''
These functions report the frequencies of
the relevant events. They belong to the
simulationTest class.

Print these reporters on the webpage later as well.
'''

class Reporters():

    def __init__(self):
        self.pure_frequency_event_dict = {}
        self.history_dict = {}
        self.run = 0
        self.relevant_events = ["know_object", "target_object", "motive", "compromise_house",
                                "observed", "successful_stolen", "raining", "spotted_by_camera"]
        self.temporal_list = []
        self.evidence_list = []
        self.temporal_dict = {}
        self.history_dict[self.run] = {}
        self.initialize_event_dict(self.pure_frequency_event_dict)
        self.initialize_event_dict(self.history_dict[self.run])

    def add_to_temporal_list(self, event):
        if event not in self.temporal_list:
            self.temporal_list.append(event)
    def add_to_evidence_list(self, event):
        if event not in self.evidence_list:
            self.evidence_list.append(event)

    def initialize_event_dict(self, dict_):
        relevant_events = self.relevant_events
        for key in relevant_events:
            dict_[key] = 0

    def increase_counter(self, event):
        self.add_to_temporal_list(event)
        self.pure_frequency_event_dict[event] += 1
        self.history_dict[self.run][event] += 1

    def get_report_of_event(self, event):   # if event is not X
        return self.history_dict[self.run][event]

    def increase_evidence_counter_once(self, event):
        self.add_to_evidence_list(event)
        if self.history_dict[self.run][event] == 0:  # only increase if it is called for the first time :)
            self.pure_frequency_event_dict[event] += 1
            self.history_dict[self.run][event] += 1

    def increase_counter_once(self, event):
        self.add_to_temporal_list(event)
        if self.history_dict[self.run][event] == 0:  # only increase if it is called for the first time :)
            self.pure_frequency_event_dict[event] += 1
            self.history_dict[self.run][event] += 1

    def decrease_counter_once(self, event):  # only in case of successful stealing to unsuccesful stealing (being observed while stealing)
        if self.history_dict[self.run][event] == 1:
            self.pure_frequency_event_dict[event] -= 1
            self.history_dict[self.run][event] -= 1

    def increase_run(self):
        self.run += 1
        self.history_dict[self.run] = {}
        try:
            self.temporal_dict[tuple(self.temporal_list)] += 1
        except KeyError:
            self.temporal_dict[tuple(self.temporal_list)] = 1
        self.temporal_list = []
        self.initialize_event_dict(self.history_dict[self.run])

