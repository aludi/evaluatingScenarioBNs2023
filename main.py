from GroteMarkt import GroteMarktModel
from CreateMap import CreateMap
import os
from Reporters import Reporters
import csv


def create_reporters_for_agent_behaviour():

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
        "E_object_gone"
    ]

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

    return rel_events


def create_map():
    # create the map and size of simulation
    y = 20
    coverage = None
    topic_gen = os.getcwd() + "/groteMarkt.png"
    C = CreateMap(topic_gen, coverage, y)
    x = int(y*C.rel)
    return x, y, mapGm




# create map
x, y, mapGm = create_map()

# create reporters of measurements
reporters = Reporters(relevant_events=create_reporters_for_agent_behaviour())

# runs of simulation
runs = 10

# outcomes are stored:
outcome_file = "GroteMarktOutcomes.csv"


for i in range(0, runs):
    model = GroteMarktModel(N=2, width=x, height=y, topic=mapGm, reporters=reporters, scenario= "GroteMarktPrivate", output_file=outcome_file, torus=False)
    for j in range(100):
        model.step()
    reporters.increase_run()


history_list = []
for key in reporters.history_dict.keys():
    history_list.append(reporters.history_dict[key])
csv_columns = reporters.relevant_events

# remove unnecessary columns for simpler model
csv_columns.remove("E_camera_sees_object_1_0")
csv_columns.remove("E_valuable_1_0")
csv_columns.remove("E_vulnerable_1_0")
csv_columns.remove("E_sneak_1_0")
csv_columns.remove("know_valuable_1_0")
csv_columns.remove("know_vulnerable_1_0")
csv_columns.remove("seen_1_0")

csv_file = outcome_file

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, extrasaction='ignore') # write results to outcome file
        writer.writeheader()
        for data in history_list:
            writer.writerow(data)
except IOError:
    print("I/O error line 170 experiment")