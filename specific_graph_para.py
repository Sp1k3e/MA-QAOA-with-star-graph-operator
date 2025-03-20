'''
    手动输入图和参数
'''
import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
import numpy as np
import matplotlib.pyplot as plt

a = 1.5708
b = 0.7854
depth = 1
save = False   
show = False

# no_vertices = 6
# depth = 1
# seed = 7
# graph_type = ['random', 0.4]
# graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]
# parameter_list = [a,0,b,b,b,b] + [0,a,0,a,0,0]

# no_vertices = 3
# depth = 1
# seed = 7
# graph_type = ['random', 0]
# graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]
# parameter_list = [b,0,b] + [a,0,a]

# edge_list = [(0,1)]
# parameter_list = [1.56] + [0,b]

# edge_list = [(0,1), (1,2)]
# parameter_list = [a,a] + [b,0,b]
# parameter_list = [b,b] + [0,a,0]

# edge_list = [(0,1), (1,2), (1,3)]
# parameter_list = [a,a,a] + [b,0,b,0]
# save_name = '-2'

edge_list = [(0,1), (1,2), (2,3)]
parameter_list = [a,-a,a] + [0,b,b,b]

# edge_list = [(0,1), (1,2), (2,3)]
# parameter_list = [b,0,b] + [0,a,0,a]
# save_name = '-1'

# edge_list = [(0,1), (1,2), (2,3), (2,4)]
# parameter_list = [b,b,b,b] + [0,a,0,a,a]
# save_name = ''

depth = 1
edge_list = [(0,1), (1,2), (2,3)]
parameter_list = [0, 1.5708, 0]+[-1.5708, -0.863, -1.5708] + [0.1579, 0.3927, 0.3927, 0.1579] + [0.7854, 1.5708, 1.5708, 0.7854]
parameter_list = [0, 1.5708, 0]+[-1.5708, -0.863, -1.5708] + [0.1579, 0.3927, 0.3927, 0.1579] + [0.7854, 1.5708, 1.5708, 0.7854]

graph = nx.Graph();
graph.add_edges_from(edge_list)
no_vertices = graph.number_of_nodes()
for index, edge in enumerate(graph.edges()):
    graph.get_edge_data(*edge)['weight'] = 1

no_edges = graph.number_of_edges()

target_graph = graph


pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
hamiltonian = build_operators.cut_hamiltonian(graph)
max_cut_solution = useful_methods.find_optimal_cut(graph)
print(f"max cut: {max_cut_solution[0]}")
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]


#! 直接运行
dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, depth, pauli_ops_dict, 'All')
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
# print(hamiltonian_expectation)
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

print(f'layers:{depth} MA-All specific graph and parameters')
print(f'cut_approx_ratio: {cut_approx_ratio}')
print('-----------------------------------------------')

for layer in range(depth):
    print('-----------------------------------------------')
    print(f'layer {layer + 1:}')
    my_dict = {key: value for key, value in zip(target_graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])} # gamma for every edge
    for key, value in my_dict.items():
        print(f"{key}: {value:.4f}")
    print(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')

    if(show or save):
        for key, value in my_dict.items():
            my_dict[key] = format(my_dict[key], '.2f')

        plt.clf()
        l_dict = {}
        for n in range(no_vertices):
            l_dict[n] = round(parameter_list[depth * no_edges + layer * no_vertices + n] ,2)
        pos = nx.spring_layout(target_graph)
        nx.draw_networkx_nodes(target_graph, pos)
        nx.draw_networkx_edges(target_graph, pos)
        nx.draw_networkx_edge_labels(target_graph, pos, my_dict, font_size=8) #每条边的gamma
        nx.draw_networkx_labels(target_graph, pos, l_dict, font_size=10) #每个点的beta
        for i in range(no_vertices):
            pos[i] += np.array([-0.06, 0.06]) 
        nx.draw_networkx_labels(target_graph, pos, {key:value for key, value in zip(range(no_vertices), max_cut_solution[0])}, font_color= "r", alpha=0.8,font_size=10)
        for i in range(no_vertices):
            pos[i] += np.array([0.0, -0.12]) 
        nx.draw_networkx_labels(target_graph, pos, font_color="g", font_size=10)

        plt.title(f'MA subgraph r:{cut_approx_ratio}')
        if show:
            plt.show()
            plt.clf()
            nx.draw_networkx_nodes(graph, pos)
            nx.draw_networkx_edges(graph, pos)
            for i in range(no_vertices):
                pos[i] += np.array([-0.06, 0.06]) 
            nx.draw_networkx_labels(target_graph, pos, {key:value for key, value in zip(range(no_vertices), max_cut_solution[0])}, font_color= "r", alpha=0.8,font_size=10)
            for i in range(no_vertices):
                pos[i] += np.array([0.0, -0.12]) 
            nx.draw_networkx_labels(target_graph, pos, font_color="g", font_size=10)
            plt.show()

        # plt.savefig(f"./results/manual_input{time.time()}.png")
        # plt.savefig(f"./results/specific_target_graph/manual/manual_input{no_vertices}{save_name}.png")

