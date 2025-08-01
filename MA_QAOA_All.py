import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import random
    
def MA_All(no_vertices, depth, seed, graph_type, save = False, show = False, minimize_method = 'BFGS'):
    gamma_0 = 1
    beta_0 = 0.7854
    graph = generate_graphs.generate_graph_type(no_vertices, graph_type, seed)[0]

    no_edges = graph.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices)
    hamiltonian = build_operators.cut_hamiltonian(graph)

    max_cut_solution = useful_methods.find_optimal_cut(graph)
    max_cut_value = max_cut_solution[1]
    max_ham_eigenvalue = max_cut_solution[2]
    # print(f"minimize_method: {minimize_method}")
    print(f'layers:{depth} MA-All')

    simulation_time = []

    def obj_func(parameter_values):
        start_time = time.perf_counter()

        dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_values, depth, pauli_ops_dict, 'All')

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        # seconds = execution_time % 60
        # print(f"One round simulation took {minutes}m {seconds:.2f}s.")
        simulation_time.append(execution_time)

        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    start_time = time.perf_counter()

    # initial_parameter_guesses = [gamma_0] * (depth * no_edges) + [beta_0] * (depth * no_vertices)
    initial_parameter_guesses = [random.random() * 3 for _ in range(depth * (no_edges + no_vertices))] 
    # print(initial_parameter_guesses)
    result = minimize(obj_func, initial_parameter_guesses, method=minimize_method)

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    #! 输出结果
    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(graph, parameter_list, depth, pauli_ops_dict, 'All')

    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    # print('***************')
    print("目标函数总调用次数:", result.nfev)
    print(f'total iteration: {result.nit}')
    print(f"Minimize time: {execution_time}s")
    print(f"simulation time: {sum(simulation_time)}s")
    print(f'cut_approx_ratio: {cut_approx_ratio}')

    if(save):
        with open(f"./results/tmp_MA{depth}.csv", "a") as f:
            f.write(f'MA-QAOA,{no_vertices},{graph_type},{depth},{seed},{cut_approx_ratio},{result.nfev}, {result.nit}, {execution_time}, {sum(simulation_time)}\n')

    # save optimal parameters
    # with open(f"./results/parameters/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}", 'w') as f:
    #     f.write(f"max cut: {max_cut_solution[0]}\n")
    #     f.write(f'r: {cut_approx_ratio}\n')
        # f.write(parameter_list)

    # 画图
    if(save and show):
        pdf_pages = PdfPages(f"./results/figures/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}.pdf")
        for layer in range(depth):
            print('-----------------------------------------------')
            print(f'layer {layer + 1:}')
            my_dict = {key: value for key, value in zip(graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])} # gamma for every edge
            for key, value in my_dict.items():
                print(f"{key}: {value:.4f}")
            print(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')

            # save parameters
            # with open(f"./results/parameters/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}", 'a') as f:
            #     f.write(f'layer {layer + 1:}\n')
            #     for key, value in my_dict.items():
            #         f.write(f"{key}: {value:.4f}\n")
            #         my_dict[key] = format(my_dict[key], '.2f')
            #     f.write(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}\n')

            # draw parameter graph
            plt.clf()
            l_dict = {}
            for n in range(no_vertices):
                l_dict[n] = round(parameter_list[depth * no_edges + layer * no_vertices + n] ,2)
            if layer == 0:
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

            plt.title(f'MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{layer + 1}_seed{seed}  r:{cut_approx_ratio}')
            # plt.savefig(f"./results/figures/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}.png")
            if(show):
                plt.show()
            if(save):
                pdf_pages.savefig()
                plt.close()
                pdf_pages.close()

    print('-----------------------------------------------')

    return cut_approx_ratio