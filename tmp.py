import networkx as nx
from src_code import generate_graphs
import matplotlib.pyplot as plt

# 创建示例图
G = nx.Graph()
G.add_edges_from([(0, 1), (1, 2), (2, 0), (0, 3), (1, 3)])

G = generate_graphs.generate_graph_type(8,['random', 0.5],1)[0]
# nx.draw(G)
# plt.show()
""" 
# 找到所有三角形
triangles = [cycle for cycle in nx.cycle_basis(G) if len(cycle) == 3]

# 移除每个三角形中的一条边
for triangle in triangles:
    # 随机移除三角形中的一条边
    u, v = triangle[0], triangle[1]
    if G.has_edge(u, v):
        G.remove_edge(u, v)
 """

print(nx.cycle_basis(G)[0])

while [cycle for cycle in nx.cycle_basis(G) if len(cycle) == 3]:
    c = [cycle for cycle in nx.cycle_basis(G) if len(cycle) == 3][0]
    print(c)
    u, v = c[0], c[1]
    if G.has_edge(u, v):
        G.remove_edge(u, v)

nx.draw(G)
plt.show()

# 查看修改后的图
print("修改后的边：", list(G.edges()))
# print("connected", nx.is_connected(G))