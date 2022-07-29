from pylab import *
import matplotlib.pyplot as plt
import os
import pyAgrum as gum
import copy as copy
from Experiment import Experiment
import csv
import pandas as pd
import pickle

import math
import pyAgrum.lib.image as gim

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid


def simple():
    bn=gum.fastBN("c->r->w<-s<-c")

    bn.cpt("c").fillWith([0.5,0.5])

    bn.cpt("s")[0,:]=0.5 # equivalent to [0.5,0.5]
    bn.cpt("s")[1,:]=[0.9,0.1]

    bn.cpt("w")[{'r': 0, 's': 0}] = [1, 0]
    bn.cpt("w")[{'r': 0, 's': 1}] = [0.1, 0.9]
    bn.cpt("w")[{'r': 1, 's': 0}] = [0.1, 0.9]
    bn.cpt("w")[{'r': 1, 's': 1}] = [0.01, 0.99]
    bn.cpt("w")

    bn.cpt("r")[{'c':0}]=[0.8,0.2]
    bn.cpt("r")[{'c':1}]=[0.2,0.8]

    return bn


def nodes_for_bn(bn, nodes):
    for node in nodes:
        bn.add(gum.LabelizedVariable(node, node, 2))
    return bn


def links_for_bn(bn, nodes):
    # FULL BN
    for i in range(0, len(nodes)):
        for j in range(1, len(nodes)-i):
            bn.addArc(nodes[i], nodes[i+j])
    return bn

def generate_arc_links(exp):
    list_ = exp.reporters.relevant_events
    final_list = []
    prev_list = []
    for item in list_:
        prev = copy.deepcopy(prev_list)
        tupl_ = (prev, item)
        final_list.append(tupl_)
        prev_list.append(item)

    return final_list

def fill_cpts(bn, exp):
    list_ = generate_arc_links(exp)
    for x in list_:
        parents, child = x
        cpt_table = exp.conditional_frequencies_dict(parents, child, 2)
        for item in cpt_table:
            #print(item)
            tup = item.pop(child)
            count = item.pop("count")
            a, b = tup
            if count == 0:  # impossible combination (eg: not target object, but compromise house)
                count = 1   # TODO: HAAAACK FRAUD
                a = 0
                b = 1
            bn.cpt(child)[item] = [(b/count), (a/count)]
    return bn

def fill_cpts_rounded(bn, exp, f):
    list_ = generate_arc_links(exp)
    for x in list_:
        parents, child = x
        cpt_table = exp.conditional_frequencies_dict(parents, child, 2)
        for item in cpt_table:
            tup = item.pop(child)
            count = item.pop("count")
            a, b = tup
            if count == 0:  # impossible combination (eg: not target object, but compromise house)
                count = 1   # TODO: HAAAACK FRAUD
                a = 0
                b = 0
            #print(round(b/count, 1))
            bn.cpt(child)[item] = [round((b/count), f), round((a/count), f)]
    return bn


def fill_cpts_random(bn):
    for node in bn.nodes():
        bn.generateCPT(node)
        print(bn.cpt(node))
    return bn

def get_temporal_ordering_nodes(experiment, global_state_csv):
    print("best temporal ordering!")
    # determine the temporal order
    # consider only all temporal orders that include all events!
    max_score = 0
    # default ordering
    best_temporal_ordering = []
    header = next(csv.reader(open(global_state_csv)))
    for i in range(0, len(header)):
        best_temporal_ordering.append(i)  # default ordering is just [0, 1, ...]
        flag = "def"
    for key in experiment.reporters.temporal_dict.keys():
        if len(key) == len(experiment.reporters.relevant_events) - len(experiment.reporters.evidence_list):
            if experiment.reporters.temporal_dict[key] > max_score:
                best_temporal_ordering = list(key)
                max_score = experiment.reporters.temporal_dict[key]
                flag = "cust"
    best_ordering_in_col_numbers_list = []
    print(best_temporal_ordering)
    if len(list(header)) == len(experiment.reporters.relevant_events):
        if flag == "cust":
            for item in best_temporal_ordering:
                best_ordering_in_col_numbers_list.append(header.index(item))
            for item in experiment.reporters.evidence_list:
                best_ordering_in_col_numbers_list.append(header.index(item))
        else:
            best_ordering_in_col_numbers_list = best_temporal_ordering
    else:
        flag = "def"
        for item in header:
            best_ordering_in_col_numbers_list.append(header.index(item))

    #print(flag)
    #print(best_ordering_in_col_numbers_list)
    return best_ordering_in_col_numbers_list

