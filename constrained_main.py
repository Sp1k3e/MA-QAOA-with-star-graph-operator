import constrained_problem_QAOA
import heuristic_MA
from src_code import generate_graphs
import networkx as nx
import numpy as np
np.set_printoptions(precision=3, suppress=True)

penalty_term = 1
no_vertices = 8
p = 0.4
depth = 1

# circuit_type = "partial mixer"
circuit_type = "unconstrained"
# circuit_type = "MA"

phase_operator_type = 'additional_RX'
# phase_operator_type = 'variational_lambda'
# phase_operator_type = 'variational_lambdas'
# phase_operator_type = 'fewer_RZ'
# phase_operator_type = 'multiply_gamma'
# phase_operator_type = 'original'

save = False
save = True

test = False
test = True


if(test):
    seed = 10
    # G = nx.Graph()
    # edge_list = [(0,1)]
    # edge_list = [(0,1), (0,2)] #三角形少一条边
    # edge_list = [(0,1), (1,2), (0,2)] #三角形
    # edge_list = [(0,1), (1,2), (1,3)] #正方形少一条边
    # edge_list = [(0,1), (1,2), (2,3), (0,3)] #正方形
    # edge_list = [(0,1), (1,2), (1,3), (3,4), (2,3)]
    # G.add_edges_from(edge_list)

    G = generate_graphs.generate_graph_type(no_vertices,['random', p], seed)[0]
    no_vertices = G.number_of_nodes()
    edge_list = G.edges()
    print(edge_list)

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
    if(circuit_type == "unconstrained"):
        constrained_problem_QAOA.MIS_QAOA(G, depth, False, penalty_term, custom_phase_operator=custom_phase_operator, save=save, phase_operator_type=phase_operator_type, p=p, seed=seed)

    #! MA
    if(circuit_type == "MA"):
        constrained_problem_QAOA.MIS_MA_QAOA(G,depth, penalty_term, initial_state=initial_vector)
    # heuristic_MA.star_graph_MA_MIS(G, 'specific', 0, 1)

    raise SystemExit("test done")
    # tests end----------------------------------------------------------------

#! simulations
# initial_state = []
for seed in range(11):
    G = generate_graphs.generate_graph_type(no_vertices,['random', p], seed)[0]
    if nx.is_connected(G) == False:
        print("unconnected graph")
        continue

    # constrained_problem_QAOA.MIS_QAOA(G, depth, use_constrain_operator=True)

    if(circuit_type == 'unconstrained'):
        constrained_problem_QAOA.MIS_QAOA(G, depth, use_constrain_operator=False, save=save, seed=seed, p = p, phase_operator_type=phase_operator_type, penalty_term=penalty_term)


    if(circuit_type == 'MA'):
        constrained_problem_QAOA.MIS_MA_QAOA(G,depth, penalty_term, save = save, seed=seed)


