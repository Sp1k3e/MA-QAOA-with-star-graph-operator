from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from collections import deque
import time

def triangle_count(graph):
    count = [0] * graph.number_of_edges()
    index = 0
    for edge in graph.edges:
        u = edge[0]
        v = edge[1]
        for c in range(graph.number_of_nodes()):
            if  graph.has_edge(u,c) and graph.has_edge(v,c):
                count[index] += 1
        index += 1
    return count

def tune(graph, parameter):
    gamma = parameter[0]
    beta = parameter[1]
    parameter_list = []
    n = graph.number_of_nodes()

    tuned_nodes = [0] * n
    queue = deque([0])

    while queue:
        node = queue.popleft()
        nei = graph.neighbors(node)

        if tuned_nodes[node] == 0:
            tuned_nodes[node] = 1
            parameter_list += [gamma]
            for i in nei:
                tuned_nodes[i] = 2
                queue.
        elif tuned_nodes[node] == 1:
            for i in nei:

        else:
            for i in nei:


    for i in range(n):
        if tuned_nodes[i] == 1:
            parameter_list += 
        if tuned_nodes[i] == 2:
            parameter_list += 

    return parameter_list


def tune_QAOA(no_vertices, depth, seed, graph_type, save):
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]

    gamma_0 = 0.2
    beta_0 = 1

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]

    pauli_ops_dict = build_operators.build_my_paulis(no_vertices)
    hamiltonian = build_operators.cut_hamiltonian(graph)
    print(f'layers:{depth} standard-QAOA')
    #! 初始化完成

    def obj_func(parameter_values):
        dens_mat = build_operators.build_standard_qaoa_ansatz(graph, parameter_values, pauli_ops_dict)
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    # start_time = time.time()

    initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth)
    result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

    # end_time = time.time()
    # print(f"optimization_time: {round(end_time - start_time, 2)} seconds")

    parameter_list = list(result.x)

    # standard QAOA
    dens_mat = build_operators.build_standard_qaoa_ansatz(graph, parameter_list, pauli_ops_dict)
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    # ham_approx_ratio = hamiltonian_expectation / max_ham_eigenvalue
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    print(f'cut_approx_ratio: {cut_approx_ratio}')
    print(f'gamma: {parameter_list[:depth]}')
    print(f'beta: {parameter_list[depth:]}')
    # with open("./results/tmp.csv", "a") as f:
        # f.write(f'standard_QAOA,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio}\n')

    # tune beta
    tuned_parameter = tune(graph, parameter_list)

    dens_mat = build_operators.build_MA_qaoa_ansatz(graph, tuned_parameter, depth, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    print(f'tuned parameter cut_approx_ratio: {cut_approx_ratio}')
    print(f'gamma: {parameter_list[:depth]}')
    print(f'beta: {parameter_list[depth:]}')

    if(save):
        #only save parameters for standard QAOA
        with open(f"./results/standard/standard{no_vertices}_{depth}random_layer{depth}_seed{seed}", 'a') as f:
            f.write(f"layers:{depth} standard-QAOA")
            f.write(f'gamma: {parameter_list[:depth]}')
            f.write(f'beta: {parameter_list[depth:]}')