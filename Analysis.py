import pyAgrum as gum
import copy as copy
from Experiment import Experiment
from BN import K2_BN, K2_BN_csv_only
import csv
import pandas as pd
import math
import numpy as np
from collections import defaultdict
import csv
import random
import os
import matplotlib.pyplot as plt
import itertools
import shutil
from colour import Color
from CredibilityGame import CredibilityGame
from VlekNetwork import VlekNetwork



def hugin_converter(bnfilename, path):  # make the network handable in hugin with some cheats
    bn = path + "/BNs/"+bnfilename+".net"
    file1 = open(bn, 'r')
    Lines = file1.readlines()
    count = 0
    # Strips the newline character
    proper = []
    for line in Lines:
        count += 1
        flag = 0
        for x in ["unnamedBN;", "aGrUM 0.22.5", "node_size"]:
            if x in line:
                flag = 1

        if flag == 0:
            if "states = (0 1 );" in line:
                line = "states = (\"0\" \"1\");\n"
            elif "states = (1 0 );" in line:
                line = "states = (\"1\" \"0\");\n"
            #print("Line{}: {}".format(count, line))
            proper.append(line)

    #print(bnfilename)

    with open(path+"/huginBN/"+bnfilename+".net", 'w') as file2:
        file2.writelines(proper)


