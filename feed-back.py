import networkx
import random
from scipy import sparse
from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from qiskit import quantum_info as qi
import math
import matplotlib.pyplot as plt


no_vertices = 8
seed = 1
graph = generate_graphs.generate_regular_graph(no_vertices,3,seed)[0]

hamiltonian = build_operators.cut_hamiltonian(graph=graph)
gradient_ops_dict = build_operators.build_all_mixers(graph=graph)
pauli_ops_dict = build_operators.build_all_paulis(no_vertices)

max_cut_solution = useful_methods.find_optimal_cut(graph)
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]
ham_offset = max_cut_value - max_ham_eigenvalue

hamiltonian = build_operators.cut_hamiltonian(graph)
# mix_hamiltonian = build_operators.mix_hamiltonian(graph)

beta = 1
delta_t = 0.1
# mix_type = 'standard_x'
ham_approx_ratios = []
hamiltonian_expectation_t = 0
cut_approx_ratios = [0]

max_layers = 20
layer = 0

curr_dens_mat = build_operators.initial_density_matrix(no_vertices)

def build_layer(curr_dens_mat, beta, mix_type):
    """ one layer 
    """
    cut_unit = build_operators.cut_unitary(graph,delta_t,pauli_ops_dict)
    curr_dens_mat = (cut_unit * curr_dens_mat) * (cut_unit.transpose().conj())

    mix_unit = build_operators.mixer_unitary(mix_type, beta * delta_t, pauli_ops_dict, no_vertices)
    curr_dens_mat = (mix_unit * curr_dens_mat) * (mix_unit.transpose().conj())

    return curr_dens_mat


def update_beta(curr_dens_mat, i):
    tmp_str = 'I' * (i) + 'X' + 'I' * (no_vertices -i -1)
    pauli_strings = tmp_str[::-1]
    h = qi.SparsePauliOp(pauli_strings).to_operator()
    mix_hamiltonian = sparse.csr_matrix(h)
    A = 1j*(mix_hamiltonian*hamiltonian - hamiltonian * mix_hamiltonian) * curr_dens_mat
    expectation = A.trace().real

    return expectation

while layer < no_vertices:
    curr_dens_mat = build_operators.initial_density_matrix(no_vertices)
    curr_dens_mat = build_layer(curr_dens_mat, beta, 'X'+str(layer))

    # hamiltonian_expectation = (hamiltonian * curr_dens_mat).trace().real
    # cut_approx_ratios.append((hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value)

    beta = update_beta(curr_dens_mat, layer)
    print(beta)
    layer +=1

# while layer < max_layers:
#     layer +=1
#     curr_dens_mat = build_layer(curr_dens_mat, beta, mix_type)

#     hamiltonian_expectation = (hamiltonian * curr_dens_mat).trace().real
#     cut_approx_ratios.append((hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value)

#     print("layer", layer, ': ', format(cut_approx_ratios[layer],'.10f'), "  beta: ", beta, sep='')

#     beta = update_beta(curr_dens_mat)
