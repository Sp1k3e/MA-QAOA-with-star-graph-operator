from src_code import generate_graphs
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
edges = [(0, 1), (0, 3), (1, 2), (2, 3)]
G.add_edges_from(edges)


# 计算最大独立集
mis = nx.approximation.maximum_independent_set(G)
print("最大独立集:", mis, "解", len(mis))


pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
plt.show()