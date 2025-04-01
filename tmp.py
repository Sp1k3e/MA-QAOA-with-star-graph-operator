import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import time
import random

def star_graph_MA(no_vertices, depth, seed, graph_type, save = True):
    """
    """
    gamma_0 = 1.5708
    beta_0 = 0.7854
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]
    if nx.is_connected(graph) == False:
        return

    no_edges = graph.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
    hamiltonian = build_operators.cut_hamiltonian(graph)

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    # print(f"max cut: {max_cut_solution[0]}")
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


    def obj_func(parameter_values):
        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values, 1, pauli_ops_dict, 'All')
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    start_time = time.time()

    initial_parameter_guesses = [gamma_0] * (target_graph.number_of_edges() * depth) + [beta_0] * (no_vertices * depth)
    # initial_parameter_guesses = [ random.random()*3 for _ in range(2*no_vertices-1)]
    result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

    end_time = time.time()
    execution_time = end_time - start_time
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = execution_time % 60
    print(f"Minimize function took {hours}h {minutes}m {seconds:.2f}s.")

    #! 输出结果
    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, 1, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value
    # print(parameter_list)

    tmp_list = []
    i = 0
    #! 填充parameter_list中的gamma为0的边
    for _ in range(depth):
        for edge in graph.edges():
            if edge not in selected_e:
                tmp_list += [0]
            else: 
                tmp_list += [parameter_list[i]]
                i += 1
    tmp_list += parameter_list[i:]
    parameter_list = tmp_list

    #! 输出结果
    print(f'layers:{depth} star_graph_MA')
    print(f'total iteration: {result.nit}')
    print(f'cut_approx_ratio: {cut_approx_ratio}')

    if(save):
        with open("./tmp.csv", "a") as f:
            f.write(f'star_graph,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio}, {result.nit}, {execution_time}\n')
    # 保存最优参数
    # if(save):
    #     with open(f"./results/parameters/heuristic/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}", 'w') as f:
    #         f.write(parameter_list)

    print('-----------------------------------------------')


n = 8
seed = 0
graph_type = ['random', 0.5]
# graph_type = ['random', 0.7]
# graph_type = ['regular', 3]
#! save
save = True
show = False

minimize_method = 'BFGS'
layer = 1

# for seed in range (0,100):
seed = 0
star_graph_MA(n, layer, seed, graph_type)