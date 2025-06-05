import constrained_problem_QAOA
from src_code import generate_graphs
import networkx as nx
import numpy as np

np.set_printoptions(precision=3, suppress=True)

no_vertices = 8
depth = 1
seed = 0

G = nx.Graph()
edge_list = [(0,1)]
# edge_list = [(0,1), (0,2)] #三角形
# edge_list = [(0,1), (1,2), (0,2)] #三角形
# edge_list = [(0,1), (1,2), (1,3)] #正方形少一条边
# edge_list = [(0,1), (1,2), (2,3), (0,3)] #正方形
# edge_list = [(0,1), (1,2), (1,3), (3,4), (2,3)]
G.add_edges_from(edge_list)

# G = generate_graphs.generate_graph_type(8,['random', 0.5], 1)[0]

no_vertices = G.number_of_nodes()

#! partial mixer
# constrained_problem_QAOA.MIS_QAOA(no_vertices, depth, G, True)

#! unconstraned circuit
penalty_term = 1
penalty_term /= 2
constrained_problem_QAOA.MIS_QAOA(no_vertices, depth, G, False, penalty_term)
