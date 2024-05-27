import networkx as nx
from src_code import get_data
import random

def generate_graph(n, seed=1):

    graph = nx.Graph()
    edge_list = []
    for n_1 in range(n):

        for n_2 in range(n_1+1, n):

            edge_list.append((n_1, n_2))
            
    graph.add_edges_from(edge_list)

    random.seed(seed)
    weights = [random.random() for i in range(len(edge_list))]

    for index, edge in enumerate(graph.edges()):
        graph.get_edge_data(*edge)['weight'] = weights[index]

    return graph, weights

no_vertices = 4
graph = generate_graph(no_vertices)[0]
pos=nx.circular_layout(graph)
nx.draw_networkx(graph, pos)
labels = nx.get_edge_attributes(graph,'weight')
for edge in labels:
    labels[edge] = round(labels[edge], 3)
tmp = nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

from src_code import build_operators

hamiltonian = build_operators.cut_hamiltonian(graph=graph)
gradient_ops_dict = build_operators.build_all_mixers(graph=graph)