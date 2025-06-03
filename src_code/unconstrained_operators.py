from qiskit import quantum_info as qi
from networkx import Graph
import numpy as np
import networkx as nx
from src_code.mixers_density import *
from scipy import sparse
import math
from src_code import useful_methods

def MIS_hamiltonian(graph, penalty):
    """
    unconstrained QAOA cost Hamiltonian
    """
    hamiltonian_operator = None
    no_nodes = graph.number_of_nodes()
    no_edges = graph.number_of_edges()
    penalty /= 2

    pauli_strings = [None] * (no_nodes + 3 * no_edges)
    coeffs = [-0.5] * no_nodes + [penalty, penalty, -penalty] * no_edges
    index = 0

    for i in range(no_nodes):
        tmp_str = 'I' * (i) + 'Z' + 'I' * (no_nodes - i - 1)
        tmp_str = tmp_str[::-1]
        pauli_strings[index] = tmp_str
        index += 1

    for (i,j) in graph.edges():
        tmp_str = 'I' * (i) + 'Z' + 'I' * (no_nodes - i - 1)
        tmp_str = tmp_str[::-1]
        pauli_strings[index] = tmp_str
        index += 1

        tmp_str = 'I' * (j) + 'Z' + 'I' * (no_nodes - j - 1)
        tmp_str = tmp_str[::-1]
        pauli_strings[index] = tmp_str
        index += 1

        tmp_str = 'I' * (i) + 'Z' + 'I' * (j - i - 1) + 'Z' + 'I' * (no_nodes - j - 1)
        tmp_str = tmp_str[::-1]
        pauli_strings[index] = tmp_str
        index += 1


    hamiltonian_operator = qi.SparsePauliOp(pauli_strings, np.array(coeffs)).to_operator()

    return sparse.csr_matrix(hamiltonian_operator.data)


def initial_density_matrix(no_qubits):
    dim = 2**no_qubits
    dens_mat = qi.DensityMatrix(np.full((dim, dim), 1/dim))

    return sparse.csr_matrix(dens_mat.data)

def MIS_unconstrained_mixer_unitary(no_nodes, parameter_value, dict_paulis):
    """
    """
    first = True
    for i in range(no_nodes):
        if first:
            result = math.cos(parameter_value) * dict_paulis['I'] + 1j * math.sin(parameter_value) * dict_paulis["X" + str(i)]
            first = False

        else:
            result = result * (math.cos(parameter_value) * dict_paulis['I'] + 1j * math.sin(parameter_value) * dict_paulis["X" + str(i)])

    return result

def MIS_unconstrained_phase_unitary(graph, parameter, dict_paulis, penalty_term):
    """
    phase unitary with objective function and penelty term
    """
    first = True
    parameter = 0.5 * parameter
    lambda_parameter = penalty_term * parameter
    for i in range(graph.number_of_nodes()):
        tmp_matrix = dict_paulis['I'] * math.cos(parameter) + dict_paulis['Z' + str(i)] * math.sin(parameter) * 1j

        if first:
            result = tmp_matrix
            first = False
        else:
            result = tmp_matrix * result
    
    edges = graph.edges()
    for (i, j) in edges:
        tmp_matrix = dict_paulis['I'] * math.cos(lambda_parameter) - (dict_paulis['Z' + str(i)]) * math.sin(lambda_parameter) * 1j 

        tmp_matrix *= dict_paulis['I'] * math.cos(lambda_parameter) - (dict_paulis['Z' + str(j)]) * math.sin(lambda_parameter) * 1j 

        # tmp_matrix = dict_paulis['I'] * math.cos(lambda_parameter) - (dict_paulis['Z' + str(i)] * dict_paulis['Z' + str(j)]) * math.sin(lambda_parameter) * 1j * tmp_matrix
        tmp_matrix *= dict_paulis['I'] * math.cos(lambda_parameter) + (dict_paulis['Z' + str(i) + 'Z' + str(j)]) * math.sin(lambda_parameter) * 1j

        # np.set_printoptions(precision=3, suppress=True)
        # print(tmp_matrix.todense())
        
        result = tmp_matrix * result
        
    return result

def build_MIS_unconstrained_QAOAnsatz(graph, parameter_list, pauli_dict, penalty_term):
    no_layers = len(parameter_list) // 2
    ham_parameters = parameter_list[:no_layers]
    mixer_parameters = parameter_list[no_layers:]
    
    no_qubits = graph.number_of_nodes()

    dens_mat = initial_density_matrix(no_qubits)

    for layer in range(no_layers):
        cut_unit = MIS_unconstrained_phase_unitary(graph, ham_parameters[layer], pauli_dict, penalty_term)
        dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())
    
        mix_unit = MIS_unconstrained_mixer_unitary(no_qubits, mixer_parameters[layer], pauli_dict)
        dens_mat = (mix_unit * dens_mat) * (mix_unit.transpose().conj())

    return dens_mat