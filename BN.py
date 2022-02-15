from pylab import *
import matplotlib.pyplot as plt
import os
import pyAgrum as gum
import copy as copy
from Experiment import Experiment
import csv
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


def do_stolen(bn):
    bn.cpt("successful_stolen")[{'know_object': 0, 'target_object': 0, 'compromise_house': 0, 'observed': 0, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 0, 'target_object': 0, 'compromise_house': 0, 'observed': 1, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 0, 'target_object': 0, 'compromise_house': 1, 'observed': 0, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 0, 'target_object': 0, 'compromise_house': 1, 'observed': 1, 'motive': 1}] = [1, 0]

    bn.cpt("successful_stolen")[{'know_object': 0, 'target_object': 1, 'compromise_house': 0, 'observed': 0, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 0, 'target_object': 1, 'compromise_house': 0, 'observed': 1, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 0, 'target_object': 1, 'compromise_house': 1, 'observed': 0, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 0, 'target_object': 1, 'compromise_house': 1, 'observed': 1, 'motive': 1}] = [1, 0]

    bn.cpt("successful_stolen")[{'know_object': 1, 'target_object': 0, 'compromise_house': 0, 'observed': 0, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 1, 'target_object': 0, 'compromise_house': 0, 'observed': 1, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 1, 'target_object': 0, 'compromise_house': 1, 'observed': 0, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 1, 'target_object': 0, 'compromise_house': 1, 'observed': 1, 'motive': 1}] = [1, 0]

    bn.cpt("successful_stolen")[{'know_object': 1, 'target_object': 1, 'compromise_house': 0, 'observed': 0, 'motive': 1}] = [0, 1]
    bn.cpt("successful_stolen")[{'know_object': 1, 'target_object': 1, 'compromise_house': 0, 'observed': 1, 'motive': 1}] = [0, 1]
    bn.cpt("successful_stolen")[{'know_object': 1, 'target_object': 1, 'compromise_house': 1, 'observed': 0, 'motive': 1}] = [1, 0]
    bn.cpt("successful_stolen")[{'know_object': 1, 'target_object': 1, 'compromise_house': 1, 'observed': 1, 'motive': 1}] = [0, 1]
    bn.cpt("successful_stolen")[
        {'know_object': 0, 'target_object': 0, 'compromise_house': 0, 'observed': 0, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 0, 'target_object': 0, 'compromise_house': 0, 'observed': 1, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 0, 'target_object': 0, 'compromise_house': 1, 'observed': 0, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 0, 'target_object': 0, 'compromise_house': 1, 'observed': 1, 'motive': 0}] = [1, 0]

    bn.cpt("successful_stolen")[
        {'know_object': 0, 'target_object': 1, 'compromise_house': 0, 'observed': 0, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 0, 'target_object': 1, 'compromise_house': 0, 'observed': 1, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 0, 'target_object': 1, 'compromise_house': 1, 'observed': 0, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 0, 'target_object': 1, 'compromise_house': 1, 'observed': 1, 'motive': 0}] = [1, 0]

    bn.cpt("successful_stolen")[
        {'know_object': 1, 'target_object': 0, 'compromise_house': 0, 'observed': 0, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 1, 'target_object': 0, 'compromise_house': 0, 'observed': 1, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 1, 'target_object': 0, 'compromise_house': 1, 'observed': 0, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 1, 'target_object': 0, 'compromise_house': 1, 'observed': 1, 'motive': 0}] = [1, 0]

    bn.cpt("successful_stolen")[
        {'know_object': 1, 'target_object': 1, 'compromise_house': 0, 'observed': 0, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 1, 'target_object': 1, 'compromise_house': 0, 'observed': 1, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 1, 'target_object': 1, 'compromise_house': 1, 'observed': 0, 'motive': 0}] = [1, 0]
    bn.cpt("successful_stolen")[
        {'know_object': 1, 'target_object': 1, 'compromise_house': 1, 'observed': 1, 'motive': 0}] = [1, 0]

    return bn


