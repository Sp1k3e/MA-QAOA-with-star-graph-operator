from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import math
import networkx as nx
import matplotlib.pyplot as plt

depth = 2
no_vertices = 8
seed = 1
p = 0.4
graph = generate_graphs.generate_connected_graph(no_vertices, seed)[0]
no_edges = graph.number_of_edges()
# networkx.draw_networkx(graph)
# plt.show()
print(f'no_v:{no_vertices} seed:{seed} p:{p}  layer:{depth} MA_Phaser')

pauli_ops_dict = build_operators.build_all_paulis(no_vertices)
# print(pauli_ops_dict)
gamma_0 = 0.5
beta_0 = 0.0

max_cut_solution = useful_methods.find_optimal_cut(graph)
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]

hamiltonian = build_operators.cut_hamiltonian(graph)
#! 初始化完成


def obj_func(parameter_values):
    dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_values, depth, pauli_ops_dict, 'P')
    expectation_value = (hamiltonian * dens_mat).trace().real
    return expectation_value * (-1.0)

# 只改phaser
initial_parameter_guesses = [gamma_0] * (depth * graph.number_of_edges()) + [beta_0] * (depth)

result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

#! 输出结果
parameter_list = list(result.x)
dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_list, depth, pauli_ops_dict, 'P')
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value
print(f'cut_approx_ratio: {cut_approx_ratio}')

#? Rounding
parameter_list2 = [0 if -0.2 < x < 0.2 else x for x in parameter_list]
dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_list2, depth, pauli_ops_dict, 'P')
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

print(f'rounding cut_approx_ratio: {cut_approx_ratio}')

# for edge in graph.edges:
#     print(edge, end='')
# print(f'gamma: {parameter_list[:depth * graph.number_of_edges()]}')
# print(f'beta: {parameter_list[depth * graph.number_of_edges():]}')

for layer in range(depth):
    print('-----------------------------------------------')
    print(f'layer {layer + 1:}')
    my_dict = {key: value for key, value in zip(graph.edges, parameter_list2[layer * no_edges : (layer + 1) * no_edges])}
    # print(f'gamma: {my_dict}')
    for key, value in my_dict.items():
        my_dict[key] = round(value, 3)
        print(f"{key}: {value:.4f}")
    print(f'beta: {parameter_list2[depth * no_edges + layer]}')


# todo 可视化每条边的gamma
# pos = nx.circular_layout(graph)
# labels = nx.shell_layout(graph,'weight')
# nx.draw_networkx(graph, pos)
# nx.draw_networkx_nodes(graph, pos)
# nx.draw_networkx_edges(graph, pos, graph.edges(), connectionstyle='arc3, rad = 0.1')
# nx.draw_networkx_edge_labels(graph, pos, edge_labels=my_dict,label_pos=0.3)
# plt.show()