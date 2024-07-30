import networkx as nx
import matplotlib.pylab  as plt
import re
import ast
from matplotlib.backends.backend_pdf import PdfPages

def read_parameters(file_path, rounding):
    gammas = []
    betas = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('('):
                gammas += [float(line.split(' ')[2])]
            if line.startswith("beta"):
                match = re.search(r'\[([^\]]+)\]', line)
                numbers_string = match.group(0)
                numbers_list = ast.literal_eval(numbers_string)
                betas += numbers_list
    
    parameter_list = gammas + betas
    if rounding:
        for i in range(len(parameter_list)):
            if abs(parameter_list[i]) < 0.35:
                parameter_list[i] = 0;
            if parameter_list[i] > -0.9 and parameter_list[i] < -0.6:
                parameter_list[i] = -0.7854

    return parameter_list


def save_pic_para(file_path, parameter_list,save = False):
    if(save):
        with open(f"./results/parameters/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}", 'w') as f:
            f.write(f"max cut: {max_cut_solution[0]}\n")
            f.write(f'r: {cut_approx_ratio}\n')
    if(save):
        pdf_pages = PdfPages(f"./results/figures/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}.pdf")

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
            # plt.savefig(f"./results/figures/{no_vertices}vertex/MA{no_vertices}_{graph_type[1]}{graph_type[0]}_layer{depth}_seed{seed}.png")
            pdf_pages.savefig()
            plt.close()

    if(save):
        pdf_pages.close()