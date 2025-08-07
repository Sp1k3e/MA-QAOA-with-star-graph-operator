import networkx as nx

edge_list = [(0,1), (0,2)] #三角形少一条边
G = nx.Graph()
G.add_edges_from(edge_list)

no_vertices = G.number_of_nodes()

MIS = nx.approximation.maximum_independent_set(G)
# print(MIS)
MIS_value = len(MIS)
print("MIS value:", MIS_value)

binary_solution = ['0'] * no_vertices
for i in MIS:
    binary_solution[i] = '1'
solution = len(MIS)
print("MIS solution:", ''.join(binary_solution))

final_state = ['0','1','1']
result_vertices = []

for i in range(no_vertices):
    if final_state[i] == '1':
        result_vertices += [i]

# print(result_vertices)

feasible_pro = 0
optimal_pro = 0

n = len(result_vertices)
for i in range(n):
    for j in range(i+1, n):
        a = result_vertices[i]
        b = result_vertices[j]
        if G.has_edge(a,b):
            print("invalide solution")
            break

if n == solution:
    print('optimal solution')

n = 1
solution = format(i, f'0{n}b').format(3)
print(solution)

for i in range(n):
    if solution[i] == '1':
        result_vertices += [i]
        n = len(result_vertices)

for i in range(n):
    for j in range(i+1, n):
        a = result_vertices[i]
        b = result_vertices[j]
        if G.has_edge(a,b):
            print("invalide solution")
            break