def calculate_world_states_accuracy(file_name, path, output_node):
    network = path + "/BNs/" + file_name + ".net"
    if "param" not in file_name and "map" not in file_name:
        csv_name = file_name.split("_", 1)[0]  # we want to refer to hte original csv file
    else:
        csv_name = file_name
    csv_file = path + "/train/" + csv_name + ".csv"
    if "net" not in network:
        network = network + ".net"
    bn = gum.loadBN(network)
    df = pd.read_csv(csv_file, sep=r',',
                     skipinitialspace=True)
    ddf = df.drop_duplicates()
    event_list = list(ddf.head())  # experiment.reporters.relevant_events
    n = file_name.split("_", 2)
    if len(n) > 1:
        [name, dist, val] = n
    else:
        name = n[0]
        dist = "none"
        val = 0

    possible_states = []
    impossible_states = []

    l = list(itertools.product([1, 0], repeat=len(event_list)))
    for item in l:
        a = np.array(item)
        #print(a)
        da = pd.DataFrame(np.expand_dims(a, axis=0), columns=list(ddf.head()))
        result = pd.concat([ddf, da]).shape[0] - pd.concat([ddf, da]).drop_duplicates().shape[0]
        #print(result)
        if result == 1:
            possible_states.append(item)
        else:
            impossible_states.append(item)

    output_ind = event_list.index(output_node)

    for state_list in [possible_states]:

        acc = 0
        rmq = 0
        bad_count = 0
        # print(network)

        list_for_rows = []
        x = ["precision", "names", "state", "posterior", "accuracy", "rmsq"]
        list_for_rows.append(x)


        if state_list == possible_states:
            state_name = "possibleStates"
        else:
            state_name = "impossibleStates"
        #print(state_name)

        print(event_list)
        for item in state_list:
            #print()
            ie = gum.LazyPropagation(bn)
            ie.addAllTargets()
            #print(item)

            #print(event_list[output_ind])
            for name in load_temporal_evidence(networks[:-4])["events"]:
                i = event_list.index(name)
                #ie.addAllTargets()
                if i != output_ind:


                    #print("\t", i, event_list[i], item[i])
                    try:
                        ie.addEvidence(event_list[i], item[i])
                        #ie.eraseTarget(event_list[i])
                        #ie.evidenceJointImpact(ie.targets(), {event_list[i]})
                        final_posterior = ie.posterior(event_list[output_ind])[1]
                        #ie.addTarget(event_list[i])
                        #ie.eraseEvidence(event_list[i])

                        #ie.addEvidence(event_list[i], item[i])
                        final_posterior = ie.posterior(event_list[output_ind])[1]
                        #print(final_posterior)

                    except:

                        final_posterior = "NA"
                        #print(f"network breaks!!  {file_name}")
                        break
            f = 0
            if final_posterior == "NA":
                #print("bad")
                acc += 0
                bad_count += 1
            else:
                #print("final posterior", final_posterior)
                #print("actual value", event_list[output_ind], item[output_ind])
                rmq += abs(int(item[output_ind]) - final_posterior)

                if int(round(final_posterior,0)) == int(item[output_ind]):
                    acc += 1
                    f = 1
                    #print("accuracy win")
                else:
                    acc += 0
                    f = 0
                    #print()
                    #print("accuracy loss")

            row = [val, event_list, item, final_posterior, f, abs(int(item[output_ind]) - final_posterior)]
            list_for_rows.append(row)
        with open(path + f"/stats/runs/{csv_name}_{state_name}_STATE_run_performance.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            for row in list_for_rows:
                writer.writerow(row)

        print(file_name)
        print(f"overall accuracy {acc/len(state_list)}")
        print(f"overall rmsq {rmq/len(state_list)}")
        print(f"overall inconsistent count {bad_count/len(state_list)}")


        row = [name, val, acc/len(state_list), rmq/len(state_list), bad_count/len(state_list)]

        with open(path + f"/stats/performance/{csv_name}_{state_name}_STATE_performance.csv", 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)

        print()


    print()




def load_temporal_evidence(name):
    # this should load a json dict that is written during the experiment
    d = {}
    #print(name)
    if "KB1" in name:
        d["events"] = ["jane_has_knife", "jane_and_mark_fight","jane_stabs_mark_with_knife"]
        d["values"] = [1, 1, 0]
        d["output"] = ["mark_dies"]

    elif "KB2" in name:
        d["events"] = ["jane_and_mark_fight", "jane_has_knife", "jane_threatens_mark_with_knife", "mark_hits_jane", "jane_drops_knife", "mark_falls_on_knife", "mark_dies_by_accident"]
        d["values"] = [1, 1, 1, 1, 1, 1, 0]
        d["output"] = ["mark_dies"]

    elif "KBFull" in name:
        d["events"] = ["jane_and_mark_fight", "jane_has_knife", "jane_stabs_mark_with_knife", \
        "jane_threatens_mark_with_knife", "mark_hits_jane", "jane_drops_knife", "mark_falls_on_knife", "mark_dies_by_accident"]
        d["values"] = [1, 1, 0, 1, 1, 1, 0, 0]
        d["output"] = ["mark_dies"]

    elif "StolenLaptop" in name:
        #"lost_object", "know_object", "target_object", "motive", "compromise_house",
           #                         "flees_startled", "successful_stolen", "raining", "curtains",
        if "Private" in name:
            d["events"] = ["E_object_is_gone",
                                    "E_broken_lock",
                                    "E_disturbed_house",
                                    "E_s_spotted_by_house",
                                    "E_s_spotted_with_goodie",
                                    ]
        else:
            d["events"] = ["E_object_is_gone",
                           "E_broken_lock",
                           "E_disturbed_house",
                           "E_s_spotted_by_house",
                           "E_s_spotted_with_goodie",
                           "E_private"]

        d["values"] = [1, 1, 1, 1, 1, 0]
        d["output"] = ["successful_stolen"]

    elif "GroteMarkt" in name:

        if "Private" in name:
            d["events"] = [
                "E_psych_report_1_0",
                "E_camera_1",
                "E_camera_seen_stealing_1_0",
                "E_object_gone_0"
            ]
            d["values"] = [
                1,
                1,
                1,
                1
                ]
            d["output"] = ["stealing_1_0", "object_dropped_accidentally_0"]

        else:
            d["events"] = [
                "E_valuable_1_0",
                "E_vulnerable_1_0",
                "E_psych_report_1_0",
                "E_camera_1",
                "E_sneak_1_0",
                "E_camera_seen_stealing_1_0",
                "E_object_gone_0"]
            d["values"] = [
                1,
                1,
                1,
                1,
                1,
                1,
                1]
            d["output"] = ["stealing_1_0", "object_dropped_accidentally_0"]

    elif "WalkThrough" in name:
        d["events"] = [
            "E_neighbor",
            "E_prints",
            "E_stab_wounds",
            "E_forensic"
        ]
        d["values"] = [
            1,
            1,
            1,
            1,
            ]
        d["output"] = ["mark_dies"]

    else:
        print("temporal evidence not implemented yet ")
        exit()

    return d



def progress_evidence(path, network_name, temporal_evidence):
    bn = gum.loadBN(path + "/BNs/" + network_name+".net")
    ie = gum.LazyPropagation(bn)



    x = []
    y_0 = []
    y_1 = []

    posterior_name = []

    #print(temporal_evidence)

    event = temporal_evidence["events"]
    val = temporal_evidence["values"]
    output_0 = temporal_evidence["output"][0]
    output_1 = temporal_evidence["output"][1]

    df = pd.read_csv(path + "/test/" + network_name + ".csv")

    #print(event)
    #print(list(df.columns))
    #print(event == list(df.columns))


    init_df_len = df.shape[0]
    df_s = df.query(f"{output_0} == {1}")
    df_a = df.query(f"{output_1} == {1}")
    df_r = df.query(f"{output_0} == {0} & {output_1} == {0}")
    #print(df.shape[0])
    '''
    if df.shape[0] > 0:
        print(df_s.shape[0] / df.shape[0], df_a.shape[0] / df.shape[0], df_r.shape[0] / df.shape[0], df.shape[0])
    else:
        print("state does not occur")
    '''
    x.append("No evidence")
    y_0.append(round(ie.posterior(output_0)[1], 2))
    y_1.append(round(ie.posterior(output_1)[1], 2))

    d_0 = []
    d_1 = []
    count = []

    if df.shape[0] > 0:
        d_0.append(round(df_s.shape[0] / df.shape[0], 2))
        d_1.append(round(df_a.shape[0] / df.shape[0], 2))
        count.append(df.shape[0])
    else:
        d_0.append(0)
        d_1.append(0)
        count.append(0)
        #print("state does not occur")


    posterior_name.append(output_0)

    i = 0
    for i in range(0, len(event)):
        #print(i, event[i], val[i])
        df = df.query(f"{event[i]} == {val[i]}")
        df_s = df_s.query(f"{event[i]} == {val[i]}")
        df_a = df_a.query(f"{event[i]} == {val[i]}")
        df_r = df_r.query(f"{event[i]} == {val[i]}")


        if df.shape[0] > 0:
            d_0.append(round(df_s.shape[0] / df.shape[0], 2))
            d_1.append(round(df_a.shape[0] / df.shape[0], 2))
            count.append(df.shape[0])

        else:
            d_0.append(0)
            d_1.append(0)
            count.append(0)

        #if df.shape[0] > 0:
        #    print(df_s.shape[0]/df.shape[0], df_a.shape[0]/df.shape[0],df_r.shape[0]/df.shape[0], df.shape[0] )
        #else:
        #    print("state does not occur")
        ie.addEvidence(event[i], val[i])
        x.append(str((event[i], val[i])))
        posterior_name.append(output_0)


        try:
            y_0.append(round(ie.posterior(output_0)[1], 2))
        except Exception:
            y_0.append(-1)

        try:
            y_1.append(round(ie.posterior(output_1)[1], 2))
        except Exception:
            y_1.append(-1)

            #y_1.append("NA")

    #print(y_0[-1], d_0[-1])
    #print(y_1[-1], d_1[-1])

    otp = {}
    otp["evidence"] = x
    otp[output_0] = y_0
    otp[output_1] = y_1
    otp[f"freq_{output_0}"] = d_0
    otp[f"freq_{output_1}"] = d_1
    otp["acc_0"] = abs(y_0[-1] - d_0[-1])
    otp["acc_1"] = abs(y_1[-1] - d_1[-1])
    otp["count"] = count[-1]/init_df_len

    #print(y_0)
    #print(y_1)

    otp["posterior_name"] = posterior_name
    otp_pd = pd.DataFrame.from_dict(otp)
    return otp_pd


def plot_evidence_posterior_base_network_only(path, base_network, df):

    flag = 0
    colors = ["#2037ba", "#b62a2a"]
    color_id = 0

    file = base_network
    param = file.split("_", 2)
    ax = plt.gca()

    if len(param) > 2:
        [base, dis, num] = param
        num = num[:-4]
        flag = 0
    else:
        base = file
        num = "network"
        flag = 1
    if flag == 1:
        df.rename(columns={"posterior": str(num)}, inplace=True)
        df.rename(columns={"freq_stealing_1_0": "F(steal)"}, inplace=True)
        df.rename(columns={"freq_object_dropped_accidentally_0":"F(dropped)"}, inplace=True)
        df.rename(columns={"stealing_1_0":"P(steal)"}, inplace=True)
        df.rename(columns={"object_dropped_accidentally_0":"P(dropped)"}, inplace=True)


        col = list(df.columns)

        N = 2
        ind = np.arange(N)  # the x locations for the groups
        width = 0.27

        df.plot(kind='bar', x = col[0], y=col[1:3], width=-0.2, align='edge', legend=True, title=base, ax=ax, stacked=True)
        df.plot(kind='bar', x = col[0], y=col[3:5], width=0.2, color=colors, align='edge', legend=True, title=base, ax=ax, stacked=True)

        plt.axhline(y=1, color='black', linestyle='-')
        plt.xticks(range(0, len(df["evidence"])), df["evidence"], rotation='vertical')
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(right=0.8, bottom=0.5)
        ax.legend(loc="best")
        plt.xlabel("Evidence added")
        plt.ylabel("Posterior probability")
        val = float(df["count"][0])
        #str_num = "{:.4f}".format(val*100)
        plt.title("The effect of evidence on the posterior ({val:.2f} % of runs)".format(val=val*100))

        file_name = path + "/plots/freq/evidence_progress_" + base_network + "_{val:.4f}".format(val=val*100) + ".pdf"
        #print(file_name)
        plt.savefig(file_name)
        #plt.show()
        plt.close()

    #print(df['acc_0'][0], df['acc_1'][0])

    return df['acc_0'][0], df['acc_1'][0], df["count"][0], df["evidence"]

def generate_dict(df, events):
    x = df[events]
    dict_output = x.iloc[len(x.index) - 1].to_dict()
    sum1 = 0
    for key in dict_output.keys():
        sum1 += dict_output[key]
    dict_output["neither"] = 1 - sum1
    return dict_output

def experiment_different_evidence(path, scn):

    nw = f"{path}/BNs/{scn}.net"

    folder_path = f"{path}/plots/freq/"
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)


    d = load_temporal_evidence(nw)
    i = 1
    df = pd.read_csv(path + "/test/" + scn + ".csv")

    values_list = df[d["events"]].drop_duplicates().values.tolist() # select all unique evidence states states

    a0 = []
    a1 = []
    c = []
    vl = []
    dict_val = {}
    dict_fre = {}
    dict_freq_val = {}

    freq = ["freq_stealing_1_0", "freq_object_dropped_accidentally_0"]

    for l in values_list:

        d["values"] = l
        temporal_evidence = d

        df = progress_evidence(path, scn, temporal_evidence)

        dict_output = generate_dict(df, d["output"])
        dict_freq = generate_dict(df, freq)

        #print(dict_output)


        ac0, ac1, count, e = plot_evidence_posterior_base_network_only(path, scn, df)
        #print(e)
        #print(count)
        a0.append(ac0)
        a1.append(ac1)
        c.append(count)
        i += 1
        vl.append(str(l))
        dict_val[tuple(l)] = dict_output
        dict_freq_val[tuple(l)] = dict_freq
    print_table_preference_ordering(dict_val)
    print_table_preference_ordering(dict_freq_val)


    file_name = path + "/plots/freqStates.pdf"
    plt.bar(vl, c, color="#2037ba")
    plt.xticks(rotation=20)
    plt.ylabel('frequency')
    plt.xlabel('number of runs')
    plt.title("Frequency of evidence states in simulation")
    #plt.show()
    plt.savefig(file_name)
    plt.close()
    return round(1 - sum(a0)/len(a0), 3), round(1 - sum(a1)/len(a1), 3)

