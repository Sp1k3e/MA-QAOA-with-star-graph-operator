'''
    在特定图上的MA-QAOA
'''
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
depth = 5
save = False

# edge_list = [(0,1), (1,2), (2,3)]
edge_list = [(0,1), (1,2), (2,3),(3,4)]
# edge_list = [(0,1), (1,2), (2,3), (1,4),(1,5),(2,6),(6,7),(7,8)] #can't solve in 2 layer
edge_list = [(0,1), (1,2), (2,3),(3,4),(4,5),(6,7)]
# edge_list = [(0,1), (1,2), (0,2)] #三角形
# edge_list = [(0,1), (1,2), (2,3), (0,3)] #正方形
# edge_list = [(0,1), (1,2), (0,2), (0,3), (3,4)]
# edge_list = [(0,1), (1,2), (1,3), (3,4)]

# edge_list = [(0,7), (3,7), (5,7), (2,7), (1,7), (2,3), (2,1), (1,6),(2,6),(5,6), (3,4), (4,6)]
# edge_list = [(0,1), (0,2), (1,2), (1,3),(2,3), (0,4), (0,5), (0,6)]

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

def obj_func(parameter_values):
    dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_values, depth, pauli_ops_dict, 'All')
    expectation_value = (hamiltonian * dens_mat).trace().real
    return expectation_value * (-1.0)

initial_parameter_guesses = [gamma_0] * (depth * no_edges) + [beta_0] * (depth * no_vertices)
bounds = [(-3.1416, 3.1416)] * (depth * no_edges) + [(0, 6.2832)] * (depth * no_vertices)
# result = minimize(obj_func, initial_parameter_guesses,  method="BFGS")
result = minimize(obj_func, initial_parameter_guesses, bounds=bounds, method="L-BFGS-B")

#! 输出结果
parameter_list = list(result.x)
#todo 单独计算每层ap
dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_list, depth, pauli_ops_dict, 'All')
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value


print('***************')
print(f'cut_approx_ratio: {cut_approx_ratio}')
# if(save):
#     with open(f"./results/parameters/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}", 'w') as f:
#         f.write(f"max cut: {max_cut_solution[0]}\n")
#         f.write(f'r: {cut_approx_ratio}\n')

if(save):
    pdf_pages = PdfPages(f"./results/specific_graph/MA{no_vertices}_layer{depth}.pdf")

for layer in range(depth):
    print('-----------------------------------------------')
    print(f'layer {layer + 1:}')
    my_dict = {key: value for key, value in zip(graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])} # gamma for every edge
    for key, value in my_dict.items():
        print(f"{key}: {value:.4f}")
    print(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')

    if(save):
        # with open(f"./results/parameters/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}", 'a') as f:
            # f.write(f'layer {layer + 1:}\n')
        for key, value in my_dict.items():
                # f.write(f"{key}: {value:.4f}\n")
            my_dict[key] = format(my_dict[key], '.2f')
            # f.write(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}\n')

        plt.figure()
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

        plt.title(f'MA{no_vertices}_layer{layer + 1} r:{cut_approx_ratio}')
        pdf_pages.savefig()
        plt.close()
        # plt.savefig(f"./results/specific_graph/MA{no_vertices}_layer{depth}.png")

if(save):
    pdf_pages.close()

print('-----------------------------------------------')
