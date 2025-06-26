import networkx as nx
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
import numpy as np
import matplotlib.pyplot as plt

n = 8
seed = 0
graph_type = ['random', 0.5]

G = generate_graphs.generate_graph_type(n, graph_type, seed)[0]

# pos = nx.spring_layout(G)
# nx.draw(G)

# plt.show()

d = 10
x = np.linspace(-np.pi, np.pi, 100)
y = np.cos(x) ** d * np.sin(x * ( 1 - d))

plt.plot(x, y, label='y = sin(x)')    # 画线
plt.title(f"d={d}")             # 标题
plt.xlabel("x")                        # x 轴标签
plt.ylabel("y")                        # y 轴标签
plt.legend()                           # 显示图例
plt.grid(True)                         # 显示网格
plt.show()                             # 显示图像
