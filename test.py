from itertools import permutations
from src_code import generate_graphs
import networkx as nx

def longest_simple_path(G):
    # 找到所有连通分量
    components = nx.connected_components(G)
    longest_path = []
    for component in components:
        subgraph = G.subgraph(component)
        # 枚举所有节点排列，找到最长简单路径
        for path in permutations(subgraph.nodes):
            if all(subgraph.has_edge(path[i], path[i+1]) for i in range(len(path) - 1)):
                if len(path) > len(longest_path):
                    longest_path = path
    return longest_path

# 创建一个无向图
# G = nx.Graph()
# edges = [
    # (1, 2), (2, 3),(2,6), (3, 4), (4, 5), (7, 6), (8, 9), (9,10),(10,11)
# ]
# G.add_edges_from(edges)

for seed in range(100):
    G = generate_graphs.generate_graph_type(8, ['random', 0.5], seed)[0]

    path = longest_simple_path(G)
    print("Longest Path in Graph:", path)
    print("Longest Path Length:", len(path) - 1)