def print_table_preference_ordering(dict_k):

    replaced_names = {}
    replaced_names["freq_stealing_1_0"] = "F(steal)"
    replaced_names["freq_object_dropped_accidentally_0"] = "F(dropped)"
    replaced_names["stealing_1_0"] = "P(steal)"
    replaced_names["object_dropped_accidentally_0"] = "P(dropped)"
    for k in dict_k.keys():
        if "freq_stealing_1_0" in list(dict_k[k].keys()):
            replaced_names["neither"] = "F(neither)"
            break
        else:
            replaced_names["neither"] = "P(neither)"




    print("\\begin{table}")
    print("\\begin{center}")
    str_tabular_formatting = "\\begin{tabular}{|l|c|c|c|}"
    print(str_tabular_formatting)
    print("\\hline")
    print("evidence & H1 & H2 & H3 \\\\")
    print("\\hline")
    for key in dict_k.keys():
        print(key, end="&")
        x = dict(sorted(dict_k[key].items(), key=lambda item:item[1], reverse=True))
        #print(x)

        val_order = 0
        for k in x.keys():
            print("{k} ({v:.2f})".format(k=replaced_names[k], v=x[k]), end=" ")
            #print(k, "("+ x[k] +")", end="  ")
            if k != list(x.keys())[-1]:
                if x[k] > val_order:
                    print("&", end= " ")
                    #print(" $>$ ", end=" ")
                else:
                    print("&", end=" ")
                    #print(" ~ ", end=" ")
                val_order = x[k]
            else:
                print("\\\\")
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{center}")
    print("\\caption{ }")
    print("\\label{ }")
    print("\\end{table}")

