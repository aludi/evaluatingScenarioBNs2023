from pylab import *
import matplotlib.pyplot as plt
import os
import pyAgrum as gum
import copy as copy
from Experiment import Experiment
import csv
import pandas as pd
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


    for i in range(0, len(header)):
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

def evidence_cannot_be_connected_to_each_other(temporal_ordering):
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
            #pass

    return forbidden_pairs

def K2_BN(experiment, csv_file, name):
    global_state_csv = csv_file #"globalStates.csv"
    learner = gum.BNLearner(global_state_csv)  # using bn as template for variables and labels
    file_name = name #"BayesNets/K2BN.net"
    temporal_order = get_temporal_ordering_nodes(experiment, global_state_csv)
    if name != "BayesNets/adaptedK2BN.net":
        forbidden = evidence_cannot_be_connected_to_each_other(temporal_order)
        for (a, b) in forbidden:
            learner.addForbiddenArc(a, b)
    #print(temporal_order)
    learner.useK2(temporal_order)
    bn = learner.learnBN()
    header = next(csv.reader(open(global_state_csv)))
    for name in list(header):
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
    #print(f"saved bn as {file_name}")
    return bn

def disturb_cpts(experiment, disturb_type, params_list):
    file_name = "noiseBN.net"
    K2_BN(experiment, "globalStates.csv", file_name)

    bn = gum.loadBN(file_name)
    noise_list = []

    if disturb_type == "NORMAL_NOISE":

        '''
        The probabilities in the cpt are not the probabilities generated by K2,
        but they're distorted by a noise error (e)
            X'(X=1) = X(X=1) - e
            X'(X=0) = X(X=0) + e    (or vice versa)

        where e is drawn from a truncatec normal distribution with 
        M = 0, SD = 0.2 (tune parameters later) - the distribution cannot be o . For
        every variable we draw again from this normal distribution.
        
        This might represent the best case scenario for human estimations
        of probability - even if we cannot know the exact probability,
        we might be able to estimate them closely enough.
        
        However, it is very likely that our probability estimations
        do not work according to this standard-noise model. For instance,
        racial (or other societal) biases cannot be assumed to 
        be modelled with a "normal" divergence (the noise will be
        predisposed to go into "one direction", and not the other).
        
        However, first we need to see if BNs are robust against this 
        most simple noise-type of error.
        
        '''
        m, sd, type = params_list
        smallest_change = 1
        largest_change = 0
        nodes = bn.nodes() # list of nodes to iterate over (names don't matter because noise is all the same
        for node in list(nodes):
            x = bn.cpt(node)
            name = x.var_names[-1]
            e = np.random.normal(loc=m, scale=sd)
            noise_list.append(e)
            #print(name, e)
            for i in bn.cpt(name).loopIn():
                if i.todict()[name] == 0:
                    bn.cpt(name).set(i, keep_in_range(bn.cpt(name).get(i) + e))
                elif i.todict()[name] == 1:
                    bn.cpt(name).set(i, keep_in_range(bn.cpt(name).get(i) - e))

            if abs(e) > largest_change:
                largest_change = abs(e)
            if abs(e) < smallest_change:
                smallest_change = abs(e)
        #print(largest_change, smallest_change)
        gum.saveBN(bn, "noiseBN.net")
        #print(f"saved bn as {file_name}")
        return [largest_change, smallest_change]

    if disturb_type == "ROUNDED":
        ''' we want to round the BN
        to some degree of decimals,
        since humans are not really accurate at 0.0001
        estimations.
        So then we want to get to 0.1, or 0.01 level rounding  (params_list)
        in the network, to see what happens then.
        '''
        [decimal_place, rounded_name] = params_list
        nodes = bn.nodes()  # list of nodes to iterate over (names don't matter because noise is all the same
        for node in list(nodes):
            x = bn.cpt(node)
            name = x.var_names[-1]
            for i in bn.cpt(name).loopIn():
                bn.cpt(name).set(i, round(bn.cpt(name).get(i), decimal_place))
        gum.saveBN(bn, "roundedBN.net")
        return ["empty"]

    if disturb_type == "ARBROUNDED":
        ''' we want to round the BN
        to some degree (round to quartile, octile, thirds, 2nds, hwatever,
        since we like round numbers
        
        '''
        [step, rounded_name] = params_list

        nodes = bn.nodes()  # list of nodes to iterate over (names don't matter because noise is all the same
        for node in list(nodes):
            x = bn.cpt(node)
            name = x.var_names[-1]
            for i in bn.cpt(name).loopIn():
                val = bn.cpt(name).get(i)
                val = val
                y = math.floor((val/step) + 0.5) * step
                bn.cpt(name).set(i, y)
        gum.saveBN(bn, f"ARBRoundedBN{str(step*100)}.net")
        return ["empty"]

