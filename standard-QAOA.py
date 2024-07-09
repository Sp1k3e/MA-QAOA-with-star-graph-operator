from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import random

no_vertices = 2
depth = 1
seed = 1
p = 0.4
graph = generate_graphs.generate_connected_graph(no_vertices, seed, p)[0]
# graph = generate_graphs.generate_regular_graph(no_vertices,3,seed)[0]
print(f'layers:{depth} standard-QAOA')

pauli_ops_dict = build_operators.build_all_paulis(no_vertices)
gamma_0 = 0.1
beta_0 = 0.0

max_cut_solution = useful_methods.find_optimal_cut(graph)
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]

hamiltonian = build_operators.cut_hamiltonian(graph)
#! 初始化完成

def obj_func(parameter_values):
    dens_mat = build_operators.build_standard_qaoa_ansatz(graph, parameter_values, pauli_ops_dict)
    expectation_value = (hamiltonian * dens_mat).trace().real
    return expectation_value * (-1.0)

initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth)
# initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth)
result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

parameter_list = list(result.x)

dens_mat = build_operators.build_standard_qaoa_ansatz(graph, parameter_list, pauli_ops_dict)
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
ham_approx_ratio = hamiltonian_expectation / max_ham_eigenvalue
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

data = {
    'cut_approx_ratio' : cut_approx_ratio,
    'ham_approx_ratio' : ham_approx_ratio,
    'optimised_Hamiltonian_unitary_parameters' : parameter_list[:depth],
    'optimised_mixer_unitary_parameters' : parameter_list[depth:],
}

print(f'cut_approx_ratio: {cut_approx_ratio}')
print(f'gamma: {parameter_list[:depth]}')
print(f'beta: {parameter_list[depth:]}')


#! fix gammas to update multi-angle betas
# gammas = parameter_list[:-1]
# # optimize beta again
# def obj_func2(parameter_values):
#     parameter_values = gammas + parameter_values.tolist()
#     dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_values, depth, pauli_ops_dict, 'SM')
#     expectation_value = (hamiltonian * dens_mat).trace().real
#     return expectation_value * (-1.0)

# # initial_parameter_guesses = [beta_0] * (depth * no_vertices)
# initial_parameter_guesses = [beta_0] * (no_vertices)
# result = minimize(obj_func2, initial_parameter_guesses, method="BFGS")

# parameter_list = list(result.x)
# parameter_list = gammas + parameter_list

# dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_list, depth, pauli_ops_dict, 'SM')
# hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
# ham_approx_ratio = hamiltonian_expectation / max_ham_eigenvalue
# cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

# print('-------------------------------')
# print(f'cut_approx_ratio: {cut_approx_ratio}')
# for layer in range(depth):
#     print('-------------------------------------------------')
#     print(f'layer {layer + 1:}')
#     print(f'gamma: {parameter_list[layer]}')
#     print(f'beta: {[round(num, 4) for num in parameter_list[depth + layer * no_vertices: depth + (layer + 1) * no_vertices]]}')