import networkx as nx
from src_code import generate_graphs
import matplotlib.pyplot as plt
from collections import Counter
import csv

MA2 = []

with open(f'results/MA-QAOA/MA-QAOA2.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if (row[2] == 'random0.5'):
            MA2 += [float(row[-1])]

fig, ax = plt.subplots()

bplot = ax.boxplot(MA2)
plt.show()