from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import time

def QAOA(no_vertices, depth, seed, graph_type, save):
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

    start_time = time.time()

    initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth)
    result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

    end_time = time.time()
    print(f"optimization_time: {round(end_time - start_time, 2)} seconds")

    parameter_list = list(result.x)

    dens_mat = build_operators.build_standard_qaoa_ansatz(graph, parameter_list, pauli_ops_dict)
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    ham_approx_ratio = hamiltonian_expectation / max_ham_eigenvalue
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    print(f'cut_approx_ratio: {cut_approx_ratio}')
    print(f'gamma: {parameter_list[:depth]}')
    print(f'beta: {parameter_list[depth:]}')
    with open("./results/tmp.csv", "a") as f:
        f.write(f'standard_QAOA,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio}\n')

    if(save):
        #only save parameters for standard QAOA
        with open(f"./results/standard/standard{no_vertices}_{depth}random_layer{depth}_seed{seed}", 'a') as f:
            f.write(f"layers:{depth} standard-QAOA")
            f.write(f'gamma: {parameter_list[:depth]}')
            f.write(f'beta: {parameter_list[depth:]}')