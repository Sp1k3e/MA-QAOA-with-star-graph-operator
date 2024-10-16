from src_code import generate_graphs
import matplotlib.pyplot as plt
import networkx as nx

no_vertices = 8
graph_type = ['random', 0.5]
seed = 1
graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]

nx.draw(graph)
plt.show()

sub_graph = graph.subgraph(8)

nx.draw(sub_graph)
plt.show()