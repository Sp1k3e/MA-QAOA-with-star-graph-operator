import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time
from collections import Counter
import random
    
def mst_MA(no_vertices, depth, seed, graph_type, save = True):
    '''
    using mst to choose edges that need to be optimized
    '''
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
    '''
    select nodes to be 0 (from largest drgee 
    and its edges that connect all other -4/pi nodes
    '''
    gamma_0 = -1.5708
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

    #! 选择优化的点和边
    connected_v = [False] * graph.number_of_nodes()
    edges = graph.edges()
    degrees = dict(graph.degree())
    sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
    selected_v = []
    selected_e = []

    #! 从度数较大的点找0点 
    #todo 重写为函数
    for n in sorted_nodes: #n[0]为点
        if connected_v[n[0]]:
            for n1 in sorted_nodes:
                if n[1] == n1[1] and connected_v[n1[0]] == False:
                    index1 = sorted_nodes.index(n)
                    index2 = sorted_nodes.index(n1)
                
                    sorted_nodes[index1], sorted_nodes[index2] = sorted_nodes[index2], sorted_nodes[index1]
                    n = n1
        selected_v += [n[0]]
        connected_v[n[0]] = True 
        first = True 
        for edge in edges:
            if n[0] == edge[0]:
                if not connected_v[edge[1]]: #如果边上另一点还没有被连接
                    connected_v[edge[1]] = True
                    selected_e += [(edge)]
                else: #边上另一点被连接
                    if edge[1] in selected_v:
                        continue
                    if first:
                        first =False
                        continue
                    # if first:
                        # first = False
                    for e in selected_e:
                        if edge[1] in e:
                            selected_e.remove(e)
                            break
                    # else:
                        # continue
                    selected_e += [(edge)]

            elif n[0] == edge[1]:
                if not connected_v[edge[0]]:
                    connected_v[edge[0]] = True
                    selected_e += [(edge)]
                else:
                    if edge[0] in selected_v:
                        continue
                    if first:
                        first =False
                        continue
                    # if first:
                        # first = False
                    for e in selected_e:
                        if edge[0] in e:
                            selected_e.remove(e)
                            break
                    # else:
                        # continue
                    selected_e += [(edge)]

        if all(x == True for x in connected_v):
            break

    print(f'selected nodes:{selected_v}')
    print(f'selected edges:{selected_e}')
    
    #! 只在目标图上优化
    target_graph = nx.Graph()
    target_graph.add_edges_from(selected_e)
    for index, edge in enumerate(target_graph.edges()):
        target_graph.get_edge_data(*edge)['weight'] = 1

    betas = []
    for node in graph.nodes():
        if node in selected_v:
            betas += [0]
        else:
            betas += [0.7854]

    #! 第一层
    def obj_func(parameter_values):
        #! 设置点beta为0和pi/4
        parameter_values = np.append(parameter_values, betas)
        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values, 1, pauli_ops_dict, 'All')
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    initial_parameter_guesses = [gamma_0] * (target_graph.number_of_edges())
    result = minimize(obj_func, initial_parameter_guesses, method="Nelder-Mead")

    #! 输出结果
    parameter_list = list(result.x)
    parameter_list = parameter_list + betas
    dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, 1, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    tmp_list = []
    i = 0
    #! 填充parameter_list中的gamma为0的边
    for _ in depth:
        for edge in graph.edges():
            if edge not in selected_e:
                tmp_list += [0]
            else: 
                tmp_list += [parameter_list[i]]
                i += 1
    tmp_list += parameter_list[i:]
    parameter_list = tmp_list

    """    ! 后几层
    if depth > 1:
        print(f"layer1 r:{cut_approx_ratio}")
        depth2 = depth - 1
        def obj_func2(parameter_values):
            #! 设置点beta为0和pi/4
            dens_mat2 = build_operators.build_MA_qaoa_ansatz_from_initial(graph, parameter_values, depth2, pauli_ops_dict, 'All', dens_mat)
            expectation_value = (hamiltonian * dens_mat2).trace().real
            return expectation_value * (-1.0)

        initial_parameter_guesses = [gamma_0] * (depth2 * no_edges) + [beta_0] * (depth2 * no_vertices)
        result = minimize(obj_func2, initial_parameter_guesses, method="BFGS")

        parameter_list2 = list(result.x)
        gammas = parameter_list[:no_edges] + parameter_list2[:depth2 * no_edges]
        betas = parameter_list[no_edges:] + parameter_list2[depth2 * no_edges:]
        parameter_list = gammas + betas

        dens_mat2 = build_operators.build_MA_qaoa_ansatz_from_initial(graph, parameter_list2, depth2, pauli_ops_dict, 'All', dens_mat)
        hamiltonian_expectation = (hamiltonian * dens_mat2).trace().real
        cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value
    """

    #! 输出所有parameter
    print(f'layers:{depth} heuristic_MA')
    print('***************')
    print(f'cut_approx_ratio: {cut_approx_ratio}')
    with open("./results/tmp.csv", "a") as f:
        f.write(f'select,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio}\n')
    # 保存最优参数
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
                f.write(f'{parameter_list}')

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
            plt.savefig(f"./results/figures/heuristic/heuristic_MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}.png")

    print('-----------------------------------------------')

    #! 根据参数得出割
    # if(layer == 1):
    #     cut = []
    #     for node in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]:
    #         if node == 0:
    #             cut += [1]
    #         else:


