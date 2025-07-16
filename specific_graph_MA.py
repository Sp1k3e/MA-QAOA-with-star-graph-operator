import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import random
    
depth = 2
use_different_phase_operators = True
# use_different_phase_operators = False

saveFig = False
save = True

# problem graph-----------------------------------------------------------
edge_list = [(0,1), (1,2), (2,3)]
# edge_list = [(0,1), (1,2), (2,3),(3,4)]
# edge_list = [(0,1),(1,2),(2,3),(3,4),(4,5)] # 2-layer can't solve this
# edge_list = [(0,1),(1,2),(2,3),(3,4),(4,5), (5,6)] 
# edge_list = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)] 

# edge_list = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(0,7)] # polygon

# edge_list = [(0,1), (1,2), (0,2)] # Triangle
# edge_list = [(0,1), (1,2), (2,3), (0,3)] #正方形
# edge_list = [(0,1), (1,2), (0,2), (0,3), (3,4)]
# edge_list = [(0,1), (1,2), (2,3), (1,4),(1,5),(2,6),(6,7),(7,8)]

# graphs contain line
# edge_list = [(0,1), (1,2),(1,3),(3,4),(4,5),(5,6),(5,7)]
# edge_list = [(0,1), (1,2),(1,3),(3,4),(4,5),(5,6),(6,7), (6,8)]

# custom phase operator----------------------------------------------------
phase_operator_edge_list = edge_list
# phase_operator_edge_list = [(0,1), (1,2), (2,3)]
# phase_operator_edge_list = [(0,1), (1,2),(1,3),(3,4),(3,5),(5,6),(5,7)]
# phase_operator_edge_list = [(0,1), (1,2), (2,3), (3,4), (3,5)]
# phase_operator_edge_list = [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)]
target_graph = nx.Graph()
target_graph.add_edges_from(phase_operator_edge_list)
no_edges = target_graph.number_of_edges()

phase_operator_edge_list2 = edge_list
# phase_operator_edge_list2 = [(0,3)]
# phase_operator_edge_list2 = [(0,1), (1,2),(1,3),(3,4),(3,5),(5,6),(5,7)]
# phase_operator_edge_list2 = [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)]
target_graph2 = nx.Graph()
target_graph2.add_edges_from(phase_operator_edge_list2)
no_edges2 = target_graph2.number_of_edges()


use_different_phase_operators = use_different_phase_operators and depth > 1 and depth < 3
if use_different_phase_operators:
    print("phase operator1 edges: \n", phase_operator_edge_list)
    print("phase operator2 edges: \n", phase_operator_edge_list2)
else:
    print("phase operator edges: \n", phase_operator_edge_list)
    phase_operator_edge_list2 = phase_operator_edge_list
    use_different_phase_operators = False


print("edges:\n", edge_list)
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
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]

#-------------------------------------------------------------------------
for i in range(10):
    print(f'layers:{depth} specific_graph MA-All')

    def obj_func(parameter_values):
        if(use_different_phase_operators):
            dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values[:no_vertices + no_edges], 1, pauli_ops_dict, 'All')
            dens_mat = build_operators.build_MA_qaoa_ansatz_from_initial_dens(target_graph2, parameter_values[no_vertices + no_edges:], 1, pauli_ops_dict, 'All', initial_density=dens_mat)
        else:
            dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values, depth, pauli_ops_dict, 'All')

        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    if use_different_phase_operators:
        initial_parameter_guesses = [random.random() * 3 for _ in range(depth * (no_vertices) + no_edges + no_edges2)]
        bounds = [(0, 6.2832)] * (no_edges2 + no_edges) + [(0, 6.2832)] * (depth * no_vertices)
    else:
        initial_parameter_guesses = [random.random() * 3 for _ in range(depth * (no_edges + no_vertices))]
        bounds = [(-3.1416, 3.1416)] * (depth * no_edges) + [(0, 6.2832)] * (depth * no_vertices)
    # initial_parameter_guesses = [gamma_0] * (depth * no_edges) + [beta_0] * (depth * no_vertices)
    result = minimize(obj_func, initial_parameter_guesses,  method="BFGS")
    # result = minimize(obj_func, initial_parameter_guesses, bounds=bounds, method="Nelder-Mead")

    parameter_list = list(result.x)

    if(use_different_phase_operators):
        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list[:no_vertices+no_edges], 1, pauli_ops_dict, 'All')
        dens_mat = build_operators.build_MA_qaoa_ansatz_from_initial_dens(target_graph2, parameter_list[no_vertices+no_edges:], 1, pauli_ops_dict, 'All', initial_density=dens_mat)
    else:
        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, depth, pauli_ops_dict, 'All')

    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    print('***************')
    print(f'cut_approx_ratio: {cut_approx_ratio}')
    if(save):
        with open(f"./results/specific_graph/MA{no_vertices}_layer{depth}_{edge_list != phase_operator_edge_list}.csv", 'a') as f:
            if depth == 2:
                f.write(f"MA_QAOA, {depth}, {edge_list != phase_operator_edge_list} , {edge_list}, {phase_operator_edge_list}, {phase_operator_edge_list2}, {cut_approx_ratio}\n")
            else:
                f.write(f"MA_QAOA, {depth}, {edge_list!=phase_operator_edge_list}, {edge_list}, {phase_operator_edge_list}, {cut_approx_ratio}\n")

    if(saveFig):
        pdf_pages = PdfPages(f"./results/specific_graph/MA{no_vertices}_layer{depth}.pdf")

    for layer in range(depth):
        print(f'layer {layer + 1:}')
        if use_different_phase_operators:
            if(layer == 0):
                print(parameter_list[:no_edges])
                print(parameter_list[no_edges:no_edges + no_vertices])
            else:
                print(parameter_list[no_vertices+no_edges:no_vertices+no_edges + no_edges2])
                print(parameter_list[no_vertices+no_edges + no_edges2:])

        else:
            my_dict = {key: value for key, value in zip(target_graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])} # gamma for every edge
            for key, value in my_dict.items():
                print(f"{key}: {value:.4f}")
            print(f'beta: {[round(num, 3) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')

        if(saveFig):
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

    if(saveFig):
        pdf_pages.close()
    
    print('------------------------------------------------')