import pandas as pd
org_dir + "/experiments/" + scenario
df = pd.read_csv(path + "/train/" + network_name + ".csv")

df.query()
df.filter(items=["stealing_1_0", "object_dropped_accidentally_0", "E_psych_report_1_0", "E_camera_1",
                 "E_camera_seen_stealing_1_0", "E_object_gone_0"])