def star_graph_MA(no_vertices, depth, seed, graph_type, save = True):
    """
    star graph phase operator
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

    simulation_time = []

    def obj_func(parameter_values):
        start_time = time.time()

        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values, 1, pauli_ops_dict, 'All')

        simulation_time.append(time.time() - start_time)

        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    start_time = time.time()

    # initial_parameter_guesses = [gamma_0] * (target_graph.number_of_edges() * depth) + [beta_0] * (no_vertices * depth)
    initial_parameter_guesses = [random.random() * 3 for _ in range(no_vertices + target_graph.number_of_edges())]
    result = minimize(obj_func, initial_parameter_guesses, method="BFGS")
    # result = minimize(obj_func, initial_parameter_guesses, method="Nelder-Mead")

    end_time = time.time()
    execution_time = end_time - start_time
    # hours = int(execution_time // 3600)
    # minutes = int((execution_time % 3600) // 60)
    # seconds = execution_time % 60
    # print(f"Minimize function took {hours}h {minutes}m {seconds:.2f}s.")

    #! 输出结果
    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, 1, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value
    # print(parameter_list)


    #! 输出结果
    print(f'layers:{depth} star_graph_MA')

    print("目标函数总调用次数:", result.nfev)
    print(f'total iteration: {result.nit}')
    print(f"Minimize time: {execution_time}s")
    print(f"simulation time: {sum(simulation_time)}s")
    print(f'cut_approx_ratio: {cut_approx_ratio}')

    print('-----------------------------------------------')

    # if(save):
    #     with open(f"./results/star-graph/star-graph{depth}.csv", "a") as f:
    #         f.write(f'star_graph,{no_vertices},{graph_type[0] + str(graph_type[1])},{depth},{seed},{cut_approx_ratio}\n')


    if(save and cut_approx_ratio > 0.99):
        with open("./results/tmp_star_graph.csv", "a") as f:
            # f.write(f'star_graph,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio}, {result.nit}, {execution_time}\n')
            f.write(f'star-graph,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio}, {result.nfev}, {result.nit}, {execution_time}, {sum(simulation_time)}\n')

    return cut_approx_ratio

    """ 
    tmp_list = []
    i = 0
    # 填充parameter_list中的gamma为0的边
    for _ in range(depth):
        for edge in graph.edges():
            if edge not in selected_e:
                tmp_list += [0]
            else: 
                tmp_list += [parameter_list[i]]
                i += 1
    tmp_list += parameter_list[i:]
    parameter_list = tmp_list
    """
    # 保存最优参数
    # if(save):
    #     with open(f"./results/parameters/heuristic/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}", 'w') as f:
    #         f.write(parameter_list)

    """ 
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
                f.write(f'{parameter_list}')

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
            plt.savefig(f"./results/figures/heuristic/heuristic_MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}.png")
    """


# def random_graph_MA(no_vertices, depth, seed, graph_type, save = True):


def sub_graph_MA(no_vertices, depth, seed, graph_type, save = True):
    '''
    random sub graph phase operator MA-QAOA
    '''
    gamma_0 = 1.5708
    beta_0 = 0.7854
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]
    if nx.is_connected(graph) == False:
        print("bad seed, disconnected graph")
        return

    no_edges = graph.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
    hamiltonian = build_operators.cut_hamiltonian(graph)

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]
    #! 初始化完成------------------------------------------------

    #! 只在目标图上优化
    target_graph = nx.minimum_spanning_tree(graph)

    if nx.is_connected(target_graph) == False:
        print("bad seed, disconnected graph")
        return
    selected_e = target_graph.edges()
    # print(f'selected edges:{selected_e}')


    def obj_func(parameter_values):
        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values, depth, pauli_ops_dict, 'All')
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    start_time = time.time()

    initial_parameter_guesses = [gamma_0] * (target_graph.number_of_edges() * depth) + [beta_0] * (no_vertices * depth)
    #! Nelder-Mead比BFDS好很多
    result = minimize(obj_func, initial_parameter_guesses, method="Nelder-Mead")

    end_time = time.time()
    execution_time = end_time - start_time
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = execution_time % 60
    print(f"Minimize function took {hours}h {minutes}m {seconds:.2f}s.")

    #! 输出结果
    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, depth, pauli_ops_dict, 'All')
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

    print(f'layers:{depth} subgraph_MA')
    # print('***************')
    print(f'cut_approx_ratio: {cut_approx_ratio}')
    print('----------------------------------------------------')

    if(save):
        with open(f"./results/MA-QAOA/subgraph_MA_Ne_{depth}.csv", "a") as f:
            f.write(f'subgraph_MA,{no_vertices},{graph_type[0]+str(graph_type[1])},{depth},{seed},{cut_approx_ratio}\n')


def TR_MA(no_vertices, depth, seed, graph_type, TR_type, save = True, minimize_method = "BFGS"):
    '''
    triangle removal phase operator MA-QAOA
    '''
    gamma_0 = 1.5708
    beta_0 = 0.7854
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]
    if nx.is_connected(graph) == False:
        print("bad seed, disconnected graph")
        return

    no_edges = graph.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
    hamiltonian = build_operators.cut_hamiltonian(graph)

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]
    #! 初始化完成------------------------------------------------

    #! 只在目标图上优化
    target_graph = graph
    triangles = [cycle for cycle in nx.cycle_basis(target_graph) if len(cycle) == 3]
    if(TR_type == 'All'):
        for triangle in triangles:
        # 随机移除三角形中的一条边
            u, v = triangle[0], triangle[1]
            if target_graph.has_edge(u, v):
                target_graph.remove_edge(u, v)
                
    if(TR_type == 'All_without_Most'):
        edge_counter = Counter()
        for triangle in triangles:
            edges = [(triangle[i], triangle[j]) for i in range(3) for j in range(i+1, 3)]
            edge_counter.update(edges)

        max_edge = max(edge_counter, key=edge_counter.get)

        # flag = False
        for triangle in triangles:
            u, v = triangle[0], triangle[1]
            if (u, v) == max_edge or (v, u) == max_edge:
                v = triangle[2]
        # 随机移除三角形中的一条边
            if target_graph.has_edge(u, v): 
                target_graph.remove_edge(u, v)
    

    if(TR_type == 'Most'):
        # 移除出现在三角形中最多的一条边
        # 统计边的出现次数
        edge_counter = Counter()
        for triangle in triangles:
            edges = [(triangle[i], triangle[j]) for i in range(3) for j in range(i+1, 3)]
            edge_counter.update(edges)
        
        # 找到出现次数最多的边
        max_edge = max(edge_counter, key=edge_counter.get)
        # max_count = edge_counter[max_edge]
        
        target_graph.remove_edge(max_edge[0], max_edge[1])

    if nx.is_connected(target_graph) == False:
        print("bad seed, disconnected graph")
        return
    selected_e = target_graph.edges()
    # print(f'selected edges:{selected_e}')


    def obj_func(parameter_values):
        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values, depth, pauli_ops_dict, 'All')
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    start_time = time.time()

    initial_parameter_guesses = [gamma_0] * (target_graph.number_of_edges() * depth) + [beta_0] * (no_vertices * depth)
    #! Nelder-Mead比BFDS好很多
    result = minimize(obj_func, initial_parameter_guesses, method=minimize_method)

    end_time = time.time()
    execution_time = end_time - start_time
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = execution_time % 60
    print(f"Minimize function took {hours}h {minutes}m {seconds:.2f}s.")

    #! 输出结果
    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, depth, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value
    # print(parameter_list)

    # tmp_list = []
    # i = 0
    # #! 填充parameter_list中的gamma为0的边
    # for _ in range(depth):
    #     for edge in graph.edges():
    #         if edge not in selected_e:
    #             tmp_list += [0]
    #         else: 
    #             tmp_list += [parameter_list[i]]
    #             i += 1
    # tmp_list += parameter_list[i:]
    # parameter_list = tmp_list

    print(f'layers:{depth} TR_{TR_type}_MA')
    print(f'total iteration: {result.nit}')
    print(f'cut_approx_ratio: {cut_approx_ratio}')
    print('----------------------------------------------------')

    if(save):
        with open(f"./results/MA-QAOA/TR_{TR_type}_MA_Ne_{depth}.csv", "a") as f:
            f.write(f'TR_{TR_type}_MA,{no_vertices},{graph_type[0]+str(graph_type[1])},{depth},{seed},{cut_approx_ratio}\n')



# def MDER_MA(no_vertices, depth, seed, graph_type, save = True):

def longest_path_MA(no_vertices, depth, seed, graph_type, save = True):
    '''
    triangle removal phase operator MA-QAOA
    '''
    gamma_0 = 1.5708
    beta_0 = 0.7854
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]
    if nx.is_connected(graph) == False:
        print("bad seed, disconnected graph")
        return

    no_edges = graph.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
    hamiltonian = build_operators.cut_hamiltonian(graph)

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]
    #! 初始化完成------------------------------------------------

    #! 只在目标图上优化
    target_graph = graph

    selected_e = target_graph.edges()


    def obj_func(parameter_values):
        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values, depth, pauli_ops_dict, 'All')
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    start_time = time.time()

    initial_parameter_guesses = [gamma_0] * (target_graph.number_of_edges() * depth) + [beta_0] * (no_vertices * depth)
    result = minimize(obj_func, initial_parameter_guesses, method="BFGS")

    end_time = time.time()
    execution_time = end_time - start_time
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = execution_time % 60
    print(f"Minimize function took {hours}h {minutes}m {seconds:.2f}s.")

    #! 输出结果
    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, depth, pauli_ops_dict, 'All')
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

    #! 输出所有parameter
    print(f'layers:{depth} TR_MA')
    print('***************')
    print(f'cut_approx_ratio: {cut_approx_ratio}')

    with open("./results/MA-QAOA/TR_MA.csv", "a") as f:
        f.write(f'TR_ALL_MA,{no_vertices},{graph_type[0]+str(graph_type[1])},{depth},{seed},{cut_approx_ratio}\n')


def complete_MA(no_vertices, depth, seed, graph_type, TR_type, save = True):
    '''
    complete graph phase operator MA-QAOA
    '''
    gamma_0 = 1.5708
    beta_0 = 0.7854
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]
    if nx.is_connected(graph) == False:
        print("bad seed, disconnected graph")
        return

    no_edges = graph.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices) 
    hamiltonian = build_operators.cut_hamiltonian(graph)

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]
    #! 初始化完成------------------------------------------------

    #! 只在目标图上优化
    target_graph = nx.complete_graph(no_vertices)

    weights = [1 for i in range(len(target_graph.edges()))]
    for index, edge in enumerate(target_graph.edges()):
        target_graph.get_edge_data(*edge)['weight'] = weights[index]

    if nx.is_connected(target_graph) == False:
        print("bad seed, disconnected graph")
        return
    selected_e = target_graph.edges()
    # print(f'selected edges:{selected_e}')


    def obj_func(parameter_values):
        dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_values, depth, pauli_ops_dict, 'All')
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    start_time = time.time()

    initial_parameter_guesses = [gamma_0] * (target_graph.number_of_edges() * depth) + [beta_0] * (no_vertices * depth)
    #! Nelder-Mead比BFDS好很多
    result = minimize(obj_func, initial_parameter_guesses, method="Nelder-Mead")

    end_time = time.time()
    execution_time = end_time - start_time
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = execution_time % 60
    print(f"Minimize function took {hours}h {minutes}m {seconds:.2f}s.")

    #! 输出结果
    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(target_graph, parameter_list, depth, pauli_ops_dict, 'All')
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value
    # print(parameter_list)

    

    print(f'layers:{depth} TR_{TR_type}_MA')
    print(f'cut_approx_ratio: {cut_approx_ratio}')
    print('----------------------------------------------------')

    if(save):
        with open(f"./results/MA-QAOA/complete_MA_Ne_{depth}.csv", "a") as f:
            f.write(f'complete_MA,{no_vertices},{graph_type[0]+str(graph_type[1])},{depth},{seed},{cut_approx_ratio}\n')