import networkx
import random
from src_code import build_operators
from src_code import useful_methods
from scipy.optimize import minimize
import math
import matplotlib.pyplot as plt

def generate_graph(n, seed):
    graph = networkx.Graph()
    edge_list = []
    for n1 in range(n):
        for n2 in range(n1+1,n):
            edge_list.append((n1,n2))
    
    graph.add_edges_from(edge_list)
    random.seed(seed)
    weights = [random.random() for i in range(len(edge_list))]

    for index, edge in enumerate(graph.edges()):
        graph.get_edge_data(*edge)['weight'] = weights[index]

    return graph, weights

no_vertices = 5
seed = 1
graph = generate_graph(no_vertices, seed)[0]
depth = 5

pauli_ops_dict = build_operators.build_all_paulis(no_vertices)
# print(pauli_ops_dict)
gamma_0 = 0.01
beta_0 = 0.0
alpha_0 = 0.0

max_cut_solution = useful_methods.find_optimal_cut(graph)
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]

hamiltonian = build_operators.cut_hamiltonian(graph)
#初始化完成


def obj_func(parameter_values):
    dens_mat = build_operators.build_XinY_qaoa_ansatz(graph, parameter_values, pauli_ops_dict)
    expectation_value = (hamiltonian * dens_mat).trace().real
    return expectation_value * (-1.0)

initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth) + [alpha_0] * (depth)
# initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth)
result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

parameter_list = list(result.x)
dens_mat = build_operators.build_XinY_qaoa_ansatz(graph, parameter_list, pauli_ops_dict)
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

data = {
    'cut_approx_ratio' : cut_approx_ratio,
    # 'optimised_Hamiltonian_unitary_parameters' : parameter_list[:depth],
    # 'optimised_mixer_unitary_parameters' : parameter_list[depth:],
}
print(f'cut_approx_ratio: {cut_approx_ratio}')