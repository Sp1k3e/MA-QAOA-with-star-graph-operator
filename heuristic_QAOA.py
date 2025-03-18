from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import networkx as nx
import time

def TR_QAOA(no_vertices, depth, seed, graph_type, save):
    """
    triangle removed QAOA
    """
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]

    gamma_0 = 0.2
    beta_0 = 1

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices)
    hamiltonian = build_operators.cut_hamiltonian(graph)
    print(f'layers:{depth} TR-QAOA')
    #! 初始化完成

    #! phase operator
    target_graph = graph

    # TR_Most
    """ 
    triangles = [cycle for cycle in nx.cycle_basis(target_graph) if len(cycle) == 3]
    for triangle in triangles:
        u, v = triangle[0], triangle[1]
        if target_graph.has_edge(u, v):
            target_graph.remove_edge(u, v)
    """

    # TR_All
    while [cycle for cycle in nx.cycle_basis(target_graph) if len(cycle) == 3]:
        c = [cycle for cycle in nx.cycle_basis(target_graph) if len(cycle) == 3][0]
        u, v = c[0], c[1]
        if target_graph.has_edge(u, v):
            target_graph.remove_edge(u, v)

    if nx.is_connected(target_graph) == False:
        print("bad seed, disconnected graph")
        return
    # selected_e = target_graph.edges()
    # print(f'selected edges:{selected_e}')

    def obj_func(parameter_values):
        dens_mat = build_operators.build_standard_qaoa_ansatz(target_graph, parameter_values, pauli_ops_dict)
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    # start_time = time.time()

    initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth)
    result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

    # end_time = time.time()
    # print(f"optimization_time: {round(end_time - start_time, 2)} seconds")

    parameter_list = list(result.x)

    dens_mat = build_operators.build_standard_qaoa_ansatz(target_graph, parameter_list, pauli_ops_dict)
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    print(f'cut_approx_ratio: {cut_approx_ratio}')
    # print(f'gamma: {parameter_list[:depth]}')
    # print(f'beta: {parameter_list[depth:]}')
    print('--------------------------------------')

    if(save):
        with open("./results/QAOA/TR_QAOA.csv", "a") as f:
            f.write(f'TR_QAOA,{no_vertices},{graph_type[0] + str(graph_type[1])},{depth},{seed},{cut_approx_ratio}\n')


def star_graph_QAOA(no_vertices, depth, seed, graph_type, save):
    """
    star graph phase operator QAOA
    """
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
    selected_e = []

    for i in range(no_vertices - 1):
        selected_e += [(0, i + 1)]

    print(f'selected edges:{selected_e}')
    
    #! 只在目标图上优化
    target_graph = nx.Graph()
    target_graph.add_edges_from(selected_e)
    for index, edge in enumerate(target_graph.edges()):
        target_graph.get_edge_data(*edge)['weight'] = 1


    def obj_func(parameter_values):
        dens_mat = build_operators.build_standard_qaoa_ansatz(target_graph, parameter_values, pauli_ops_dict)
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    # start_time = time.time()
    initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth)
    result = minimize(obj_func, initial_parameter_guesses, method="BFGS")
    # end_time = time.time()
    # print(f"optimization_time: {round(end_time - start_time, 2)} seconds")

    parameter_list = list(result.x)

    dens_mat = build_operators.build_standard_qaoa_ansatz(target_graph, parameter_list, pauli_ops_dict)
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    print(f'cut_approx_ratio: {cut_approx_ratio}')
    print(f'gamma: {parameter_list[:depth]}')
    print(f'beta: {parameter_list[depth:]}')
    # with open("./results/tmp.csv", "a") as f:
    #     f.write(f'standard_QAOA,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio}\n')

    if(save):
        #only save parameters for standard QAOA
        with open(f"./results/standard/standard{no_vertices}_{depth}random_layer{depth}_seed{seed}", 'a') as f:
            f.write(f"layers:{depth} standard-QAOA")
            f.write(f'gamma: {parameter_list[:depth]}')
            f.write(f'beta: {parameter_list[depth:]}')