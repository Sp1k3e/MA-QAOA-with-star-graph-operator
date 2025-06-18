import constrained_problem_QAOA
import heuristic_MA
from src_code import generate_graphs
import networkx as nx
import numpy as np

np.set_printoptions(precision=3, suppress=True)

no_vertices = 8
depth = 1
seed = 0

G = nx.Graph()
# edge_list = [(0,1)]
# edge_list = [(0,1), (0,2)] #三角形少一条边
edge_list = [(0,1), (1,2), (0,2)] #三角形
# edge_list = [(0,1), (1,2), (1,3)] #正方形少一条边
# edge_list = [(0,1), (1,2), (2,3), (0,3)] #正方形
# edge_list = [(0,1), (1,2), (1,3), (3,4), (2,3)]
G.add_edges_from(edge_list)
no_vertices = G.number_of_nodes()

# G = generate_graphs.generate_graph_type(no_vertices,['random', 0.5], seed)[0]

#! custom phase operator
custom_phase_operator = G
# custom_phase_operator = G.remove_edge(0,2)


#! partial mixer
# constrained_problem_QAOA.MIS_QAOA(no_vertices, depth, G, use_constrain_operator=True, custom_phase_operator=custom_phase_operator)


#! unconstraned circuit
penalty_term = 1
constrained_problem_QAOA.MIS_QAOA(no_vertices, depth, G, False, penalty_term/2)


#! MA
# heuristic_MA.star_graph_MA_MIS(G, 'specific', 0, 1)