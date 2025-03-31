import csv

"""
optimizer time and rounds
"""

star_rounds = []
star_time = []

MA_rounds = []
MA_time = []

MA2_rounds = []
MA2_time = []

QAOA3_rounds = []
QAOA3_time = []

with open(f'results/optimizer-consumption/tmp_star_graph.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        star_rounds += [float(row[-2])]
        star_time += [float(row[-1])]

with open(f'results/optimizer-consumption/tmp_MA.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        MA_rounds += [float(row[-2])]
        MA_time += [float(row[-1])]

with open(f'results/optimizer-consumption/tmp_MA2.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        MA2_rounds += [float(row[-2])]
        MA2_time += [float(row[-1])]

with open(f'results/optimizer-consumption/tmp_QAOA3.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        QAOA3_rounds += [float(row[-2])]
        QAOA3_time += [float(row[-1])]


print(sum(star_rounds)/len(star_rounds))
print(sum(star_time)/len(star_time))

print(sum(MA_rounds)/len(MA_rounds))
print(sum(MA_time)/len(MA_time))

print(sum(MA2_rounds)/len(MA2_rounds))
print(sum(MA2_time)/len(MA2_time))

print(sum(QAOA3_rounds)/len(QAOA3_rounds))
print(sum(QAOA3_time)/len(QAOA3_time))