def unpickle_dict(name):
    f = open(name, "rb")
    output = pickle.load(f)
    f.close()
    #print(output)
    return output

def get_temporal_ordering_nodes_path(training_data, path):
    # path + "/train/"+training_data
    header = next(csv.reader(open(path + "/train/" + training_data)))
    best_temporal_ordering = []

    #print("TEMPORAL ORDERING")

    for i in range(0, len(header)):
        #print(header[i])
        best_temporal_ordering.append(i)  # default ordering is just [0, 1, ...]
        flag = "def"

    if "KB" in training_data:
        return best_temporal_ordering

    # determine the temporal order
    # consider only all temporal orders that include all events!
    max_score = 0
    # default ordering

    temporal_dict_path = path+"/pickleJar/"+training_data[:-4]+"_temporal.pkl"
    relevant_dict_path = path+"/pickleJar/"+training_data[:-4]+"_relevantEvents.pkl"
    evidence_list_path = path+"/pickleJar/"+training_data[:-4]+"_evidenceList.pkl"

    temporal_dict = unpickle_dict(temporal_dict_path)
    relevant_dict = unpickle_dict(relevant_dict_path)
    evidence_list = unpickle_dict(evidence_list_path)
    #print(evidence_list)

    for key in temporal_dict.keys():
        if len(key) == len(relevant_dict) - len(evidence_list):
            if temporal_dict[key] > max_score:
                best_temporal_ordering = list(key)
                max_score = temporal_dict[key]
                flag = "cust"
    best_ordering_in_col_numbers_list = []
    #print(best_temporal_ordering)
    if len(list(header)) == len(relevant_dict):
        if flag == "cust":
            for item in best_temporal_ordering:
                #print(item)
                try:
                    if item[0] == "E":
                        print('evidence node in wrong list?')
                        evidence_list.append(item)
                    else:
                        best_ordering_in_col_numbers_list.append(header.index(item))
                except ValueError:
                    print("removed private item not in ordering")
            #print(best_ordering_in_col_numbers_list)

            for key in relevant_dict:
                print(key)
                if header.index(key) not in best_ordering_in_col_numbers_list and key[0] != "E":
                    try:
                        best_ordering_in_col_numbers_list.append(header.index(key))
                    except ValueError:
                        print("removed private item not in ordering")
            for item in evidence_list:
                #print(item)
                try:
                    best_ordering_in_col_numbers_list.append(header.index(item))
                except ValueError:
                    print("removed private evidence not in ordering")
            #print(best_ordering_in_col_numbers_list)
        else:
            best_ordering_in_col_numbers_list = best_temporal_ordering
    else:
        flag = "ev def"
        nl = []
        for item in header:
            if item[0] == "E":
                nl.append(header.index(item))
            else:
                best_ordering_in_col_numbers_list.append(header.index(item))

        for item in nl:
            best_ordering_in_col_numbers_list.append(item)

    #print(flag)
    #print(best_ordering_in_col_numbers_list)
    return best_ordering_in_col_numbers_list

def evidence_cannot_be_connected_to_each_other_path(training_data, path, temporal_ordering):
    if "KB" in training_data:   # we don't do this for tvlek networks
        return []
    #we know evidence is always added at the end
    forbidden_pairs = []
    evidence = []

    relevant_dict_path = path + "/pickleJar/" + training_data[:-4] + "_relevantEvents.pkl"
    relevant_dict = unpickle_dict(relevant_dict_path)

    for event in relevant_dict:
        if event[0] == "E":
            evidence.append(event)
    #evidence = temporal_ordering[-len(experiment.reporters.evidence_list):]  # we get column header idx
    #print("EVIDENCE")
    #print(evidence)
    for i in range(0, len(evidence)):
        for j in range(1, len(evidence) - i):
            forbidden_pairs.append((evidence[i], evidence[j+i]))
            forbidden_pairs.append((evidence[j+i], evidence[i]))
    return forbidden_pairs



