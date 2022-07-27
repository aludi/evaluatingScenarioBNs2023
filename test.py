import random
import pandas as pd
from itertools import combinations, product


'''count = 0
max = 1000000
for i in range(0, max):
    object_val = random.randint(60, 90)  # super tempting target
    risk_t = random.randint(50, 100)  # steals sometimes
    if object_val > risk_t:
        count += 1

print(count/max)'''


file_path = "experiments/GroteMarktPrivate/test/GroteMarktPrivate.csv"
df = pd.read_csv(file_path)
all_ev = ["E_psych_report_1_0", "E_camera_1", "E_camera_seen_stealing_1_0", "E_object_gone_0"]
com = [["E_psych_report_1_0"], ["E_camera_1"], ["E_camera_seen_stealing_1_0"], ["E_object_gone_0"]]
for i in range(2, len(all_ev) + 1):
    for item in combinations(all_ev, i):
        com.append(list(item))

min_steal = -1
min_drop = -1


for x in com:
    print(x)
    val = list(product([0, 1], repeat=len(x)))
    for t in val:
        s = f""
        for i in range(0, len(x)):
            # create query
            s += f"{x[i]} == {t[i]} &"
        print(s)
        y = df.query(s[:-1])  # remove trailing &
        steal = y["stealing_1_0"].mean()
        drop = y["object_dropped_accidentally_0"].mean()

        if steal == 1:
            print("\t minimal set steal : ", s[:-1])
            min_steal = s[:-1]
        if drop == 1:
            print("\t minimal set drop : ", s[:-1])
            min_drop = s[:-1]
        if steal == 0 and drop == 0:
            print("\t minimal set nothing : ", s[:-1])
            min_none = s[:-1]