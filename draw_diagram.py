import csv
import matplotlib.pyplot as plt

depth = 2
counts = 0
QAOA = 0
TR_QAOA = 0
TR_MA = 0
MA = 0
skip_seed = []

with open('results/QAOA/TR_QAOA.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')

    i = 0
    for row in csvreader:
        if row[-3] == str(depth):
            if str(i) != row[-2]:
                skip_seed += [str(i)]
                i += 1

            i += 1
            counts += 1
            TR_QAOA += float(row[-1])
print(f'skip seed {skip_seed}')    
    
with open('results/QAOA/QAOA.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    for row in csvreader:
        if row[-3] == str(depth):
            if row[-2] in skip_seed:
                continue

            QAOA += float(row[-1])

""" 
with open('results/MA-QAOA/TR_MA.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-2] in skip_seed:
            continue

        TR_MA += float(row[-1])

with open('results/MA-QAOA/MA-QAOA.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-2] in skip_seed:
            continue

        MA += float(row[-1])
 """

print(TR_QAOA)
print(QAOA)
# print(TR_MA)
# print(MA)