def print_latex_table_from_dict(dict_k):
    print(dict_k.keys())
    print("\\begin{table}")
    str_tabular_formatting = "\\begin{tabular}{l"
    for i in range(0, 3):
        str_tabular_formatting = str_tabular_formatting + "|c"
    str_tabular_formatting = str_tabular_formatting + "}"
    print(str_tabular_formatting)
    print("evidence & stealing\_1\_0 & object\_dropped\_accidentally\_0 & neither \\\\")
    for key in dict_k.keys():
        print(key, end='&')
        for k in dict_k[key].keys():
            if dict_k[key][k] >= 0:
                print("{val:.2f}".format(val=dict_k[key][k]), end='&')
            else:
                print("\\cellcolor{red} {val:.2f}".format(red="{RedOrange}", val=dict_k[key][k]), end='&')
        print("\\\\")
    print("\\end{tabular}")
    print("\\end{table}")





class Analysis():
    def __init__(self, scenario, output_nodes, org_dir, network_dir, train_test_split,  outcomes, test):
        # directories
        self.scenario = scenario
        self.output_nodes = output_nodes
        self.org_dir = org_dir
        self.network_dir = network_dir
        self.train_test_split = train_test_split
        self.runs = train_test_split[0]
        self.outcomes_csv = outcomes
        self.test_csv = test
        self.accuracy_csv = f"{scenario}Accuracy.csv"
        self.results = []
        self.networks = []
        self.outcome_experiment = None
        self.test_experiment = None



