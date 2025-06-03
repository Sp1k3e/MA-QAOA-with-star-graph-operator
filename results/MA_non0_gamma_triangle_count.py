import networkx as nx
from src_code import generate_graphs
import csv


triangle_count = 0
optimal_count = 0

with open('results/parameters/MA-QAOA1.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        # row = next(csvreader)
        para_list = row[7:-8]

        para_list[0] = para_list[0].replace('[','')
        # para_list[-1] = para_list[-1].replace(']','')
        para_list = list(map(float,para_list))

        para_list = [0 if abs(i) < 0.05 else 1 for i in para_list]    
        # print(para_list)
            
        G = generate_graphs.generate_graph_type(8,['random',0.5], int(row[4]))[0]
        triangles = [cycle for cycle in nx.cycle_basis(G) if len(cycle) == 3]
        triangle_count += len(triangles)

        edge_list = tuple(G.edges())
        new_edge = []
        
        for i in range(len(para_list)):
            if(para_list[i] != 0):
                # print(edge_list[i])
                new_edge.append(edge_list[i])
        # print(new_edge)

        G = nx.Graph()
        G.add_edges_from(new_edge)

        triangles = [cycle for cycle in nx.cycle_basis(G) if len(cycle) == 3]
        # print(len(triangles))
        optimal_count += len(triangles)

print(f'{triangle_count} {optimal_count}')
print(optimal_count/triangle_count)  