import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
    
gamma_0 = -0.7854
beta_0 = 0.7854
depth = 4
saveFig = False

# edge_list = [(0,1), (1,2), (2,3)]
# edge_list = [(0,1), (1,2), (2,3),(3,4)]
# edge_list = [(0,1), (1,2), (2,3), (1,4),(1,5),(2,6),(6,7),(7,8)] #can't solve in 2 layer
# edge_list = [(0,1), (1,2), (2,3),(3,4),(4,5),(6,7)]
# edge_list = [(0,1), (1,2), (0,2)] #三角形
# edge_list = [(0,1), (1,2), (2,3), (0,3)] #正方形
# edge_list = [(0,1), (1,2), (0,2), (0,3), (3,4)]
# edge_list = [(0,1), (1,2), (1,3), (3,4)]

edge_list = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)] # line
edge_list = [(0,1),(1,2),(2,3),(3,4),(4,5)] # line
# edge_list = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(0,7)] # polygon

# graph contain line
# edge_list = [(0,1), (1,2),(1,3),(3,4),(4,5),(5,6),(5,7)]

graph = nx.Graph();
graph.add_edges_from(edge_list)
no_vertices = graph.number_of_nodes()
for index, edge in enumerate(graph.edges()):
    graph.get_edge_data(*edge)['weight'] = 1
graph_type = ['manual', no_vertices]

no_edges = graph.number_of_edges()
pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
hamiltonian = build_operators.cut_hamiltonian(graph)

max_cut_solution = useful_methods.find_optimal_cut(graph)
print(f"max cut: {max_cut_solution[0]}")
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]
print(f'layers:{depth} specific_graph MA-All')
#! 初始化完成

# phase_operator_edge_list = [(0,1), (1,2),(1,3),(3,4),(3,5),(3,6),(3,7)]
phase_operator_edge_list = edge_list
target_graph = nx.Graph()
target_graph.add_edges_from(phase_operator_edge_list)
no_edges = target_graph.number_of_edges()


def obj_func(parameter_values):
    dens_mat = build_operators.build_standard_qaoa_ansatz(target_graph, parameter_values, depth, pauli_ops_dict, 'All')
    expectation_value = (hamiltonian * dens_mat).trace().real
    return expectation_value * (-1.0)

initial_parameter_guesses = [gamma_0] * (depth * no_edges) + [beta_0] * (depth * no_vertices)
bounds = [(-3.1416, 3.1416)] * (depth * no_edges) + [(0, 6.2832)] * (depth * no_vertices)
# result = minimize(obj_func, initial_parameter_guesses,  method="BFGS")
result = minimize(obj_func, initial_parameter_guesses, bounds=bounds, method="Nelder-Mead")

#! 输出结果
parameter_list = list(result.x)
dens_mat = build_operators.build_standard_qaoa_ansatz(target_graph, parameter_list, depth, pauli_ops_dict, 'All')
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value


print('***************')
print(f'cut_approx_ratio: {cut_approx_ratio}')
# if(save):
#     with open(f"./results/parameters/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}", 'w') as f:
#         f.write(f"max cut: {max_cut_solution[0]}\n")
#         f.write(f'r: {cut_approx_ratio}\n')

for layer in range(depth):
    print('-----------------------------------------------')
    print(f'layer {layer + 1:}')
    my_dict = {key: value for key, value in zip(target_graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])} # gamma for every edge
    for key, value in my_dict.items():
        print(f"{key}: {value:.4f}")
    print(f'beta: {[round(num, 3) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')


print('-----------------------------------------------')
