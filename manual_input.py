import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
import time

a = 0.7854
b = -0.7854
    
# no_vertices = 6
# depth = 1
# seed = 7
# graph_type = ['random', 0.4]
# save = True
# graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]
# parameter_list = [a,0,b,b,b,b] + [0,a,0,a,0,0]

no_vertices = 3
depth = 1
seed = 7
graph_type = ['random', 0]
save = True
graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]
parameter_list = [b,0,b] + [a,0,a]


#! input parameters manually

no_edges = graph.number_of_edges()
pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
hamiltonian = build_operators.cut_hamiltonian(graph)

max_cut_solution = useful_methods.find_optimal_cut(graph)
print(f"max cut: {max_cut_solution[0]}")
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]
#! 初始化完成

#! 输出结果
dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_list, depth, pauli_ops_dict, 'All')
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

print(f'layers:{depth} MA-All')
print('***************')
print(f'cut_approx_ratio: {cut_approx_ratio}')

for layer in range(depth):
    print('-----------------------------------------------')
    print(f'layer {layer + 1:}')
    my_dict = {key: value for key, value in zip(graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])} # gamma for every edge
    for key, value in my_dict.items():
        print(f"{key}: {value:.4f}")
    print(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')

    if(save):
        for key, value in my_dict.items():
            my_dict[key] = format(my_dict[key], '.2f')

        plt.clf()
        l_dict = {}
        for n in range(no_vertices):
            l_dict[n] = round(parameter_list[depth * no_edges + layer * no_vertices + n] ,2)
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_edge_labels(graph, pos, my_dict, font_size=8) #每条边的gamma
        nx.draw_networkx_labels(graph, pos, l_dict, font_size=10) #每个点的beta
        for i in range(no_vertices):
            pos[i] += np.array([-0.06, 0.06]) 
        nx.draw_networkx_labels(graph, pos, {key:value for key, value in zip(range(no_vertices), max_cut_solution[0])}, font_color= "r", alpha=0.8,font_size=10)
        for i in range(no_vertices):
            pos[i] += np.array([0.0, -0.12]) 
        nx.draw_networkx_labels(graph, pos, font_color="g", font_size=10)

        plt.title(f'MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}  r:{cut_approx_ratio}')
        plt.savefig(f"./results/manual_input{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}.png")

print('-----------------------------------------------')