### intentions
#scenario = "CredibilityGame"
#scenario = "GroteMarkt"
#scenario = "StolenLaptop"
scenario = "VlekNetwork"
tr = 100
train_test_split = [tr, int(tr/10)]

runs = train_test_split[0]
test = train_test_split[1]

analysis = Analysis(scenario, [], os.getcwd(), None, train_test_split, None, None)

org_dir = os.getcwd()
csv_file_name = None

d_S = {"camera_vision":2}
d_V = {}
d_G = {"subtype":2, "map": org_dir+"/experiments/GroteMarkt/maps/groteMarkt.png"}

runs = [1, 5, 10, 20, 40, 60, 100, 200, 500, 1000]
for (scenario, train_runs, param_dict) in [ #("GroteMarkt", runs , d_G),
                                            ("GroteMarktPrivate", runs, d_G)
                                            ]:

    a_acc = []
    a_sto = []
    for num_runs in train_runs:
        os.chdir(org_dir)
        path = org_dir + "/experiments/" + scenario


        list_files = os.listdir(org_dir + "/experiments/" + scenario + "/train")
        list_files.sort()

        flag = 1
        it = 0
        while flag == 1 and it < 10:

            experiment = Experiment(scenario=scenario, runs=num_runs, train="train",
                                       param_dict=param_dict)  # we do the simple scenario

            #print("done with experiment")
            list_files = os.listdir(org_dir + "/experiments/" + scenario + "/train")
            list_files.sort()

            if ".DS_Store" in list_files:
                list_files.remove(".DS_Store")

            #print("List files", list_files)
            for train_data in list_files:
                if "pkl" in train_data:
                    continue
                flag = K2_BN_csv_only(train_data, path)
            it += 1

        print()
        print()
        print("TABLES FOR NUM RUNS    ", num_runs)

        if it >= 10 and flag == 1:
            a_acc.append(0)
            a_sto.append(0)

        else:


            disturbed_list_files = os.listdir(path + "/BNs")
            disturbed_list_files.sort()
            if ".DS_Store" in list_files:
                disturbed_list_files.remove(".DS_Store")
            disturbed_list_files = [scenario + ".net"]
            #print("disturbed files", disturbed_list_files)
            for networks in disturbed_list_files:
                if networks == ".DS_Store":
                    continue

                #print(networks)
                #
                k = networks.split("_", 2)
                if len(k) > 2:
                    [base, dist, num] = k
                    num = num[:-4]

                else:
                    dist = "none"
                    num = 0


                #print("hugin")
                #hugin_converter(networks[:-4], path)

                #print(networks[:-4])

                #print("progress")
                acc, stolen = experiment_different_evidence(path, networks[:-4])
                a_acc.append(acc)
                a_sto.append(stolen)



    file_name = path + "/plots/accuracy.pdf"

    ax = plt.gca()

    plt.plot(train_runs, a_sto, color="#2037ba", marker="o")
    plt.plot(train_runs, a_acc, color="#b62a2a", marker="o")

    plt.ylabel('accuracy')
    plt.xlabel('number of runs')
    plt.title("Accuracy of network")

    plt.savefig(file_name)
    #plt.show()
    plt.close()



exit()