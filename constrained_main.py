import constrained_problem_QAOA
import heuristic_MA
from src_code import generate_graphs
import networkx as nx
import numpy as np

np.set_printoptions(precision=3, suppress=True)
save = False
save = True

no_vertices = 8
seed = 1

depth = 5
# circuit_type = "partial mixer"
circuit_type = "unconstrained"
# circuit_type = "MA"
test = False

if(test):
    G = nx.Graph()
    edge_list = [(0,1)]
    edge_list = [(0,1), (0,2)] #三角形少一条边
    edge_list = [(0,1), (1,2), (0,2)] #三角形
    # edge_list = [(0,1), (1,2), (1,3)] #正方形少一条边
    # edge_list = [(0,1), (1,2), (2,3), (0,3)] #正方形
    # edge_list = [(0,1), (1,2), (1,3), (3,4), (2,3)]
    G.add_edges_from(edge_list)


    G = generate_graphs.generate_graph_type(no_vertices,['random', 0.5], seed)[0]
    no_vertices = G.number_of_nodes()

    #! custom phase operator
    custom_phase_operator = G.copy()
    custom_phase_operator = None
    # custom_phase_operator.remove_edge(0,2)
    # custom_phase_operator.add_edge(1,2)
    # print(G)

    # tests-------------------------------------------------------------------
    # !initial state should be (superposition of) feasible solution for partial mixer
    initial_state = [0b000]
    # initial_state = [0b111]
    initial_vector = np.zeros(2**no_vertices)
    for i in initial_state:
        initial_vector[i] = 1
    initial_vector = initial_vector/np.linalg.norm(initial_vector)

    initial_vector = []
    if(circuit_type != "unconstrained" and len(initial_vector) != 0):
        print("initial_vector:")
        for i in range(2**no_vertices):
            if(initial_vector[i] > 0.001):
                print(format(i, f'0{no_vertices}b'), end = ' ')
                print(initial_vector[i])
        print('------------------------')

    #! partial mixer
    if(circuit_type == "partial mixer"):
        constrained_problem_QAOA.MIS_QAOA(G, depth, use_constrain_operator=True, initial_state=initial_vector, custom_phase_operator=custom_phase_operator)

    #! unconstraned circuit
    penalty_term = 1 # in real cost function, this should multiple 2
    if(circuit_type == "unconstrained"):
        constrained_problem_QAOA.MIS_QAOA(G, depth, False, penalty_term, custom_phase_operator=custom_phase_operator)

    #! MA
    if(circuit_type == "MA"):
        constrained_problem_QAOA.MIS_MA_QAOA(G,depth, penalty_term, initial_state=initial_vector)
    # heuristic_MA.star_graph_MA_MIS(G, 'specific', 0, 1)

    raise SystemExit("程序终止")
    # tests end----------------------------------------------------------------

#! simulations
# initial_state = []
for seed in range(50):
    G = generate_graphs.generate_graph_type(no_vertices,['random', 0.5], seed)[0]

    # constrained_problem_QAOA.MIS_QAOA(G, depth, use_constrain_operator=True)
    constrained_problem_QAOA.MIS_QAOA(G, depth, use_constrain_operator=False, save=save, seed=seed)


