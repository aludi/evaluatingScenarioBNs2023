import csv
from collections import defaultdict

# TODO: make a box/case visualization
class CaseModel():
    def __init__(self, output_file):

        """f = "CredibilityGameOutcomes.csv"
        f = "StolenLaptopOutcomes.csv"""

        f = output_file

        with open(f) as csvf:
            freq_dict = defaultdict(int)
            r = csv.reader(csvf)
            header = next(r, None)
            for row in r:
                try:
                    freq_dict[tuple(row)] += 1
                except KeyError:
                    freq_dict[tuple(row)] = 0

        ## convert 0 and 1 into names
        name_dict = {}
        for key in sorted(freq_dict, key=freq_dict.get, reverse=True):
            #print(len(key))
            l = []
            for x in range(0,len(key)):
                if key[x] == '0':
                    w = "~"+header[x]
                else:
                    w = header[x]
                l.append(w)
            name_dict[key] = l
            print(name_dict[key], freq_dict[key])



        # create preference ordering
        prev_key = "no"
        prev_string = ""
        for key in sorted(freq_dict, key=freq_dict.get, reverse=True):

            if prev_key != "no":
                if freq_dict[key] < freq_dict[prev_key]:
                    prev_string = prev_string + " > "
                else:
                    prev_string = prev_string + " ~ "
            prev_string = prev_string + str(name_dict[key])
            prev_key = key

        print("CASE MODEL")
        print(prev_string)
        self.prev_string = prev_string


    def get_case_model(self):
        return self.prev_string

