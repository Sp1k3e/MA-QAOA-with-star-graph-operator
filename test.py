from src_code import generate_graphs
import matplotlib.pyplot as plt
import networkx as nx

# graph = generate_graphs.generate_graph_type(3,['random',0.4], 7)[0]

graph = nx.Graph()
edge_list = [(0,1), (1,2), (2,3)]

graph.add_edges_from(edge_list)
for index, edge in enumerate(graph.edges()):
    graph.get_edge_data(*edge)['weight'] = 1

nx.draw_networkx(graph)

plt.show()

