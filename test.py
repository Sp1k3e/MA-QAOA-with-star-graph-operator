import networkx as nx
from networkx.algorithms.approximation import steiner_tree

# 创建一个无向图
G = nx.Graph()

# 添加边（节点之间的连接和权重）
G.add_weighted_edges_from([
    (1, 2, 3),
    (2, 3, 1),
    (3, 4, 2),
    (1, 4, 4),
    (2, 4, 5),
    (1, 3, 10)
])

# 需要连接的节点
terminals = [1, 3, 4]

# 计算 Steiner 树
steiner = steiner_tree(G, terminals)

# 打印 Steiner 树中的边
print("Edges in the Steiner tree:")
print(sorted(steiner.edges(data=True)))
print(type(steiner))

b = [1]
b += [2]
print(b)