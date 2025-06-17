filename = "12864_2007_1089_MOESM1_ESM.txt"

with open(filename) as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip()]
    for line in lines:
        print(line.split("||"))
