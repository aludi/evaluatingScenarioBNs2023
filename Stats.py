import pandas as pd
import matplotlib as plt
import os
import random
import pyAgrum as gum

def calculate_accuracy(network, csv_file):
    '''print(network)
    print(orgDir)
    print(bnDir)
    print(os.getcwd())'''
    print(network)

    if "net" not in network:
        network = network + ".net"

    #org_dir = orgDir
    #if dir not in os.getcwd():

    bn = gum.loadBN(network)

    # todo: set evidence
    # see value of output
    # if the same +1, else +0
    # then calcualte accuracy
    # store D in some other array

    direction_dict = {}


    '''evidence = []
    for x in event_list:
        if x[0] == "E": # evidence node
            evidence.append(x)
'''


    df = pd.read_csv(csv_file, sep=r',',
            skipinitialspace = True)

    print(df.columns)

    accuracy = 0
    rmsd = 0
    #print(output_nodes)
    network_name = []
    pred_output=[]
    matching_output=[]
    rms_list=[]
    input_list = []
    output_list = []
    for i in range(0, int(len(df)/10)):
        print("NEW COMBO")
        event_list = list(bn.names())  # experiment.reporters.relevant_events
        random.shuffle(event_list)
        output_node = event_list.pop()

        ie = gum.LazyPropagation(bn)
        k = []
        print("going over set nodes")
        for ev in event_list:
            val = df.loc[i, ev]
            print("\t", ev, int(val))
            ie.addEvidence(ev, int(val))
            k.append(val)

        print("output according to csv")
        val_output = df.loc[i, output_node]
        print("\t", output_node, val_output)
        output_list.append(val_output)
        #print("output actual",val_output)
        try:
            print("output according to network")
            fin = round(ie.posterior(output_node)[1], 2)
            print("\t", output_node, fin)
            rmsd += round(abs(fin - val_output), 2)
            rms_list.append(round(abs(fin - val_output), 2))

        except:
            fin = "NA"
            rmsd += 1
            rms_list.append(1)

        if fin == val_output:
            accuracy += 1
            matching_output.append(1)
        else:
            matching_output.append(0)

            pass

            pred_output.append(fin)
            network_name.append(network)
            input_list.append(k)

    otp = {}
    otp["network"] = network_name
    otp["input"] = input_list
    otp["output"] = output_list
    otp["predicted"] = pred_output
    otp["matching"] = matching_output
    otp["RMS"] = rms_list
    #otp_pd = pd.DataFrame.from_dict(otp)

    print("accuracy", accuracy/int(len(df)/10))
    print("root mean swuare", rmsd/int(len(df)/10))

    print(otp)

calculate_accuracy("BNVlekNetwork/kb1.net", "VlekOutcomesKB1.csv")
