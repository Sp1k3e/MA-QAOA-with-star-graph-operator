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
    dim = 2**no_qubits
    # dens_mat = qi.DensityMatrix(np.full((dim, dim), 1/dim))
    mat = np.zeros((dim,dim))
    mat[0][0] = 1
    dens_mat = qi.DensityMatrix(mat)

    return sparse.csr_matrix(dens_mat.data)

def MIS_hamiltonian(graph):
    """
    cost Hamiltonian
    """
    hamiltonian_operator = None
    no_nodes = graph.number_of_nodes()

    pauli_strings = [None] * no_nodes
    coeffs = [-1] * no_nodes
    index = 0

    for i in range(no_nodes):
        tmp_str = 'I' * (i) + 'Z' + 'I' * (no_nodes - i - 1)
        tmp_str = tmp_str[::-1]
        pauli_strings[index] = tmp_str
        # coeffs[index] = (-0.5) * graph.get_edge_data(i, k)['weight']
        index += 1

    # hamiltonian_operator = qi.SparsePauliOp(pauli_strings).to_operator()
    hamiltonian_operator = qi.SparsePauliOp(pauli_strings, np.array(coeffs)).to_operator()

    return sparse.csr_matrix(hamiltonian_operator.data)



def MIS_constrained_mixer_unitary(graph, parameter, dict_paulis):
    """
    X on each qubit
    """
    i = 0
    first = True
    for i in range(graph.number_of_nodes()):
        B = dict_paulis['I']
        for j in graph.neighbors(i):
            B = B * ((dict_paulis['I'] + dict_paulis['Z'+str(j)])/2)

        tmp_matrix = dict_paulis['I'] + ((math.cos(parameter)-1) * dict_paulis['I'] + 1j*math.sin(parameter)*dict_paulis['X'+str(i)]) * B

        if first:
            result = tmp_matrix
            first = False
        else:
            result = tmp_matrix * result

    return result


def MIS_constrained_phase_unitary(graph, parameter, dict_paulis):
    first = True
    parameter = parameter
    for i in range(graph.number_of_nodes()):
        tmp_matrix = dict_paulis['I'] * math.cos(parameter) + dict_paulis['Z' + str(i)] * math.sin(parameter) * 1j

        if first:
            result = tmp_matrix
            first = False
        else:
            result = tmp_matrix * result
        
    return result


def build_MIS_constrained_QAOAnsatz(graph, parameter_list, pauli_dict):
    no_layers = len(parameter_list) // 2
    ham_parameters = parameter_list[:no_layers]
    mixer_parameters = parameter_list[no_layers:]
    
    no_qubits = graph.number_of_nodes()

    dens_mat = initial_density_matrix(no_qubits)

    for layer in range(no_layers):
        cut_unit = MIS_constrained_phase_unitary(graph, ham_parameters[layer], pauli_dict)
        dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())
    
        mix_unit = MIS_constrained_mixer_unitary(graph, mixer_parameters[layer], pauli_dict)
        dens_mat = (mix_unit * dens_mat) * (mix_unit.transpose().conj())

    return dens_mat


# def build_MIS_unconstrained_QAOAnsatz(graph, parameter_list, pauli_dict):
