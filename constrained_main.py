import constrained_problem_QAOA
import heuristic_MA
from src_code import generate_graphs
import networkx as nx
import numpy as np

np.set_printoptions(precision=3, suppress=True)

no_vertices = 8
depth = 2
seed = 0

G = nx.Graph()
edge_list = [(0,1)]
# edge_list = [(0,1), (0,2)] #三角形少一条边
edge_list = [(0,1), (1,2), (0,2)] #三角形
# edge_list = [(0,1), (1,2), (1,3)] #正方形少一条边
edge_list = [(0,1), (1,2), (2,3), (0,3)] #正方形
# edge_list = [(0,1), (1,2), (1,3), (3,4), (2,3)]
G.add_edges_from(edge_list)

G = generate_graphs.generate_graph_type(no_vertices,['random', 0.5], seed)[0]
no_vertices = G.number_of_nodes()

#! custom phase operator
custom_phase_operator = G.copy()
# custom_phase_operator.remove_edge(0,2)
# custom_phase_operator.add_edge(1,2)
# print(G)

#! partial mixer
initial_state = [0b010]
initial_vector = np.zeros(2**no_vertices)
for i in initial_state:
    initial_vector[i] = 1
initial_vector = initial_vector/np.linalg.norm(initial_vector)

initial_vector = None
# constrained_problem_QAOA.MIS_QAOA(G, depth, use_constrain_operator=True, initial_state=initial_vector, custom_phase_operator=custom_phase_operator)

#! unconstraned circuit
penalty_term = 2
constrained_problem_QAOA.MIS_QAOA(G, depth, False, penalty_term/2, custom_phase_operator=custom_phase_operator)


#! MA
# heuristic_MA.star_graph_MA_MIS(G, 'specific', 0, 1)