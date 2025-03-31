import networkx as nx
from src_code import generate_graphs
import matplotlib.pyplot as plt
from src_code import build_operators
from src_code import useful_methods
from scipy.optimize import minimize
import time

for seed in range(100):
    no_vertices = 8
    graph_type = ['random',0.7]
    # seed = 97
    depth = 1
    save = False

    gamma_0 = 1.5708
    beta_0 = 0.7854
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]

    no_edges = graph.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
    hamiltonian = build_operators.cut_hamiltonian(graph)

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    # print(f"max cut: {max_cut_solution[0]}")
    max_cut_string = max_cut_solution[0]
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]
    #! 初始化完成------------------------------------------------

    selected_e = []
    for i in range(no_vertices - 1):
        selected_e += [(0, i + 1)]

    # print(f'selected edges:{selected_e}')

    #! 只在目标图上优化
    target_graph = nx.Graph()
    target_graph.add_edges_from(selected_e)
    for index, edge in enumerate(target_graph.edges()):
        target_graph.get_edge_data(*edge)['weight'] = 1

    parameter_list = []

    #直接构造参数，验证存在参数
    node0 = max_cut_string[0]
    for node in max_cut_string[1:]:
        if node == node0:
            parameter_list += [1.57]
        else:
            parameter_list += [-1.57]

    parameter_list += [1.57] + [0.7854] * (no_vertices-1)

    #! 输出结果
    dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, 1, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value
    # print(parameter_list)

    # print(f'layers:{depth} random_select_MA')
    print(f'cut_approx_ratio: {cut_approx_ratio}')

    if(save):
        with open("./results/star-graph/tmp.csv", "a") as f:
            f.write(f'star_graph,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio}\n')

    if (cut_approx_ratio - 0.99) < 0.005:
        print("false")

    print('-----------------------------------------------')