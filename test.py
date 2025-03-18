import networkx as nx
from src_code import generate_graphs
import matplotlib.pyplot as plt
from collections import Counter


seed = 0
remove = 0

for seed in range(100):
    if seed == 92:
        continue
    G = nx.Graph()
    G = generate_graphs.generate_graph_type(8,['random',0.5],seed)[0]
    target_graph = G

    triangles = [cycle for cycle in nx.cycle_basis(G) if len(cycle) == 3]

    edge_counter = Counter()
    for triangle in triangles:
        edges = [(triangle[i], triangle[j]) for i in range(3) for j in range(i+1, 3)]
        edge_counter.update(edges)
    
    # 找到出现次数最多的边
    max_edge = max(edge_counter, key=edge_counter.get)
    # max_count = edge_counter[max_edge]
        
    # print(max_edge[0], max_edge[1])

    for triangle in triangles:
        # 随机移除三角形中的一条边
        u, v = triangle[0], triangle[1]
        if target_graph.has_edge(u, v):
            target_graph.remove_edge(u, v)
            # print(u,v,end=',')
            if(u== max_edge[0] and v == max_edge[1]):
                print('true')
                remove+=1
            if(u== max_edge[1] and v == max_edge[0]):
                print('true')
                remove+=1
    # print()

print(remove)