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

def generate_connected_graph(n, p, seed, weights = False):
    """
    generate every edge with probability p
    """
    print(f'random graph  no_v:{n} p:{p} seed:{seed} ' )

    # graph = nx.Graph()
    # random.seed(seed)
    # edge_list = []
    # has_edge = [False] * n
    # for n1 in range(n):
    #     for n2 in range(n1+1,n):
    #         if(random.random() > p):
    #             edge_list.append((n1,n2))
    #             has_edge[n1] = True
    #             has_edge[n2] = True
    
    # for i in range(n):
    #     if(has_edge[i] == False):
    #         edge_list.append((i, (i+1)%n))
    
    # graph.add_edges_from(edge_list)

    graph = nx.erdos_renyi_graph(n, p, seed = seed)
    edge_list = list(graph.edges())

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

def generate_graph_type(n, type, seed, weights = False):
    if type[0] == "regular":
        return generate_regular_graph(n, type[1], seed, weights)
    if type[0] == 'random':
        return generate_connected_graph(n,type[1], seed, weights)