def fill_cpts_common(bn):
    bn.cpt("know_object")[{}] = [0, 1]
    bn.cpt("target_object")[{'know_object': 1}] = [0.5, 0.5]
    bn.cpt("target_object")[{'know_object': 0}] = [1, 0]
    bn.cpt('motive')[{'know_object': 1, 'target_object': 1}] = [0, 1]
    bn.cpt('motive')[{'know_object': 0, 'target_object': 1}] = [1, 0]
    bn.cpt('motive')[{'know_object': 1, 'target_object': 0}] = [1, 0]
    bn.cpt('motive')[{'know_object': 0, 'target_object': 0}] = [1, 0]

    bn.cpt('compromise_house')[{'know_object': 1, 'target_object': 1, 'motive': 1}] = [0.75, 0.25]
    bn.cpt('compromise_house')[{'know_object': 0, 'target_object': 1, 'motive': 1}] = [1, 0]
    bn.cpt('compromise_house')[{'know_object': 1, 'target_object': 0, 'motive': 1}] = [1, 0]
    bn.cpt('compromise_house')[{'know_object': 0, 'target_object': 0, 'motive': 1}] = [1, 0]
    bn.cpt('compromise_house')[{'know_object': 1, 'target_object': 1, 'motive': 0}] = [1, 0]
    bn.cpt('compromise_house')[{'know_object': 0, 'target_object': 1, 'motive': 0}] = [1, 0]
    bn.cpt('compromise_house')[{'know_object': 1, 'target_object': 0, 'motive': 0}] = [1, 0]
    bn.cpt('compromise_house')[{'know_object': 0, 'target_object': 0, 'motive': 0}] = [1, 0]

    bn.cpt('observed')[{'know_object': 1, 'target_object': 1, 'compromise_house': 1, 'motive':1}] = [0.9, 0.1]
    bn.cpt('observed')[{'know_object': 1, 'target_object': 1, 'compromise_house': 0, 'motive':1}] = [1, 0]
    bn.cpt('observed')[{'know_object': 1, 'target_object': 0, 'compromise_house': 1, 'motive':1}] = [1, 0]
    bn.cpt('observed')[{'know_object': 1, 'target_object': 0, 'compromise_house': 0, 'motive':1}] = [1, 0]
    bn.cpt('observed')[{'know_object': 0, 'target_object': 1, 'compromise_house': 1, 'motive':1}] = [1, 0]
    bn.cpt('observed')[{'know_object': 0, 'target_object': 1, 'compromise_house': 0, 'motive':1}] = [1, 0]
    bn.cpt('observed')[{'know_object': 0, 'target_object': 0, 'compromise_house': 1, 'motive':1}] = [1, 0]
    bn.cpt('observed')[{'know_object': 0, 'target_object': 0, 'compromise_house': 0, 'motive':1}] = [1, 0]
    bn.cpt('observed')[{'know_object': 1, 'target_object': 1, 'compromise_house': 1, 'motive': 0}] = [1, 0]
    bn.cpt('observed')[{'know_object': 1, 'target_object': 1, 'compromise_house': 0, 'motive': 0}] = [1, 0]
    bn.cpt('observed')[{'know_object': 1, 'target_object': 0, 'compromise_house': 1, 'motive': 0}] = [1, 0]
    bn.cpt('observed')[{'know_object': 1, 'target_object': 0, 'compromise_house': 0, 'motive': 0}] = [1, 0]
    bn.cpt('observed')[{'know_object': 0, 'target_object': 1, 'compromise_house': 1, 'motive': 0}] = [1, 0]
    bn.cpt('observed')[{'know_object': 0, 'target_object': 1, 'compromise_house': 0, 'motive': 0}] = [1, 0]
    bn.cpt('observed')[{'know_object': 0, 'target_object': 0, 'compromise_house': 1, 'motive': 0}] = [1, 0]
    bn.cpt('observed')[{'know_object': 0, 'target_object': 0, 'compromise_house': 0, 'motive': 0}] = [1, 0]

    bn = do_stolen(bn)
    return bn

