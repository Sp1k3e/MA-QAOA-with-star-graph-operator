from src_code import generate_graphs
import matplotlib.pyplot as plt
import networkx

no_vertices = 8
seed = 1
p = 0.4
# graph = generate_graphs.generate_connected_graph(no_vertices, seed)[0]
graph = generate_graphs.generate_connected_graph(no_vertices, seed, p)[0]

pos=networkx.circular_layout(graph)
networkx.draw_networkx(graph, pos)
plt.show()