def export_picture(training_data, path, runs):
    #print("in here, exporting picture")
    bn = gum.loadBN(path + "/BNs/"+training_data[:-4]+f"{runs}.net")
    ie = gum.LazyPropagation(bn)
    gim.exportInference(model=bn, filename=path + "/bnImage/BNIMAGE" + training_data[:-4]+f"{runs}.pdf", engine=ie, evs={})


def K2_BN_csv_only(training_data, path, runs):
    #print(path)
    #print("training data", training_data)

    learner = gum.BNLearner(path + "/train/"+training_data)  # using bn as template for variables and labels
    file_name = path + "/BNs/"+training_data[:-4]+f"{runs}.net"
    header = next(csv.reader(open(path + "/train/"+training_data)))

    best_temporal_ordering = get_temporal_ordering_nodes_path(training_data, path)
    #for i in range(0, len(header)):
    #    best_temporal_ordering.append(i)  # default ordering is just [0, 1, ...]

    #print(best_temporal_ordering)
    learner.useK2(best_temporal_ordering)

    #forbidden = evidence_cannot_be_connected_to_each_other_path(training_data, path, best_temporal_ordering)
    #for (a, b) in forbidden:
        #print(a, b)
        #learner.addForbiddenArc(a, b)

    # print(learner)
    bn = learner.learnBN()
    header = next(csv.reader(open(path + "/train/"+training_data)))

    for name in list(header):
        x = bn.cpt(name)
        i = gum.Instantiation(x)
        i.setFirst()
        # print(x)
        # print(i, i.todict(), type(name), name)
        while (not i.end()):
            #print(i, x[i.todict()])
            if 0.5 == x[i.todict()]:  # fix the never occurring situations -> maybe add an extra check for this TODO
                pass
                #print(i.todict()[name])
                #if i.todict()[name] == 0:
                #    bn.cpt(name)[i.todict()] = 1
                #elif i.todict()[name] == 1:
                #    bn.cpt(name)[i.todict()] = 0
            i.inc()
        bn.cpt(name)
    #print("current dir", os.getcwd())
    # print(file_name)
    gum.saveBN(bn, file_name)
    try:
        export_picture(training_data, path, runs)
        return 0
    except:
        print("not wide enough data -> rerunning training ")
        return 1

    # print(f"saved bn as {file_name}")
    #return bn

def evidence_cannot_be_connected_to_each_other(experiment, temporal_ordering):
    #we know evidence is always added at the end
    forbidden_pairs = []
    evidence = []
    for event in experiment.reporters.relevant_events:
        if event[0] == "E":
            evidence.append(event)
    #evidence = temporal_ordering[-len(experiment.reporters.evidence_list):]  # we get column header idx
    for i in range(0, len(evidence)):
        for j in range(1, len(evidence) - i):
            forbidden_pairs.append((evidence[i], evidence[j+i]))
            forbidden_pairs.append((evidence[j+i], evidence[i]))
    return forbidden_pairs