def direction(file_name):
    bn = gum.loadBN(file_name)
    direction_dict = {}
    ie = gum.LazyPropagation(bn)
    event_list = experiment.reporters.relevant_events
    e_dict = {}

    for node in list(bn.nodes()):
        x = bn.cpt(node)
        name = x.var_names[-1]
        if name[0] != 'E':  # we do not care about evidence nodes
            # print(ie.posterior(node))
            node_false_val = ie.posterior(node)[0]
            node_true_val = ie.posterior(node)[1]  # always binary
            if node_false_val > node_true_val:
                e_dict[name] = "H0"
            elif node_false_val < node_true_val:
                e_dict[name] = "H1"
            else:
                e_dict[name] = "0"
            # print(direction_dict[name])
    direction_dict[("no_evidence", 0)] = e_dict


    evidence_list = []
    for ev in event_list:
        if ev[0] == 'E':  # evidence node TODO make a seperate class
            evidence_list.append(ev)

    for evidence in evidence_list:
        e_dict = {}
        if evidence != "E_private":
            val = 1
        else:
            val = 0
        ie.addEvidence(evidence, val)

        for node in list(bn.nodes()):
            x = bn.cpt(node)
            name = x.var_names[-1]
            if name[0] != 'E':  # we do not care about evidence nodes
                #print(ie.posterior(node))
                try:
                    node_false_val = ie.posterior(node)[0]
                    node_true_val = ie.posterior(node)[1]   # always binary
                    if node_false_val > node_true_val:
                        e_dict[name] = "H0"
                    elif node_false_val < node_true_val:
                        e_dict[name] = "H1"
                    else:
                        e_dict[name] = "0"
                except:
                    e_dict[name] = "N/A"
                #print(direction_dict[name])
        direction_dict[(evidence, val)] = e_dict

    return direction_dict

def comp(d1, d2, latex_file_name, params):   # compare two direction dictionaries
    h = []
    for e in d1.keys():
        for x in d1[e].keys():

            pass
            #print(e, x, d1[e][x], d2[e][x], d1[e][x] == d2[e][x])

    with open(latex_file_name, 'w') as file:
        file.write("\\begin{table}")
        file.write("\\begin{tabular}{c|cc|cc}")
        file.write("\\toprule")
        file.write("\\multirow{2}{*}{Evidence} & \\multicolumn{2}{c}{Successful Stolen} & \\multicolumn{2}{c}{Lost Object} \\\\"
                   "& {K2} & {Dev} & {K2} & {Dev} \\\\")
        file.write("\\midrule\n")
        for e in d1.keys():
            l_key = e[0].replace("_", "\_")
            file.write(str(l_key) + ", " + str(e[1]) + " & ")
            for x in ["successful_stolen", "lost_object"]:
                if d1[e][x] == d2[e][x]:
                    file.write(d1[e][x] + "&" + d2[e][x])
                else:
                    file.write("\\cellcolor{Bittersweet}" + d1[e][x] + "&" + "\\cellcolor{Bittersweet}" + d2[e][x])
                if x == "successful_stolen":
                    file.write("&")
            file.write("\\\\")

        file.write("\\bottomrule")
        file.write("\\end{tabular}")
        file.write("\\caption{Different outcomes for disturbances in the cpts with params " + str(params) + "}")
        file.write("\\end{table}")

def comp_count(d1, d_noise, latex_file_name, params):   # compare two direction dictionaries
    h = []
    for e in d1.keys():
        for x in d1[e].keys():

            pass
            #print(e, x, d1[e][x], d2[e][x], d1[e][x] == d2[e][x])

    with open(latex_file_name, 'w') as file:
        file.write("\\begin{table}")
        file.write("\\begin{tabular}{c|cc|cc}")
        file.write("\\toprule")
        file.write("\\multirow{2}{*}{Evidence} & \\multicolumn{2}{c}{Successful Stolen} & \\multicolumn{2}{c}{Lost Object} \\\\"
                   "& {K2} & {Noise} & {K2} & {Noise} \\\\")
        file.write("\\midrule\n")
        for e in d1.keys():
            l_key = e[0].replace("_", "\_")
            file.write(str(l_key) + ", " + str(e[1]) + " & ")
            for x in ["successful_stolen", "lost_object"]:
                count = 0
                for d2 in d_noise:
                    if d1[e][x] == d2[e][x]:
                        count += 1
                if (count/len(d_noise)) < 0.95:
                    file.write("\\cellcolor{Bittersweet}" + d1[e][x] + "&" + "\\cellcolor{Bittersweet}" + str(round(100*(count/len(d_noise)), 0)))
                else:
                    file.write(d1[e][x] + "&" + str(round(100*(count/len(d_noise)), 0)))
                if x == "successful_stolen":
                    file.write("&")
            file.write("\\\\")

        file.write("\\bottomrule")
        file.write("\\end{tabular}")
        file.write("\\caption{Different outcomes for disturbances in the cpts with params " + str(params) + "}")
        file.write("\\end{table}")


