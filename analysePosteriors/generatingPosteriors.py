


import pyAgrum as gum
from itertools import product
import csv



final_networks = ["BayesianNetworks/MG.net", "BayesianNetworks/MD.net"]
network_names = ["MG", "MD"]

evidence_nodes = {'E_psych_report_1_0' :0,
                  'E_camera_1' :0,
                  'E_camera_seen_stealing_1_0' :0,
                  'E_object_gone_0' :0}
total_set_nodes = {'E_psych_report_1_0' :0,
                   'E_camera_1' :0,
                   'E_camera_seen_stealing_1_0' :0,
                   'E_object_gone_0' :0,
                   "constraint" :[1, 1, 1, 0]}
outcome_nodes = ['stealing_1_0', 'object_dropped_accidentally_0']
dat_list = []
dat_list.append(["Network", "Evidence", "s1", "s2", "s3", "n", "incompatible"])


ev_sets = list(product([0 ,1], repeat = 4))

for it in range(0, len(final_networks)):
    bn =gum.loadBN(final_networks[it])
    network_name = network_names[it]
    ie = gum.LazyPropagation(bn)

    for ev_set in ev_sets:
        # print()
        # print(ev_set)
        for i in range(0, len(evidence_nodes)):
            k = list(total_set_nodes.keys())[i]
            # print(i, ev_set, ev_set[i])
            v = ev_set[i]
            total_set_nodes[k] = v
            # print(len(evidence_nodes))
        try:
            ie.setEvidence(total_set_nodes)
            p = gum.getPosterior(bn, evs=total_set_nodes, target='constraint')
            posteriors = [0, 0, 0, 0]
            for i in p.loopIn():
                x = dict(i.todict())
                posteriors[x["constraint"]] = p.get(i)
            # print(posteriors)
            dat_list.append([network_name, ev_set, posteriors[0], posteriors[1],
                             posteriors[2], posteriors[3], 0])

        except Exception as exception:
            # print(exception)
            dat_list.append([network_name, ev_set, 0, 0, 0, 0, 1])

# print(dat_list)
with open("analysePosteriors/Posteriors1.csv", 'w') as f:
    w = csv.writer(f)
    w.writerows(dat_list)

final_networks = ["BayesianNetworks/GG.net",
                  "BayesianNetworks/GD.net"]

network_names = ["GG", "GD"]
evidence_nodes = {'E_psych_report_1_0': 0,
                  'E_camera_1': 0,
                  'E_camera_seen_stealing_1_0': 0,
                  'E_object_gone_0': 0}

# outcome_nodes = ['stealing_1_0', 'object_dropped_accidentally_0']
dat_list = []
dat_list.append(["Network", "Evidence", "s1", "s2", "s3", "n", "incompatible"])
target = {'motive_1_0', 'sneak_1_0', 'stealing_1_0', 'object_dropped_accidentally_0'}

ev_sets = list(product([0, 1], repeat=4))

for it in range(0, len(final_networks)):
    bn = gum.loadBN(final_networks[it])
    network_name = network_names[it]
    ie = gum.LazyPropagation(bn)
    ie.addJointTarget(target)

    # print(bn.cpt('stealing_1_0'))
    print(network_name)
    for ev_set in ev_sets:
        # print()
        # print(ev_set)
        for i in range(0, len(evidence_nodes)):
            k = list(evidence_nodes.keys())[i]
            # print(i, ev_set, ev_set[i])
            v = ev_set[i]
            evidence_nodes[k] = v
            # print(len(evidence_nodes))
        try:
            ie.setEvidence(evidence_nodes)
            jp = ie.jointPosterior(target)
            # print(jp)
            # p = gum.getPosterior(bn, evs=evidence_nodes, target='constraint')
            posteriors = [0, 0, 0, 0]
            for i in jp.loopIn():

                x = dict(i.todict())
                if x == {'stealing_1_0': 1, 'motive_1_0': 1, 'sneak_1_0': 1, 'object_dropped_accidentally_0': 0}:
                    posteriors[0] = jp.get(i)
                elif x == {'stealing_1_0': 0, 'motive_1_0': 0, 'sneak_1_0': 0, 'object_dropped_accidentally_0': 1}:
                    posteriors[1] = jp.get(i)
                else:
                    posteriors[2] += jp.get(i)

                # posteriors[x["constraint"]] = p.get(i)
            print(posteriors)
            dat_list.append([network_name, ev_set, posteriors[0], posteriors[1],
                             posteriors[2], posteriors[3], 0])

        except Exception as exception:
            # print(exception)
            dat_list.append([network_name, ev_set, 0, 0, 0, 0, 1])

# print(dat_list)
with open("analysePosteriors/PosteriorsGenerated1.csv", 'w') as f:
    w = csv.writer(f)
    w.writerows(dat_list)