def K2_BN(experiment, csv_file, name):
    print(csv_file)
    global_state_csv = csv_file #"globalStates.csv"
    learner = gum.BNLearner(global_state_csv)  # using bn as template for variables and labels
    file_name = name #"BayesNets/K2BN.net"
    temporal_order = get_temporal_ordering_nodes(experiment, global_state_csv)
    if "adaptedK2BN.net" not in name:
        #forbidden = evidence_cannot_be_connected_to_each_other(experiment, temporal_order)
        forbidden  = []
        for (a, b) in forbidden:
            #print(a, b)
            learner.addForbiddenArc(a, b)
    #print(temporal_order)
    learner.useK2(temporal_order)
    #print(learner)
    bn = learner.learnBN()
    header = next(csv.reader(open(global_state_csv)))
    for name in list(header):

        x = bn.cpt(name)
        i = gum.Instantiation(x)
        i.setFirst()
        #print(x)
        #print(i, i.todict(), type(name), name)
        while (not i.end()):
            #print(i, "todict", i.todict(), type(i.todict()))
            if 0.5 == x[i.todict()]:    # fix the never occurring situations -> maybe add an extra check for this TODO
                if i.todict()[name] == 0:
                    bn.cpt(name)[i.todict()] = 1
                elif i.todict()[name] == 1:
                    bn.cpt(name)[i.todict()] = 0
            i.inc()

        bn.cpt(name)
    print("experiment", experiment)
    print("current dit", os.getcwd())
    gum.saveBN(bn, file_name)
    #print(f"saved bn as {file_name}")
    return bn

def K2_limited_BN(experiment):
    temp_global_state_csv = "globalStates.csv"
    d = pd.read_csv(temp_global_state_csv)
    for x in experiment.reporters.relevant_events:
        if x not in ["successful_stolen", "lost_object"]:
            #print(x[0])
            if x[0] != "E":
                d.pop(x)
    d.to_csv("partialStates.csv", index=False)

    K2_BN(experiment, "partialStates.csv", "K2Bns/adaptedK2BN.net")



### experiment with posterior outcomes
def get_outcome_posteriors_in_table(experiment, file_name, latex_file_name, extra_vals):
    bnK2 = gum.loadBN(file_name)
    ie = gum.LazyPropagation(bnK2)
    event_list = experiment.reporters.relevant_events
    evidence_list = []
    for ev in event_list:
        if ev[0] == 'E':    # evidence node TODO make a seperate class
            evidence_list.append(ev)

    with open(latex_file_name, 'w') as file:
        file.write(latex_file_name)
        file.write("\\begin{table}")
        file.write("\\begin{tabular}{c|c|c|c}")
        file.write("Evidence & Successful Stolen & Lost Object & Rest \\\\")
        file.write("\\hline")
        val = 1
        a = round(ie.posterior("successful_stolen")[1], 3)
        b = round(ie.posterior("lost_object")[1], 3)
        c = round(1 - a - b, 3)
        file.write(f" & {a} & {b} & {round(c, 3)} \\\\")
        for evidence in evidence_list:
            if evidence != "E_private":
                val = 1
            else:
                val = 0
            ie.addEvidence(evidence, val)
            a = round(ie.posterior("successful_stolen")[1], 3)
            b = round(ie.posterior("lost_object")[1], 3)
            c = round(1 - a - b, 3)
            l_key = evidence.replace("_", "\_")
            file.write(f"{l_key} = {val} & {a} & {b} & {round(c, 3)} \\\\")
        file.write("\\end{tabular}")
        if extra_vals is None:
            file.write("\\caption{Evidence set corresponding to scenario stealing. Outcome nodes.}")
        else:
            file.write("\\caption{Evidence set corresponding to scenario stealing. Outcome nodes."
                  "noise values are ", extra_vals, " }")

        file.write("\\end{table}")

        file.write("\n")

        ie = gum.LazyPropagation(bnK2)

        file.write("\\begin{table}")
        file.write("\\begin{tabular}{c|c|c|c}")
        file.write("Evidence & Successful Stolen & Lost Object & Rest \\\\")
        file.write("\\hline")
        a = round(ie.posterior("successful_stolen")[1], 3)
        b = round(ie.posterior("lost_object")[1], 3)
        c = round(1 - a - b, 3)
        file.write(f" & {a} & {b} & {round(c, 3)} \\\\")
        for evidence in evidence_list:
            if evidence in ["E_object_is_gone"]:
                val = 1
            else:
                val = 0
            ie.addEvidence(evidence, val)
            a = round(ie.posterior("successful_stolen")[1], 3)
            b = round(ie.posterior("lost_object")[1], 3)
            c = round(1 - a - b, 3)
            l_key = evidence.replace("_", "\_")
            file.write(f"{l_key} = {val} & {a} & {b} & {round(c, 3)} \\\\")
        file.write("\\end{tabular}")

        if extra_vals is None:
            file.write("\\caption{Evidence set corresponding to scenario lost. Outcome nodes.}")
        else:
            file.write("\\caption{Evidence set corresponding to scenario lost. Outcome nodes."
                  "noise values are ", extra_vals, " }")

        file.write("\\end{table}")

