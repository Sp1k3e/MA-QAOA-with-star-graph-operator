from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import math
import matplotlib.pyplot as plt

no_vertices = 6
seed = 1
graph = generate_graphs.generate_connected_graph(no_vertices, seed)[0]
no_edges = graph.number_of_edges()
# networkx.draw_networkx(graph)
# plt.show()

pauli_ops_dict = build_operators.build_all_paulis(no_vertices)
# print(pauli_ops_dict)
gamma_0 = 0.01
beta_0 = 0.0

max_cut_solution = useful_methods.find_optimal_cut(graph)
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]

hamiltonian = build_operators.cut_hamiltonian(graph)
#! 初始化完成

depth = 2

def obj_func(parameter_values):
    dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_values, depth, pauli_ops_dict, 'M')
    expectation_value = (hamiltonian * dens_mat).trace().real
    return expectation_value * (-1.0)

# 只改mixer
initial_parameter_guesses = [gamma_0] * (depth) + [beta_0] * (depth * no_vertices)

result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

#! 输出结果
parameter_list = list(result.x)
dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_list, depth, pauli_ops_dict, 'M')
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value


print(f'no_v:{no_vertices} seed:{seed}')
print(f'cut_approx_ratio: {cut_approx_ratio}')

# for edge in graph.edges:
#     print(edge, end='')
# print(f'gamma: {parameter_list[:depth * graph.number_of_edges()]}')
# print(f'beta: {parameter_list[depth * graph.number_of_edges():]}')

# todo 可视化每条边的gamma
for layer in range(depth):
    print('-------------------------------------------------')
    print(f'layer {layer + 1:}')
    print(f'gamma: {parameter_list[layer]}')
    print(f'beta: {parameter_list[depth + layer * no_vertices: depth + (layer + 1) * no_vertices]}')
