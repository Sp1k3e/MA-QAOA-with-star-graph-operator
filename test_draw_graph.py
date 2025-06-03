import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
import numpy as np
import matplotlib.pyplot as plt

n = 8
graph_type = ['random', 0.5]

G = generate_graphs.generate_graph_type(n, graph_type, 9)[0]

# pos = nx.spring_layout(G)
nx.draw(G)

plt.show()