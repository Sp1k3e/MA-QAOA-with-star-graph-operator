import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
    
def mst_MA(no_vertices, depth, seed, graph_type, save = True):
    gamma_0 = 0
    beta_0 = 0.785
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]

    no_edges = graph.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
    hamiltonian = build_operators.cut_hamiltonian(graph)

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    print(f"max cut: {max_cut_solution[0]}")
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]
    #! 初始化完成
    
    #! 选择优化的边
    mst = nx.minimum_spanning_tree(graph)
    mst_edges = mst.edges()

    def obj_func(parameter_values):
        dens_mat = build_operators.build_MA_qaoa_ansatz(mst, parameter_values, depth, pauli_ops_dict, 'All')
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    # initial_parameter_guesses = [gamma_0] * (depth * no_edges) + [beta_0] * (depth * no_vertices)
    initial_parameter_guesses = [gamma_0] * (mst.number_of_edges() * depth) + [beta_0] * (depth * no_vertices)
    result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

    #! 输出结果
    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(mst, parameter_list, depth, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    print(f'layers:{depth} MA-All')
    print('***************')
    print(f'cut_approx_ratio: {cut_approx_ratio}')
    if(save):
        with open(f"./results/parameters/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}", 'w') as f:
            f.write(f"max cut: {max_cut_solution[0]}\n")
            f.write(f'r: {cut_approx_ratio}\n')

    for layer in range(depth):
        print('-----------------------------------------------')
        print(f'layer {layer + 1:}')
        my_dict = {key: value for key, value in zip(graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])} # gamma for every edge
        for key, value in my_dict.items():
            print(f"{key}: {value:.4f}")
        print(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')

        if(save):
            with open(f"./results/parameters/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}", 'a') as f:
                f.write(f'layer {layer + 1:}\n')
                for key, value in my_dict.items():
                    f.write(f"{key}: {value:.4f}\n")
                    my_dict[key] = format(my_dict[key], '.2f')
                f.write(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}\n')

            # draw parameter graph
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
            plt.savefig(f"./results/figures/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}.png")

    print('-----------------------------------------------')

def select_MA(no_vertices, depth, seed, graph_type, save = True):
    gamma_0 = -0.7854
    beta_0 = 0.785
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]

    no_edges = graph.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
    hamiltonian = build_operators.cut_hamiltonian(graph)

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    print(f"max cut: {max_cut_solution[0]}")
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]
    #! 初始化完成------------------------------------------------

    #! 选择优化的点和边
    connected_v = [False] * graph.number_of_nodes()
    edges = graph.edges()
    degrees = dict(graph.degree())
    sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    selected_v = []
    selected_e = []

    #! 从度数较大的点找0点
    for n in sorted_nodes:
        selected_v += [n[0]]
        connected_v[n[0]] = True
        for edge in edges:
            # if n[0] in edge:
            if n[0] == edge[0]:
                if not connected_v[edge[1]]:
                    connected_v[edge[1]] = True
                    selected_e += [(edge)]
                else:
                    selected_e = [x for x in selected_e if edge[1] not in x]
                    selected_e += [(edge)]

        if all(x == True for x in connected_v):
            break
    
    print(f'selected edges:{selected_e}')
    
    #! 只在目标图上优化
    target_graph = nx.Graph();
    target_graph.add_edges_from(selected_e)
    for index, edge in enumerate(target_graph.edges()):
        target_graph.get_edge_data(*edge)['weight'] = 1

    def obj_func(parameter_values):
        for node in graph.nodes():
            if node in selected_v:
                parameter_values = np.append(parameter_values, 0)
            else:
                parameter_values = np.append(parameter_values, 0.7854)
        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values, depth, pauli_ops_dict, 'All')
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    # initial_parameter_guesses = [gamma_0] * (target_graph.number_of_edges() * depth) + [beta_0] * (depth * no_vertices)
    #todo 设置选中点为0
    initial_parameter_guesses = [gamma_0] * (target_graph.number_of_edges() * depth)
    result = minimize(obj_func, initial_parameter_guesses, method="Nelder-Mead")

    #! 输出结果
    parameter_list = list(result.x)
    for node in graph.nodes():
        if node in selected_v:
            parameter_list += [0]
        else:
            parameter_list += [0.7854]
    dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, depth, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    tmp_list = []
    i = 0
    #! 填充parameter_list
    for edge in graph.edges():
        if edge not in selected_e:
            tmp_list += [0]
        else: 
            tmp_list += [parameter_list[i]]
            i += 1
    tmp_list += parameter_list[i:]
    parameter_list = tmp_list

    print(f'layers:{depth} MA-All')
    print('***************')
    print(f'cut_approx_ratio: {cut_approx_ratio}')
    if(save):
        with open(f"./results/parameters/heuristic/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}", 'w') as f:
            f.write(f"max cut: {max_cut_solution[0]}\n")
            f.write(f'r: {cut_approx_ratio}\n')

    for layer in range(depth):
        print('-----------------------------------------------')
        print(f'layer {layer + 1:}')
        my_dict = {key: value for key, value in zip(graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])} # gamma for every edge
        for key, value in my_dict.items():
            print(f"{key}: {value:.4f}")
        print(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')

        if(save):
            with open(f"./results/parameters/heuristic/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}", 'a') as f:
                f.write(f'layer {layer + 1:}\n')
                for key, value in my_dict.items():
                    f.write(f"{key}: {value:.4f}\n")
                    my_dict[key] = format(my_dict[key], '.2f')
                f.write(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}\n')

            # draw parameter graph
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

            plt.title(f'select_MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}  r:{cut_approx_ratio}')
            plt.savefig(f"./results/figures/heuristic/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}.png")

    print('-----------------------------------------------')