def keep_in_range(x):
    ''' numbers in a ctp cannot be > 1 or < 0'''
    if x > 1:
        return 1
    if x < 0:
        return 0
    return x


def K2_limited_BN(experiment):
    temp_global_state_csv = "globalStates.csv"
    d = pd.read_csv(temp_global_state_csv)
    for x in experiment.reporters.relevant_events:
        if x not in ["successful_stolen", "lost_object"]:
            #print(x[0])
            if x[0] != "E":
                d.pop(x)
    d.to_csv("partialStates.csv", index=False)
    K2_BN(experiment, "partialStates.csv", "BayesNets/adaptedK2BN.net")


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


def get_hypothesis_posteriors_in_table(experiment, file_name, d1, d2, latex_file_name, params):
    bnK2 = gum.loadBN(file_name)
    ie = gum.LazyPropagation(bnK2)
    event_list = experiment.reporters.relevant_events
    evidence_list = []
    for ev in event_list:
        if ev[0] == 'E':  # evidence node TODO make a seperate class
            evidence_list.append(ev)

    ie = gum.LazyPropagation(bnK2)



    with open(latex_file_name, 'w') as file:

        file.write("\\begin{table}")
        file.write("\\begin{tabular}{c|cc|cc|cc|cc|cc|cc|cc}")

        file.write("\\toprule")
        file.write("\\multirow{2}{*}{Evidence} & \\multicolumn{2}{c}{Raining} & "
                   "\\multicolumn{2}{c}{Curtains} & \\multicolumn{2}{c}{Know O}"
                   " & \\multicolumn{2}{c}{Target O} & \\multicolumn{2}{c}{Motive} &"
                   " \\multicolumn{2}{c}{CH} & \\multicolumn{2}{c}{Flees} &"
                   "  & {K2} & {Dev} & {K2} & {Dev} & {K2} & {Dev} & {K2} & {Dev} &"
                   " {K2} & {Dev} & {K2} & {Dev} & {K2} & {Dev}\\\\")
        file.write("\\midrule\n")

        for e in d1.keys():
            l_key = e[0].replace("_", "\_")
            file.write(str(l_key) + ", " + str(e[1]) + " & ")
            for x in ["curtains", "raining", "know_object",
                      "target_object", "motive", "compromise_house",
                      "flees_startled"]:
                if d1[e][x] == d2[e][x]:
                    file.write(d1[e][x] + "&" + d2[e][x])
                else:
                    file.write("\\cellcolor{Bittersweet}" + d1[e][x] + "&" + "\\cellcolor{Bittersweet}" + d2[e][x])
                if x != "flees_startled":
                    file.write("&")
            file.write("\\\\")
        file.write("\\bottomrule")
        file.write("\\end{tabular}")
        file.write("\\caption{Evidence set with effect on hypothesis nodes." + str(params) + "}")
        file.write("\\end{table}")

        '''    
        val = 1
        b1 = round(ie.posterior("raining")[1], 3)
        b2 = round(ie.posterior("curtains")[1], 3)
        b3 = round(ie.posterior("know_object")[1], 3)
        b4 = round(ie.posterior("target_object")[1], 3)
        b5 = round(ie.posterior("motive")[1], 3)
        b6 = round(ie.posterior("compromise_house")[1], 3)
        b7 = round(ie.posterior("flees_startled")[1], 3)
        file.write(f" & {b1} & {b2} &{b3} &{b4} &{b5} & {b6} & {b7}   \\\\")
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
            file.write(f" {l_key} = {val} & {b1} & {b2} &{b3} &{b4} &{b5} & {b6} & {b7}   \\\\")
        file.write("\\end{tabular}")
        file.write("\\caption{Evidence set corresponding to scenario stealing. Hypothesis nodes.}")
        file.write("\\end{table}")

        file.write("\n")
        ie = gum.LazyPropagation(bnK2)

        file.write("\\begin{table}")
        file.write("\\begin{tabular}{c|c|c|c|c|c|c|c}")
        file.write("Evidence & Raining & Curtains & Know O & Target O & Motive & Compromise H & Flees \\\\")
        file.write("\\hline")
        val = 1
        b1 = round(ie.posterior("raining")[1], 3)
        b2 = round(ie.posterior("curtains")[1], 3)
        b3 = round(ie.posterior("know_object")[1], 3)
        b4 = round(ie.posterior("target_object")[1], 3)
        b5 = round(ie.posterior("motive")[1], 3)
        b6 = round(ie.posterior("compromise_house")[1], 3)
        b7 = round(ie.posterior("flees_startled")[1], 3)
        file.write(f" & {b1} & {b2} &{b3} &{b4} &{b5} & {b6} & {b7}   \\\\")
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
            file.write(f" {l_key} = {val} & {b1} & {b2} &{b3} &{b4} &{b5} & {b6} & {b7}  \\\\")
            '''



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

