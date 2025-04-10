from src_code import constrained_operators
from src_code import build_operators
import networkx as nx
import numpy as np

pi = 3.1415

edge_list = [(0,1)]
G = nx.Graph()
G.add_edges_from(edge_list)
n = G.number_of_nodes()

pauli_ops_dict = build_operators.build_my_paulis(n)

initial_density_matrix = constrained_operators.initial_density_matrix(n).todense()
# print(initial_density_matrix)

MIS_hamiltonian = constrained_operators.MIS_hamiltonian(G)

# print(MIS_hamiltonian.todense())

mixer_para = pi/2
mixer_unitary = constrained_operators.MIS_constrained_mixer_unitary(G, mixer_para, pauli_ops_dict)

print("mixer_unitary")
np.set_printoptions(precision=2, suppress=True)
print(mixer_unitary.todense())

phase_para = pi/2
MIS_cut_unitary = constrained_operators.MIS_constrained_cut_unitary(G, phase_para, pauli_ops_dict)

print("phase_unitary")
np.set_printoptions(precision=2, suppress=True)
print(MIS_cut_unitary.todense())

