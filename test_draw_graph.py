import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
import numpy as np
import matplotlib.pyplot as plt

n = 8
seed = 5
# graph_type = ['random', 0.5]
graph_type = ['random', 0.4]

G = generate_graphs.generate_graph_type(n, graph_type, seed)[0]

print(list(G.edges()))
pos = nx.spring_layout(G)
nx.draw(G)

plt.show()
