import csv
from matplotlib import pyplot as plt

unconstrained_AR = []

layer = 5
with open(f'results/MIS/unconstrained_QAOA{layer}.csv') as f:
# with open(f'results/MIS/customized/unconstrained_QAOA{layer}.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        unconstrained_AR += [float(row[-1])]

n1 = len(unconstrained_AR)
print(sum(unconstrained_AR)/n1)

feasible_AR = []
for ar in unconstrained_AR:
    if(ar < 1.01):
        feasible_AR += [ar]

n2 = len(feasible_AR)
print(sum(feasible_AR)/n2)
