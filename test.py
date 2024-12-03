import networkx as nx
from src_code import generate_graphs
import matplotlib.pyplot as plt
from collections import Counter

def find_edge_in_most_triangles(graph):
    # 获取所有三角形
    triangles = [tuple(sorted(triangle)) for triangle in nx.enumerate_all_cliques(graph) if len(triangle) == 3]
    
    # 统计边的出现次数
    edge_counter = Counter()
    for triangle in triangles:
        edges = [(triangle[i], triangle[j]) for i in range(3) for j in range(i+1, 3)]
        edge_counter.update(edges)
    
    # 找到出现次数最多的边
    max_edge = max(edge_counter, key=edge_counter.get)
    max_count = edge_counter[max_edge]
    
    return max_edge, max_count

seed = 1

# for seed in range(100):
G = nx.Graph()
G = generate_graphs.generate_graph_type(8,['random',0.5],seed)[0]

pos = nx.spring_layout(G)
label_pos = {k: (v[0], v[1] + 0.1) for k, v in pos.items()}
nx.draw_networkx_labels(G, label_pos, font_color="g", font_size=10)
nx.draw(G, pos)
plt.show()

# edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 0), (2, 3)]
# G.add_edges_from(edges)

result = find_edge_in_most_triangles(G)
print(G.edges())
print(f"出现次数最多的边是 {result[0]}，出现在 {result[1]} 个三角形中")
# print(result[0][0], result[0][1])
G.remove_edge(result[0][0], result[0][1])
print(G.edges())
# G.remove_edge(4,6)

nx.draw(G, pos)
nx.draw_networkx_labels(G, label_pos, font_color="g", font_size=10)
plt.show()