def get_evidence_list(experiment):
    event_list = next(csv.reader(open("partialStates.csv")))
    evidence_list = []
    for ev in event_list:
        if ev[0] == 'E':  # evidence node TODO make a seperate class
            evidence_list.append(ev)
    #print(evidence_list)
    return evidence_list

def get_posterior(ie, event):
    return round(ie.posterior(event)[1], 3)

def get_row_vals(ie, list_events):
    post = []
    x = 1
    for e in list_events:
        post.append(get_posterior(ie, e))
        x = x - get_posterior(ie, e)
    post.append(x)
    return post

def get_diff_outcome_posteriors_in_table(experiment, file_name1, file_name2, stolen):
    evidence_list = get_evidence_list(experiment)
    bn1 = gum.loadBN(file_name1)
    bn2 = gum.loadBN(file_name2)
    with open('table_gen.tex', 'w') as file:
        file.write("\\begin{table}")
        for turn in stolen:
            ie1 = gum.LazyPropagation(bn1)
            ie2 = gum.LazyPropagation(bn2)
            outcomes = ["successful_stolen", "lost_object"]
            file.write("\\begin{tabular}{c|c|c|c}")
            file.write("Evidence & Successful Stolen & Lost Object & Rest \\\\")
            file.write("\\hline")
            row1 = get_row_vals(ie1, outcomes)
            row2 = get_row_vals(ie2, outcomes)
            file.write(f" & {row1[0] - row2[0]} & {row1[1] - row2[1]} & {row1[2] - row2[2]} \\\\")
            for evidence in evidence_list:
                if turn == "lost":
                    if evidence in ["E_object_is_gone"]:
                        val = 1
                    else:
                        val = 0
                else:
                    if evidence != "E_private":
                        val = 1
                    else:
                        val = 0
                l_key = evidence.replace("_", "\_")
                ie1.addEvidence(evidence, val)
                ie2.addEvidence(evidence, val)
                row1 = get_row_vals(ie1, outcomes)
                row2 = get_row_vals(ie2, outcomes)

                file.write(f"{l_key} = {val} & {round(row1[0] - row2[0],3)} & {round(row1[1] - row2[1],3)} & {round(row1[2] - row2[2],3)} \\\\")
            file.write("\\end{tabular}")
            file.write("\\caption{Difference in posteriors in scenario " + turn + " }")
        file.write("\\end{table}")




def complex(experiment):
    file_name = "BayesNets/GodBN.net"
    bn = gum.BayesNet('GodBN')
    nodes = experiment.reporters.relevant_events
    bn = nodes_for_bn(bn, nodes)
    bn = links_for_bn(bn, nodes)
    bn = fill_cpts(bn, experiment)
    gum.saveBN(bn, file_name)
    print(f"saved bn as {file_name}")
    return bn

def rounded(experiment):
    file_name = "BayesNets/RoundedBN.net"
    rounding_param = 1
    bn = gum.BayesNet('RoundedBN')
    nodes = experiment.reporters.relevant_events
    bn = nodes_for_bn(bn, nodes)
    bn = links_for_bn(bn, nodes)
    bn = fill_cpts_rounded(bn, experiment, rounding_param)
    gum.saveBN(bn, file_name)
    print(f"saved bn as {file_name}")
    return bn




np.random.seed(1)
#experiment = Experiment(scenario="CredibilityGame")
'''if experiment.scenario == "StolenLaptop":
    K2_BN(experiment, experiment.csv_file_name, "K2Bns/K2BN.net")
    K2_limited_BN(experiment)

elif experiment.scenario == "CredibilityGame":
    K2_BN(experiment, experiment.csv_file_name, "CredBNs/main.net")'''

