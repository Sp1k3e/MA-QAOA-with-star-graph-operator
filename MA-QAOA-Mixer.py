from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import networkx as nx
import matplotlib.pyplot as plt

depth = 3
no_vertices = 10
seed = 1
p = 0.4
# graph = generate_graphs.generate_connected_graph(no_vertices, seed, p)[0]
graph = generate_graphs.generate_regular_graph(no_vertices, 3, seed)[0]
no_edges = graph.number_of_edges()

print(f'layers:{depth} MA-Mixer')

pauli_ops_dict = build_operators.build_all_paulis(no_vertices)
gamma_0 = 0.5
beta_0 = 0.0

max_cut_solution = useful_methods.find_optimal_cut(graph)
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]

hamiltonian = build_operators.cut_hamiltonian(graph)
#! 初始化完成

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

print(f'cut_approx_ratio: {cut_approx_ratio}')

for layer in range(depth):
    print('-------------------------------------------------')
    print(f'layer {layer + 1:}')
    print(f'gamma: {parameter_list[layer]}')
    print(f'beta: {[round(num, 4) for num in parameter_list[depth + layer * no_vertices: depth + (layer + 1) * no_vertices]]}')

    #! 输出每个点的beta
    # l_dict = {}
    # for n in range(no_vertices):
    #     l_dict[n] = round(parameter_list[depth + layer * no_vertices + n] ,4)
    # pos = nx.circular_layout(graph)
    # nx.draw_networkx_nodes(graph, pos)
    # nx.draw_networkx_edges(graph, pos)
    # nx.draw_networkx_labels(graph, pos, l_dict)
    # plt.show()


# before = parameter_list
# def obj_func2(parameter_values):
#     parameter_values = before + parameter_values.tolist()
#     dens_mat = build_operators.build_Y_qaoa_ansatz(graph, parameter_values, depth,pauli_ops_dict)
#     expectation_value = (hamiltonian * dens_mat).trace().real
#     return expectation_value * (-1.0)

# initial_parameter_guesses = [0.1] * 3
# result = minimize(obj_func2, initial_parameter_guesses, method="BFGS")

# parameter_list = before + list(result.x)

# dens_mat = build_operators.build_Y_qaoa_ansatz(graph, parameter_list, depth, pauli_ops_dict)
# hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
# ham_approx_ratio = hamiltonian_expectation / max_ham_eigenvalue
# cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

# print(f'cut_approx_ratio: {cut_approx_ratio}')
# print(result.x)