


file1 = open('BNVlekNetwork/kb1.net', 'r')
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

    print("Line{}: {}".format(count, line))
    proper.append(line)


with open('BNVlekNetwork/HUGINkb1.net', 'w') as file2:
  file2.writelines(proper)
