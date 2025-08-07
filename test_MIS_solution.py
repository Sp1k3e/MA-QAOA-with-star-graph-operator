from src_code import generate_graphs
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
edges = [(0, 1), (0, 3), (1, 2), (2, 3)]
G.add_edges_from(edges)

G = generate_graphs.generate_connected_graph(8, 0.5, 8)[0]

no_vertices = G.number_of_nodes()


MIS = nx.approximation.maximum_independent_set(G)
print("MIS:", MIS, "solution", len(MIS))

binary_solution = ['0'] * no_vertices
for i in MIS:
    binary_solution[i] = '1'
solution = len(MIS)
print("MIS solution:", ''.join(binary_solution))
# num = 0
# vec = np.zeros(2**no_vertices)
# for i in MIS:
#     num += 2**i
# vec[num] = 1
# print(MIS)
# print("solution:", solution)
# print(vec)
# hamiltonian = constrained_operators.MIS_hamiltonian(G)
# max_ham_eigenvalue = (vec @ hamiltonian @ vec).real
# print(max_ham_eigenvalue)
max_ham_eigenvalue = solution - no_vertices/2


pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
plt.show()