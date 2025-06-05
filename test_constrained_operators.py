from src_code import constrained_operators
from src_code import unconstrained_operators
from src_code import build_operators
import networkx as nx
import numpy as np
import math

pi = 3.1415

np.set_printoptions(precision=3, suppress=True)

edge_list = [(0,1)]
# edge_list = [(0,1),(1,2)]
edge_list = [(0,1),(1,2), (0,2)]
# edge_list = [(0,1), (1,2), (1,3)]
# edge_list = [(0,1), (1,2), (2,3), (0,3)]
G = nx.Graph()
G.add_edges_from(edge_list)
n = G.number_of_nodes()

pauli_ops_dict = build_operators.build_my_paulis(n)

# initial_density_matrix = constrained_operators.initial_density_matrix(n).todense()
initial_density_matrix = unconstrained_operators.initial_density_matrix(n).todense()
# print('initial density matrix')
# print(initial_density_matrix)

# MIS_hamiltonian = constrained_operators.MIS_hamiltonian(G)

# vec = np.zeros(4)
# vec[2] = 1
# print(vec)
# eigen = np.dot(MIS_hamiltonian.todense(), vec)
# print('eigen')
# print(eigen)

# print('cost hamiltonian')
# print(MIS_hamiltonian.todense())
# eigenvalues = np.linalg.eig(MIS_hamiltonian.todense())[0]
# print('eigenvalues:')
# print(eigenvalues)

phase_para = 0.5 * pi
# MIS_phase_unitary = constrained_operators.MIS_constrained_phase_unitary(G, phase_para, pauli_ops_dict)
MIS_phase_unitary = unconstrained_operators.MIS_unconstrained_phase_unitary(G, -phase_para, pauli_ops_dict, 1)
print("phase_unitary")
print(MIS_phase_unitary.todense())

mix_para = 0.375 * pi
# mixer_unitary = constrained_operators.MIS_constrained_mixer_unitary(G, mixer_para, pauli_ops_dict)
mix_unitary = unconstrained_operators.MIS_unconstrained_mixer_unitary(n, -mix_para, pauli_ops_dict)
print("mix_unitary")
print(mix_unitary.todense())

dens_mat = initial_density_matrix
dens_mat = (MIS_phase_unitary * dens_mat) * (MIS_phase_unitary.transpose().conj())
dens_mat = (mix_unitary * dens_mat) * (mix_unitary.transpose().conj())
print('dens_mat')
print(dens_mat)

penalty_term = 1

paras = [0.5 * pi, 0.375 * pi]
paras = [1.2 * pi, 0.3 * pi]
# dens_mat = constrained_operators.build_MIS_constrained_QAOAnsatz(G, paras, pauli_ops_dict)
dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(G, paras, pauli_ops_dict, penalty_term)

print('dens_mat')
print(dens_mat.todense())
# row_idx, col_idx = np.unravel_index(dens_mat.argmax(), dens_mat.shape)
# np.set_printoptions(precision=2, suppress=True)
# print(f"最大值: {dens_mat.max()}, 位置: ({row_idx}, {col_idx})")

no_vertices = G.number_of_nodes()
MIS = nx.approximation.maximum_independent_set(G)
solution = len(MIS)
num = 0
vec = np.zeros(2**no_vertices)
for i in MIS:
    num += 2**i
vec[num] = 1
 
hamiltonian = constrained_operators.MIS_hamiltonian(G)
max_ham_eigenvalue = (vec @ hamiltonian @ vec).real
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
print(hamiltonian_expectation)
print(max_ham_eigenvalue)
approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution
print("AR: ", approx_ratio)
print("solution: ", solution)

dens_mat = dens_mat.todense()
v = dens_mat[:,0]
v = v/np.sqrt(v[0])
print("probability:", end='')
print(np.array2string(np.square(np.abs(v)).flatten(), separator=', '))

sum = 0
for i in range(2**no_vertices):
    count = bin(i).count('1')
    sum += count * np.square(np.abs(v))[i]
print(sum)

formula_expectation = 0
beta = paras[1]
gamma = paras[0]

# 两个点
# for i in range(no_vertices):
#     formula_expectation += 1/2 - 1/2 * math.sin(2 * beta) * (math.sin(gamma) * math.cos(penalty_term*gamma) - math.cos(gamma) * math.sin(penalty_term*gamma))

# 三角形
for i in range(no_vertices):
    formula_expectation += 1/2
    formula_expectation += -1/2 * math.cos(penalty_term* gamma) ** 2 * math.sin(2 * beta) * math.sin(gamma) * (math.cos(penalty_term*gamma)**2 - math.sin(penalty_term*gamma)**2)
    formula_expectation += -1/2 * math.cos(penalty_term* gamma) ** 2 * math.sin(2 * beta) * math.cos(gamma) * (2 * math.cos(penalty_term*gamma) * -math.sin(penalty_term*gamma))
    # formula_expectation += -1/2 * math.cos(penalty_term* gamma) ** 2 * math.sin(2 * beta) * math.sin(gamma*(1 - 4*penalty_term))

print(formula_expectation/solution)