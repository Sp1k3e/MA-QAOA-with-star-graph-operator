import constrained_QAOA
from src_code import generate_graphs
import networkx as nx

no_vertices = 8
depth = 1
seed = 0

G = nx.Graph()
edge_list = [(0,1)]
edge_list = [(0,1), (1,2), (0,2)] #三角形
edge_list = [(0,1), (1,2), (2,3), (0,3)]
# edge_list = [(0,1), (1,2), (1,3)]
# edge_list = [(0,1), (1,2), (1,3), (3,4), (2,3)]
G.add_edges_from(edge_list)

# G = generate_graphs.generate_graph_type(8,['random', 0.5], 1)[0]

no_vertices = G.number_of_nodes()

constrained_QAOA.MIS_QAOA(no_vertices, depth, G)
