from qiskit import quantum_info as qi
from networkx import Graph
import numpy as np
import warnings
import networkx as nx
from src_code.mixers_density import *
from scipy import sparse
import math
from src_code import useful_methods

def initial_density_matrix(no_qubits):
    """
    Returns density matrix corresponding to the initial state for QAOA algorithms.

    Parameters:
        no_qubits - number of qubits in system
    Returns:
        dens_mat - DensityMatrix Instance
    """

    dim = 2**no_qubits
    dens_mat = qi.DensityMatrix(np.full((dim, dim), 1/dim))

    return sparse.csr_matrix(dens_mat.data)

def MIS_hamiltonian(graph):
    """
    return MIS hamiltonian
    """
    hamiltonian_operator = None
    no_nodes = graph.number_of_nodes()

    # with warnings.catch_warnings():
        # warnings.simplefilter("ignore", category=FutureWarning)

    # no_ops = graph.number_of_edges()
    no_ops = graph.number_of_nodes()

    pauli_strings = [None] * no_ops
    coeffs = [None] * no_ops
    index = 0

    # 遍历所有的点
    for i in range(no_nodes):
        tmp_str = 'I' * (i) + 'Z' + 'I' * (no_nodes - i - 1)
        tmp_str = tmp_str[::-1]
        pauli_strings[index] = tmp_str
        coeffs[index] = 1
        index += 1

    hamiltonian_operator = qi.SparsePauliOp(pauli_strings, np.array(coeffs)).to_operator()

    return sparse.csr_matrix(hamiltonian_operator.data)


def uncontrained_MIS_hamiltonian(graph):
    """
    cost Hamiltonian
    """
    hamiltonian_operator = None
    no_nodes = graph.number_of_nodes()

    pauli_strings = [None] * no_nodes
    # coeffs = [None] * no_ops
    index = 0

    for i in range(no_nodes):
                tmp_str = 'I' * (i) + 'Z' + 'I' * (no_nodes - i - 1)
                tmp_str = tmp_str[::-1]
                pauli_strings[index] = tmp_str
                # coeffs[index] = (-0.5) * graph.get_edge_data(i, k)['weight']
                index += 1

    hamiltonian_operator = qi.SparsePauliOp(pauli_strings).to_operator()

    return sparse.csr_matrix(hamiltonian_operator.data)


def build_MIS_QAOAnsatz(graph, parameter_list, pauli_dict):

    no_layers = len(parameter_list) // 2
    ham_parameters = parameter_list[:no_layers]
    mixer_parameters = parameter_list[no_layers:]
    
    no_qubits = graph.number_of_nodes()

    dens_mat = initial_density_matrix(no_qubits)

    for layer in range(no_layers):

        cut_unit = cut_unitary(graph, ham_parameters[layer], pauli_dict)
        dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())
    
        mix_unit = mixer_unitary('standard_x', mixer_parameters[layer], pauli_dict, no_qubits)
        dens_mat = (mix_unit * dens_mat) * (mix_unit.transpose().conj())

    return dens_mat