def experiment_with_normal_noise():
    for params in [[0, 0.001, "Normal (M, sd)"], [0, 0.01, "Normal (M, sd)"], [0, 0.1, "Normal (M, sd)"],
                   [0, 0.2, "Normal (M, sd)"], [0, 0.3, "Normal (M, sd)"], [0, 0.5, "Normal (M, sd)"]]:
        d_noise_list = []
        smallest_change = 1
        largest_change = 0
        for i in range(0, 200):
            [l, s] = disturb_cpts(experiment, "NORMAL_NOISE", params)
            if abs(l) > largest_change:
                largest_change = l
            if abs(s) < smallest_change:
                smallest_change = s
            d_1 = direction("BayesNets/K2BN.net")
            d_2 = direction("noiseBN.net")
            d_noise_list.append(d_2)
        print(params, largest_change, smallest_change)
        comp_count(d_1, d_noise_list, f'texTables/diffOutcomes{params[1]}.tex', params)
        # comp(d_1, d_2, f'texTables/diffOutcomes{params[1]}.tex', params)
        print("generated 1x table for ", params)

def experiment_with_rounding():
    for params in [[5, 'decimal places'], [4, 'decimal places'], [3, 'decimal places'],
                   [2, 'decimal places'], [1, 'decimal places'], [0, 'decimal places']]:
        [empty] = disturb_cpts(experiment, "ROUNDED", params)
        d_1 = direction("BayesNets/K2BN.net")
        d_2 = direction("roundedBN.net")
        comp(d_1, d_2, f'texTables/diffOutcomesROUNDED{params[0]}.tex', params)
        get_hypothesis_posteriors_in_table(experiment, "BayesNets/K2BN.net", d_1, d_2, f'texTables/diffOutcomesROUNDEDHYPS{params[0]}.tex', params)

        #print("generated 1x table for ", params)

def experiment_with_arbitrary_rounding():
    for params in [[0.05, 'arbit'], [0.1, 'arbit'], [0.125, 'arbit'],
                   [0.2, 'arbit'], [0.25, 'arbit'],[0.33, 'arbit'],
                   [0.5, 'arbit']]:
        [empty] = disturb_cpts(experiment, "ARBROUNDED", params)
        d_1 = direction("BayesNets/K2BN.net")
        d_2 = direction(f"ARBRoundedBN{str(params[0]*100)}.net")
        comp(d_1, d_2, f'texTables/diffOutcomesARBROUNDED{params[0]}.tex', params)
        get_hypothesis_posteriors_in_table(experiment, "BayesNets/K2BN.net", d_1, d_2, f'texTables/diffOutcomesARBROUNDEDHYPS{params[0]}.tex', params)
        #print("generated 1x table for ", params)



np.random.seed(1)
experiment = Experiment()
K2_BN(experiment, "globalStates.csv", "BayesNets/K2BN.net")
experiment_with_rounding()
experiment_with_arbitrary_rounding()


get_outcome_posteriors_in_table(experiment, "BayesNets/K2BN.net", "postK2BN.tex", None)
get_outcome_posteriors_in_table(experiment, "ARBRoundedBN33.0.net", "postarb.tex", None)
get_diff_outcome_posteriors_in_table(experiment, "BayesNets/K2BN.net", "ARBRoundedBN33.0.net", ["stolen", "lost"])



#K2_limited_BN(experiment)
#et_diff_outcome_posteriors_in_table(experiment, "BayesNets/K2BN.net", "BayesNets/adaptedK2BN.net", ["stolen", "lost"])

#get_outcome_posteriors_in_table(experiment, "BayesNets/K2BN.net")
#get_outcome_posteriors_in_table(experiment, "BayesNets/adaptedK2BN.net")
