import networkx as nx

G = nx.Graph()
edge_list = [(0,1)]
edge_list = [(0,1), (1,2), (0,2)] #三角形
edge_list = [(0,1), (1,2), (2,3), (0,3)]
# edge_list = [(0,1), (1,2), (1,3)]
# edge_list = [(0,1), (1,2), (1,3), (3,4), (2,3)]
G.add_edges_from(edge_list)

edges = G.edges()
print(edges)
for(i,j) in edges:
    print(i,j);