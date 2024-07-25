import networkx as nx
import matplotlib.pyplot as plt
from src_code import generate_graphs

G = generate_graphs.generate_connected_graph(6, 0.8, 0)[0]

# 计算最小生成树
mst = nx.minimum_spanning_tree(G)
print(mst.edges())

# 可视化图和最小生成树
pos = nx.spring_layout(G)  # 布局图形位置

plt.figure(figsize=(10, 5))

# 绘制原始图
plt.subplot(121)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=15)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
plt.title("Original Graph")

# 绘制最小生成树
plt.subplot(122)
nx.draw(mst, pos, with_labels=True, node_color='lightgreen', node_size=500, font_size=15)
nx.draw_networkx_edge_labels(mst, pos, edge_labels={(u, v): d['weight'] for u, v, d in mst.edges(data=True)})
plt.title("Minimum Spanning Tree")

plt.show()
