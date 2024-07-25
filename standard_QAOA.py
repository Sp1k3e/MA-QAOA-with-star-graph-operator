from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import matplotlib.pyplot as plt

no_vertices = 10
depth = 2
seed = 1
p = 0.7
save = False
graph = generate_graphs.generate_connected_graph(no_vertices, p, seed)[0]
print(f'layers:{depth} standard-QAOA')

gamma_0 = 0.2
beta_0 = 1

max_cut_solution = useful_methods.find_optimal_cut(graph)
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]

pauli_ops_dict = build_operators.build_my_paulis(no_vertices)
hamiltonian = build_operators.cut_hamiltonian(graph)
#! 初始化完成

def obj_func(parameter_values):
    dens_mat = build_operators.build_standard_qaoa_ansatz(graph, parameter_values, pauli_ops_dict)
    expectation_value = (hamiltonian * dens_mat).trace().real
    return expectation_value * (-1.0)

initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth)
result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

parameter_list = list(result.x)

dens_mat = build_operators.build_standard_qaoa_ansatz(graph, parameter_list, pauli_ops_dict)
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
ham_approx_ratio = hamiltonian_expectation / max_ham_eigenvalue
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

print(f'cut_approx_ratio: {cut_approx_ratio}')
print(f'gamma: {parameter_list[:depth]}')
print(f'beta: {parameter_list[depth:]}')

if(save):
    #only save parameters for standard QAOA
    with open(f"./results/parameters/standard/standard{no_vertices}", 'a') as f:
        f.write(f"layers:{depth} standard-QAOA")
        f.write(f'gamma: {parameter_list[:depth]}')
        f.write(f'beta: {parameter_list[depth:]}')