def get_temporal_ordering_nodes(experiment, global_state_csv):
    # determine the temporal order
    # consider only all temporal orders that include all events!
    max_score = 0
    # default ordering
    best_temporal_ordering = []
    header = next(csv.reader(open(global_state_csv)))

    for i in range(0, len(experiment.reporters.relevant_events)):
        best_temporal_ordering.append(i)  # default ordering is just [0, 1, ...]
        flag = "def"

    for key in experiment.reporters.temporal_dict.keys():
        #print(key, experiment.reporters.temporal_dict[key])
        #print(len(experiment.reporters.relevant_events) - len(experiment.reporters.evidence_list))
        #print(experiment.reporters.evidence_list)
        #print(experiment.reporters.temporal_list)
        #print(len(key))

        if len(key) == len(experiment.reporters.relevant_events) - len(experiment.reporters.evidence_list):
            if experiment.reporters.temporal_dict[key] > max_score:
                best_temporal_ordering = list(key)
                max_score = experiment.reporters.temporal_dict[key]
                flag = "cust"
    best_ordering_in_col_numbers_list = []
    #print(best_temporal_ordering)
    if flag == "cust":
        for item in best_temporal_ordering:
            best_ordering_in_col_numbers_list.append(header.index(item))
        for item in experiment.reporters.evidence_list:
            best_ordering_in_col_numbers_list.append(header.index(item))
    else:
        best_ordering_in_col_numbers_list = best_temporal_ordering
    print(flag)
    return best_ordering_in_col_numbers_list

def evidence_cannot_be_connected_to_each_other(temporal_ordering):
    #we know evidence is always added at the end
    forbidden_pairs = []
    evidence = temporal_ordering[-len(experiment.reporters.evidence_list):]  # we get column header idx
    for i in range(0, len(evidence)):
        for j in range(1, len(evidence) - i):
            forbidden_pairs.append((evidence[i], evidence[j+i]))
            forbidden_pairs.append((evidence[j+i], evidence[i]))

    return forbidden_pairs

def K2_BN(experiment):
    global_state_csv = "globalStates.csv"
    learner = gum.BNLearner(global_state_csv)  # using bn as template for variables and labels
    #learner.addMandatoryArc(0, 1)

    file_name = "BayesNets/K2BN.net"
    temporal_order = get_temporal_ordering_nodes(experiment, global_state_csv)
    forbidden = evidence_cannot_be_connected_to_each_other(temporal_order)
    for (a, b) in forbidden:
        learner.addForbiddenArc(a, b)
    #print(temporal_order)
    learner.useK2(temporal_order)
    bn = learner.learnBN()

    for name in experiment.reporters.relevant_events:
        x = bn.cpt(name)
        i = gum.Instantiation(x)
        i.setFirst()
        s = 0.0
        while (not i.end()):
            if 0.5 == x[i.todict()]:    # fix the never occurring situations -> maybe add an extra check for this TODO
                if i.todict()[name] == 0:
                    bn.cpt(name)[i.todict()] = 1
                elif i.todict()[name] == 1:
                    bn.cpt(name)[i.todict()] = 0
            i.inc()
        bn.cpt(name)



    gum.saveBN(bn, file_name)
    print(f"saved bn as {file_name}")
    return bn


