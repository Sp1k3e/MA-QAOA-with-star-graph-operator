import networkx as nx
import matplotlib.pyplot as plt
from src_code import generate_graphs

graph = generate_graphs.generate_connected_graph(8, 0.5, 4)[0]


connected_v = [False] * graph.number_of_nodes()
edges = graph.edges()
degrees = dict(graph.degree())
sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
selected_v = []
selected_e = []

for n in sorted_nodes:
    selected_v += [n[0]]
    connected_v[n[0]] = True
    for edge in edges:
        if n[0] in edge:
            if not connected_v[edge[1]]:
                connected_v[edge[1]] = True
                selected_e += [(edge)]

    print(connected_v)
    if all(x == True for x in connected_v):
        break

parameter_list = [1,2,3]

tmp_list = []
i = 0
#! 填充parameter_list
for edge in graph.edges():
    print(edge)
    if edge not in selected_e:
        tmp_list += [0]
    else: 
        tmp_list += [parameter_list[i]]
        i += 1
tmp_list += parameter_list[i:]
parameter_list = tmp_list