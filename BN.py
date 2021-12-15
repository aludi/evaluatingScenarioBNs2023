from pylab import *
import matplotlib.pyplot as plt
import os
import pyAgrum as gum
from Experiment import Experiment

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
    nodes = ["seen_object", "target_object", "compromise_house", "observed"]
    for node in nodes:
        id = bn.add(gum.LabelizedVariable(node, node, 2))
    x = bn.add(gum.LabelizedVariable("stolen", "stolen", ['successful', 'unsuccessful', 'no_stealing', 'weird']))
    return bn

def links_for_bn(bn):
    nodes = ["seen_object", "target_object", "compromise_house", "observed"]
    # lets do full bn
    for i in range(0, len(nodes)):
        for j in range(1, len(nodes)-i):
            bn.addArc(nodes[i], nodes[i+j])

    for node in nodes:
        bn.addArc(node, "stolen")

    return bn


def do_stolen(bn):
    bn.cpt("stolen")[{'seen_object': 0, 'target_object': 0, 'compromise_house': 0, 'observed': 0}] = [0, 0, 1, 0]
    bn.cpt("stolen")[{'seen_object': 0, 'target_object': 0, 'compromise_house': 0, 'observed': 1}] = [0, 0, 0, 1]
    bn.cpt("stolen")[{'seen_object': 0, 'target_object': 0, 'compromise_house': 1, 'observed': 0}] = [0, 0, 0, 1]
    bn.cpt("stolen")[{'seen_object': 0, 'target_object': 0, 'compromise_house': 1, 'observed': 1}] = [0, 0, 0, 1]

    bn.cpt("stolen")[{'seen_object': 0, 'target_object': 1, 'compromise_house': 0, 'observed': 0}] = [0, 0, 0, 1]
    bn.cpt("stolen")[{'seen_object': 0, 'target_object': 1, 'compromise_house': 0, 'observed': 1}] = [0, 0, 0, 1]
    bn.cpt("stolen")[{'seen_object': 0, 'target_object': 1, 'compromise_house': 1, 'observed': 0}] = [0, 0, 0, 1]
    bn.cpt("stolen")[{'seen_object': 0, 'target_object': 1, 'compromise_house': 1, 'observed': 1}] = [0, 0, 0, 1]

    bn.cpt("stolen")[{'seen_object': 1, 'target_object': 0, 'compromise_house': 0, 'observed': 0}] = [0, 0, 1, 0]
    bn.cpt("stolen")[{'seen_object': 1, 'target_object': 0, 'compromise_house': 0, 'observed': 1}] = [0, 0, 0, 1]
    bn.cpt("stolen")[{'seen_object': 1, 'target_object': 0, 'compromise_house': 1, 'observed': 0}] = [0, 0, 0, 1]
    bn.cpt("stolen")[{'seen_object': 1, 'target_object': 0, 'compromise_house': 1, 'observed': 1}] = [0, 0, 0, 1]

    bn.cpt("stolen")[{'seen_object': 1, 'target_object': 1, 'compromise_house': 0, 'observed': 0}] = [0, 1, 0, 0]
    bn.cpt("stolen")[{'seen_object': 1, 'target_object': 1, 'compromise_house': 0, 'observed': 1}] = [0, 1, 0, 0]
    bn.cpt("stolen")[{'seen_object': 1, 'target_object': 1, 'compromise_house': 1, 'observed': 0}] = [1, 0, 0, 0]
    bn.cpt("stolen")[{'seen_object': 1, 'target_object': 1, 'compromise_house': 1, 'observed': 1}] = [0, 1, 0, 0]

    return bn




def fill_cpts(bn, exp):
    nodes = ["seen_object", "target_object", "compromise_house", "observed"]

    list_ = [([], "seen_object"), (["seen_object"], "target_object"),
             (["seen_object", "target_object"], "compromise_house"),
             (["seen_object", "target_object", "compromise_house"], "observed")]


    for x in list_:
        parents, child = x
        cpt_table = exp.conditional_frequencies_dict(parents, child, 2)
        for item in cpt_table:
            tup = item.pop(child)
            count = item.pop("count")
            a, b = tup
            print(child, item, a, b, count)

            if count == 0:
                count = 1   # TODO: HAAAACK FRAUD
                a = 0
                b = 0
            bn.cpt(child)[item] = [(b/count), (a/count)]
        print(bn.cpt(child))

    bn = do_stolen(bn)

    #exp.conditional_frequencies_dict([], "seen_object")
    #exp.conditional_frequencies_dict(["seen_object"], "target_object")

    bn.generateCPT("stolen")    # random for now, don't want to bother with frequencies rm

    return bn

def fill_cpts_random(bn):
    for node in bn.nodes():
        bn.generateCPT(node)
        print(bn.cpt(node))
    return bn

def complex():
    experiment = Experiment()
    bn = gum.BayesNet('Test')
    bn = nodes_for_bn(bn)
    bn = links_for_bn(bn)
    bn = fill_cpts(bn, experiment)
    #bn = fill_cpts_random(bn)
    print(bn)
    return bn

bn = complex()
print("saved bn as Test.net")
gum.saveBN(bn, "Test.net")

