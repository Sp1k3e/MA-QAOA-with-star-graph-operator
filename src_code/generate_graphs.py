import networkx as nx
import random

def generate_complete_graph(n, seed, weights = False):
    """

    """

    graph = nx.Graph()
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
    print(f'random graph  no_v:{n} seed:{seed} p:{p}' )

    graph = nx.Graph()
    random.seed(seed)
    edge_list = []
    has_edge = [False] * n
    for n1 in range(n):
        for n2 in range(n1+1,n):
            if(random.random() > p):
                edge_list.append((n1,n2))
                has_edge[n1] = True
                has_edge[n2] = True
    
    for i in range(n):
        if(has_edge[i] == False):
            edge_list.append((i, (i+1)%n))
    
    graph.add_edges_from(edge_list)
    if weights:
        weights = [random.random() for i in range(len(edge_list))]
    else:
        weights = [1 for i in range(len(edge_list))]

    for index, edge in enumerate(graph.edges()):
        graph.get_edge_data(*edge)['weight'] = weights[index]

    return graph, weights

def generate_regular_graph(n, d, seed , weights = False):
    '''
    generate regular graph(no_vertices, degree, seed, if_weights)
    '''
    
    print(f'{d}-regular graph  no_v:{n} seed:{seed}')

    graph = nx.random_regular_graph(d,n,seed)
    edge_list = list(graph.edges())

    if weights:
        weights = [random.random() for i in range(len(edge_list))]
    else:
        weights = [1 for i in range(len(edge_list))]

    for index, edge in enumerate(graph.edges()):
        graph.get_edge_data(*edge)['weight'] = weights[index]

    return graph, weights


def generate_graph_type(n, d, seed, type, weights = False):
    if type == "regular":
        generate_regular_graph(n, d, seed, weights)
    if type == 'random':
        generate_connected_graph(n, seed, p)