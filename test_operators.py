from src_code import constrained_operators
from src_code import unconstrained_operators
from src_code import build_operators
import networkx as nx
import numpy as np

pi = 3.1415

np.set_printoptions(precision=3, suppress=True)

edge_list = [(0,1)]
# edge_list = [(0,1),(1,2)]
# edge_list = [(0,1), (1,2), (1,3)]
# edge_list = [(0,1), (1,2), (2,3), (0,3)]
G = nx.Graph()
G.add_edges_from(edge_list)
n = G.number_of_nodes()

pauli_ops_dict = build_operators.build_my_paulis(n)

initial_density_matrix = constrained_operators.initial_density_matrix(n).todense()
initial_density_matrix = unconstrained_operators.initial_density_matrix(n).todense()
print('initial density matrix')
print(initial_density_matrix)

MIS_hamiltonian = constrained_operators.MIS_hamiltonian(G)

# vec = np.zeros(4)
# vec[2] = 1
# print(vec)
# eigen = np.dot(MIS_hamiltonian.todense(), vec)
# print('eigen')
# print(eigen)

print('cost hamiltonian')
print(MIS_hamiltonian.todense())
# eigenvalues = np.linalg.eig(MIS_hamiltonian.todense())[0]
# print('eigenvalues:')
# print(eigenvalues)


mixer_para = pi/2
mixer_unitary = constrained_operators.MIS_constrained_mixer_unitary(G, mixer_para, pauli_ops_dict)
mixer_unitary = unconstrained_operators.MIS_unconstrained_mixer_unitary(n, mixer_para, pauli_ops_dict)
print("mixer_unitary")
print(mixer_unitary.todense())

phase_para = pi/2
MIS_phase_unitary = constrained_operators.MIS_constrained_phase_unitary(G, phase_para, pauli_ops_dict)
MIS_phase_unitary = unconstrained_operators.MIS_unconstrained_phase_unitary(G, phase_para, pauli_ops_dict)
print("phase_unitary")
print(MIS_phase_unitary.todense())

paras = [0.2, 1.57]
dens_mat = constrained_operators.build_MIS_constrained_QAOAnsatz(G, paras, pauli_ops_dict)
dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(G, paras, pauli_ops_dict)

print('dens_mat')
# row_idx, col_idx = np.unravel_index(dens_mat.argmax(), dens_mat.shape)
# np.set_printoptions(precision=2, suppress=True)
# print(f"最大值: {dens_mat.max()}, 位置: ({row_idx}, {col_idx})")