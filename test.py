from src_code import generate_graphs
import matplotlib.pyplot as plt
import networkx as nx

G = generate_graphs.generate_connected_graph(6,0.6,3)[0]

nx.draw_networkx(G)
plt.show()