import networkx
import random

def generate_complete_graph(n, seed, weights = False):
    """

    """

    graph = networkx.Graph()
    edge_list = []
    for n1 in range(n):
        for n2 in range(n1+1,n):
            edge_list.append((n1,n2))
    
    graph.add_edges_from(edge_list)
    random.seed(seed)
    if weights:
        weights = [random.random() for i in range(len(edge_list))]
    else:
        weights = [1 for i in range(len(edge_list))]

    for index, edge in enumerate(graph.edges()):
        graph.get_edge_data(*edge)['weight'] = weights[index]

    return graph, weights


def generate_connected_graph(n, seed, p=0.2, weights = False):
    """

    """
    # print(f'graph type:random graph  no_v:{n} seed:{seed} p:{p}' )

    graph = networkx.Graph()
    random.seed(seed)
    edge_list = []
    for n1 in range(n):
        for n2 in range(n1+1,n):
            if(random.random() > p):
                edge_list.append((n1,n2))
        # edge_list.append((n1,n1+1))
    
    graph.add_edges_from(edge_list)
    if weights:
        weights = [random.random() for i in range(len(edge_list))]
    else:
        weights = [1 for i in range(len(edge_list))]

    for index, edge in enumerate(graph.edges()):
        graph.get_edge_data(*edge)['weight'] = weights[index]

    return graph, weights


# import matplotlib.pyplot as plt
# graph = generate_connected_graph(6, 1)[0]
# networkx.draw_networkx(graph)
# plt.show()