### experiment with posterior outcomes
def get_posteriors_in_table(experiment):
    bnK2 = gum.loadBN("BayesNets/K2BN.net")
    ie = gum.LazyPropagation(bnK2)
    event_list = experiment.reporters.relevant_events
    evidence_list = []
    for ev in event_list:
        if ev[0] == 'E':    # evidence node TODO make a seperate class
            evidence_list.append(ev)
    print("\\begin{table}")
    print("\\begin{tabular}{c|c|c|c}")
    print("Evidence & Successful Stolen & Lost Object & Rest \\\\")
    print("\\hline")
    val = 1
    a = round(ie.posterior("successful_stolen")[1], 3)
    b = round(ie.posterior("lost_object")[1], 3)
    c = round(1 - a - b, 3)
    print(f" & {a} & {b} & {round(c, 3)} \\\\")
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
        print(f"{l_key} = {val} & {a} & {b} & {round(c, 3)} \\\\")
    print("\\end{tabular}")
    print("\\caption{Evidence set corresponding to scenario stealing. Outcome nodes.}")
    print("\\end{table}")

    print()
    ie = gum.LazyPropagation(bnK2)


    print("\\begin{table}")
    print("\\begin{tabular}{c|c|c|c|c|c|c|c}")
    print("Evidence & Raining & Curtains & Know O & Target O & Motive & Compromise H & Flees \\\\")
    print("\\hline")
    val = 1
    b1 = round(ie.posterior("raining")[1], 3)
    b2 = round(ie.posterior("curtains")[1], 3)
    b3 = round(ie.posterior("know_object")[1], 3)
    b4 = round(ie.posterior("target_object")[1], 3)
    b5 = round(ie.posterior("motive")[1], 3)
    b6 = round(ie.posterior("compromise_house")[1], 3)
    b7 = round(ie.posterior("flees_startled")[1], 3)
    print(f" & {b1} & {b2} &{b3} &{b4} &{b5} & {b6} & {b7}   \\\\")
    for evidence in evidence_list:
        if evidence != "E_private":
            val = 1
        else:
            val = 0
        ie.addEvidence(evidence, val)
        b1 = round(ie.posterior("raining")[1], 3)
        b2 = round(ie.posterior("curtains")[1], 3)
        b3 = round(ie.posterior("know_object")[1], 3)
        b4 = round(ie.posterior("target_object")[1], 3)
        b5 = round(ie.posterior("motive")[1], 3)
        b6 = round(ie.posterior("compromise_house")[1], 3)
        b7 = round(ie.posterior("flees_startled")[1], 3)
        l_key = evidence.replace("_", "\_")
        print(f" {l_key} = {val} & {b1} & {b2} &{b3} &{b4} &{b5} & {b6} & {b7}   \\\\")
    print("\\end{tabular}")
    print("\\caption{Evidence set corresponding to scenario stealing. Hypothesis nodes.}")
    print("\\end{table}")

    print()

    ie = gum.LazyPropagation(bnK2)

    print("\\begin{table}")
    print("\\begin{tabular}{c|c|c|c}")
    print("Evidence & Successful Stolen & Lost Object & Rest \\\\")
    print("\\hline")
    a = round(ie.posterior("successful_stolen")[1], 3)
    b = round(ie.posterior("lost_object")[1], 3)
    c = round(1 - a - b, 3)
    print(f" & {a} & {b} & {round(c, 3)} \\\\")
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
        print(f"{l_key} = {val} & {a} & {b} & {round(c, 3)} \\\\")
    print("\\end{tabular}")
    print("\\caption{Evidence set corresponding to lost scenario. Outcome nodes.}")
    print("\\end{table}")

    print()


    ie = gum.LazyPropagation(bnK2)

    print("\\begin{table}")
    print("\\begin{tabular}{c|c|c|c|c|c|c|c}")
    print("Evidence & Raining & Curtains & Know O & Target O & Motive & Compromise H & Flees \\\\")
    print("\\hline")
    val = 1
    b1 = round(ie.posterior("raining")[1], 3)
    b2 = round(ie.posterior("curtains")[1], 3)
    b3 = round(ie.posterior("know_object")[1], 3)
    b4 = round(ie.posterior("target_object")[1], 3)
    b5 = round(ie.posterior("motive")[1], 3)
    b6 = round(ie.posterior("compromise_house")[1], 3)
    b7 = round(ie.posterior("flees_startled")[1], 3)
    print(f" & {b1} & {b2} &{b3} &{b4} &{b5} & {b6} & {b7}   \\\\")
    for evidence in evidence_list:
        if evidence in ["E_object_is_gone"]:
            val = 1
        else:
            val = 0
        ie.addEvidence(evidence, val)
        b1 = round(ie.posterior("raining")[1], 3)
        b2 = round(ie.posterior("curtains")[1], 3)
        b3 = round(ie.posterior("know_object")[1], 3)
        b4 = round(ie.posterior("target_object")[1], 3)
        b5 = round(ie.posterior("motive")[1], 3)
        b6 = round(ie.posterior("compromise_house")[1], 3)
        b7 = round(ie.posterior("flees_startled")[1], 3)
        l_key = evidence.replace("_", "\_")
        print(f" {l_key} = {val} & {b1} & {b2} &{b3} &{b4} &{b5} & {b6} & {b7}  \\\\")
    print("\\end{tabular}")
    print("\\caption{Evidence set corresponding to lost scenario. Hypothesis nodes.}")
    print("\\end{table}")




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


def common_sense(experiment):
    file_name = "BayesNets/CommonBN.net"
    nodes = experiment.reporters.relevant_events
    bn = gum.BayesNet('CommonBN')
    bn = nodes_for_bn(bn, nodes)
    bn = links_for_bn(bn, nodes)
    bn = fill_cpts_common(bn)
    gum.saveBN(bn, file_name)
    print(f"saved bn as {file_name}")
    return bn

experiment = Experiment()
complex(experiment)
#rounded(experiment)
#common_sense(experiment)
K2_BN(experiment)
get_posteriors_in_table(experiment)
