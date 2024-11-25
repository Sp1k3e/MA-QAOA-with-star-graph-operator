from src_code import generate_graphs
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

def draw(graph, depth, parameter_list, graph_type, seed, ar, path):
    pdf_pages = PdfPages(path)
    no_edges = graph.num_of_edges()
    no_vertices = graph.num_of_nodes()

    for layer in depth:
        my_dict = {key: value for key, value in zip(graph.edges, parameter_list[layer * no_edges : (layer + 1) * no_edges])} # gamma for every edge
        for key, value in my_dict.items():
            print(f"{key}: {value:.4f}")
        print(f'beta: {[round(num, 4) for num in parameter_list[depth * no_edges + layer * no_vertices:depth * no_edges + (layer + 1) * no_vertices]]}')

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
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_edge_labels(graph, pos, my_dict, font_size=8) #每条边的gamma
        nx.draw_networkx_labels(graph, pos, l_dict, font_size=10) #每个点的beta
        for i in range(no_vertices):
            pos[i] += np.array([-0.06, 0.06]) 
        # nx.draw_networkx_labels(graph, pos, {key:value for key, value in zip(range(no_vertices), max_cut_solution[0])}, font_color= "r", alpha=0.8,font_size=10) #最大割的分组
        for i in range(no_vertices):
            pos[i] += np.array([0.0, -0.12]) 
        nx.draw_networkx_labels(graph, pos, font_color="g", font_size=10)

        plt.title(f'MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}  r:{ar}')
        pdf_pages.savefig()
        plt.close()

        pdf_pages.close()