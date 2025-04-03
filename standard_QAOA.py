from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import networkx as nx
import time
import random

def QAOA(no_vertices, depth, seed, graph_type, save):
    """
    standard QAOA
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

    simulation_time = []

    def obj_func(parameter_values):
        start_time = time.perf_counter()

        dens_mat = build_operators.build_standard_qaoa_ansatz(graph, parameter_values, pauli_ops_dict)

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        # print(f"One round simulation took {minutes}m {seconds:.2f}s.")
        simulation_time.append(execution_time)

        expectation_value = (hamiltonian * dens_mat).trace().real

        return expectation_value * (-1.0)

    # cut_approx_ratio = 0
    # for _ in range(10):

    start_time = time.perf_counter()

    initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth)
    # random initial parameters
    # initial_parameter_guesses = [random.random() * 3 for _ in range(2*depth)]
    result = minimize(obj_func, initial_parameter_guesses,method="BFGS")

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    parameter_list = list(result.x)

    dens_mat = build_operators.build_standard_qaoa_ansatz(graph, parameter_list, pauli_ops_dict)
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    # cut_approx_ratio = max(cut_approx_ratio,(hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value)

    print("目标函数总调用次数:", result.nfev)
    print(f'total iteration: {result.nit}')
    print(f'cut_approx_ratio: {cut_approx_ratio}')
    print(f"optimization_time: {execution_time} s")
    print(f'simulation_time: {sum(simulation_time)}')

    # print(f'gamma: {parameter_list[:depth]}')
    # print(f'beta: {parameter_list[depth:]}')

    if(save):
        with open(f"./results/tmp_QAOA{depth}.csv", "a") as f:
            # f.write(f'QAOA,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio}, {result.nit}, {simulation_time}, {execution_time}\n')
            f.write(f'QAOA,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio},{result.nfev}, {result.nit}, {execution_time}, {sum(simulation_time)}\n')

    # if(save):
    #     with open(f"./results/QAOA/QAOA_{depth}.csv", "a") as f:
    #         f.write(f'standard_QAOA,{no_vertices},{graph_type[0] + str(graph_type[1])},{depth},{seed},{cut_approx_ratio}\n')
        # with open(f"./results/standard/standard{no_vertices}_{depth}random_layer{depth}_seed{seed}", 'a') as f:
        #     f.write(f"layers:{depth} standard-QAOA")
        #     f.write(f'gamma: {parameter_list[:depth]}')
        #     f.write(f'beta: {parameter_list[depth:]}')
