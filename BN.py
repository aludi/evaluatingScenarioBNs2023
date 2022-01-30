from pylab import *
import matplotlib.pyplot as plt
import os
import pyAgrum as gum
from Experiment import Experiment
import pyAgrum.lib.image as gim



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

def nodes_for_bn(bn):
    nodes = ["know_object", "target_object","motive", "compromise_house", "observed", "successful_stolen"]
    for node in nodes:
        id = bn.add(gum.LabelizedVariable(node, node, 2))
    #x = bn.add(gum.LabelizedVariable("stolen", "stolen", ['successful', 'unsuccessful', 'no_stealing']))
    return bn

def links_for_bn(bn):
    nodes = ["know_object", "target_object", "motive", "compromise_house", "observed", "successful_stolen"]
    # lets do full bn
    for i in range(0, len(nodes)):
        for j in range(1, len(nodes)-i):
            bn.addArc(nodes[i], nodes[i+j])
    #for node in nodes:
    #    bn.addArc(node, "stolen")
    return bn



def fill_cpts(bn, exp):
    nodes = ["know_object", "target_object", "compromise_house", "observed", "motive", "successful_stolen"]    # same as Reporters

    list_ = [([], "know_object"),
             (["know_object"], "target_object"),
             (["know_object", "target_object", "motive"], "compromise_house"),
             (["know_object", "target_object"], "motive"),
             (["know_object", "target_object", "motive", "compromise_house"], "observed"),
             (["know_object", "target_object", "motive", "compromise_house", "observed"], "successful_stolen")]    # relevant relations (conditions, fully connected).


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
            bn.cpt(child)[item] = [(b/count), (a/count)]
        #print(bn.cpt(child))

    #bn = do_stolen(bn)
    #print(bn.cpt("stolen"))
    #exp.conditional_frequencies_dict([], "know_object")
    #exp.conditional_frequencies_dict(["know_object"], "target_object")

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
    nodes = ["know_object", "target_object", "motive", "compromise_house", "observed", "successful_stolen"]    # same as Reporters

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



def complex(experiment):
    file_name = "GodBN.net"
    bn = gum.BayesNet('GodBN')
    bn = nodes_for_bn(bn)
    bn = links_for_bn(bn)
    #bn = fill_cpts_random(bn)
    bn = fill_cpts(bn, experiment)
    #print(bn)
    gum.saveBN(bn, file_name)
    print(f"saved bn as {file_name}")

    return bn


def common_sense(experiment):
    file_name = "CommonBN.net"
    bn = gum.BayesNet('CommonBN')
    bn = nodes_for_bn(bn)
    bn = links_for_bn(bn)
    bn = fill_cpts_common(bn)
    #print(bn)
    gum.saveBN(bn, file_name)
    print(f"saved bn as {file_name}")

    return bn



experiment = Experiment()
complex(experiment)
common_sense(experiment)
