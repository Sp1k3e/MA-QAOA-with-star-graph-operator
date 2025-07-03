import constrained_problem_QAOA
import heuristic_MA
from src_code import generate_graphs
import networkx as nx
import numpy as np

np.set_printoptions(precision=3, suppress=True)

no_vertices = 8
depth = 1
seed = 1

G = nx.Graph()
edge_list = [(0,1)]
edge_list = [(0,1), (0,2)] #三角形少一条
# edge_list = [(0,1), (1,2), (0,2)] #三角形
# edge_list = [(0,1), (1,2), (1,3)] #正方形少一条边
# edge_list = [(0,1), (1,2), (2,3), (0,3)] #正方形
# edge_list = [(0,1), (1,2), (1,3), (3,4), (2,3)]
G.add_edges_from(edge_list)

# G = generate_graphs.generate_graph_type(no_vertices,['random', 0.5], seed)[0]
no_vertices = G.number_of_nodes()

#! other test
# alternatively appling different ansatz
depth = 1
initial_state = []
for i in range(3):
    initial_state = constrained_problem_QAOA.MIS_QAOA(G, depth, False, penalty_term=1, initial_state=initial_state)
    initial_state = initial_state / np.linalg.norm(initial_state)
    print(initial_state)
    initial_state = constrained_problem_QAOA.MIS_QAOA(G, depth, use_constrain_operator=True, initial_state=initial_state)
    initial_state = initial_state / np.linalg.norm(initial_state)