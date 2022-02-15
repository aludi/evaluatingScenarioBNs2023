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
        self.relevant_events = ["lost_object", "know_object", "target_object", "motive", "compromise_house",
                                "flees_startled", "successful_stolen", "raining", "curtains",
                                "E_object_is_gone",
                                "E_broken_lock",
                                "E_disturbed_house",
                                "E_s_spotted_by_house",
                                "E_s_spotted_with_goodie",
                                "E_private"]
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

    def set_value_directly(self, event, val):    # use for mutually exclusive events
        self.add_to_temporal_list(event)
        self.pure_frequency_event_dict[event] += val
        self.history_dict[self.run][event] += val

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

    def report(self, event, increase, evidence):
        # report that the trigger could have been fired.
        if not evidence:
            self.add_to_temporal_list(event)
        else:
            self.add_to_evidence_list(event)
        if increase and not evidence:
            self.increase_counter_once(event)
        if increase and evidence:
            self.increase_evidence_counter_once(event)

