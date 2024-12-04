import networkx as nx
from src_code import generate_graphs
import matplotlib.pyplot as plt
from collections import Counter


seed = 1

G = nx.Graph()
G = generate_graphs.generate_graph_type(8,['random',0.5],seed)[0]

triangles = [cycle for cycle in nx.cycle_basis(G) if len(cycle) == 3]
for triangle in triangles:
# 随机移除三角形中的一条边
    u, v = triangle[0], triangle[1]
    if G.has_edge(u, v):
        G.remove_edge(u, v)

print(G.edges())