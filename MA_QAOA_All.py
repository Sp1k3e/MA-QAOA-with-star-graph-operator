import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import math
import matplotlib.pyplot as plt
    
def MA_All(no_vertices, depth, seed, graph_type = 'regular', save = True):
    # no_vertices = 8
    # depth = 1
    # seed = 4
    p = 0.4
    graph = generate_graphs.generate_connected_graph(no_vertices, seed, p)[0]
    # graph = generate_graphs.generate_regular_graph(no_vertices, 3, seed)[0]

    no_edges = graph.number_of_edges()

    print(f'layers:{depth} MA-All')

    pauli_ops_dict = build_operators.build_all_paulis(no_vertices)
    gamma_0 = 0.7
    beta_0 = 0.0

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    print(f"max cut: {max_cut_solution[0]}")
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]

    hamiltonian = build_operators.cut_hamiltonian(graph)
    #! 初始化完成

    def obj_func(parameter_values):
        dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_values, depth, pauli_ops_dict, 'All')
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    # 全改
    initial_parameter_guesses = [gamma_0] * (depth * no_edges) + [beta_0] * (depth * no_vertices)

    result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

    #! 输出结果
    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_list, depth, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    print(f'cut_approx_ratio: {cut_approx_ratio}')

    for layer in range(depth):
        print('-----------------------------------------------')
        print(f'layer {layer + 1:}')
        my_dict = {key: value for key, value in zip(graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])}
        # print(f'gamma: {my_dict}')
        for key, value in my_dict.items():
            print(f"{key}: {value:.4f}")
            my_dict[key] = format(my_dict[key], '.3f')
        print(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')

        #todo 存数据
        if(save):
            plt.clf()
            l_dict = {}
            for n in range(no_vertices):
                l_dict[n] = round(parameter_list[depth * no_edges + layer * no_vertices + n] ,3)
            pos = nx.spring_layout(graph)
            nx.draw_networkx_nodes(graph, pos)
            nx.draw_networkx_edges(graph, pos)
            nx.draw_networkx_edge_labels(graph, pos, my_dict)
            nx.draw_networkx_labels(graph, pos, l_dict)
            # plt.show()
            plt.savefig(f"./results/figures/MA{no_vertices}{graph_type}_seed{seed}.png")

print('-----------------------------------------------')