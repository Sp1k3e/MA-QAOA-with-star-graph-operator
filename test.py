import networkx as nx
import matplotlib.pyplot as plt

n = 10  # 节点数
p = 0.7  # 边的生成概率

# 生成Erdős-Rényi随机图
G = nx.erdos_renyi_graph(n, p, seed = 0)
# 画图
nx.draw(G, with_labels=True)
plt.show()
