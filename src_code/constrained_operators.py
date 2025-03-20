from qiskit import quantum_info as qi
from networkx import Graph
import numpy as np
import warnings
import networkx as nx
from src_code.mixers_density import *
from scipy import sparse
import math
from src_code import useful_methods

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




def build_MIS_QAOAnsatz(graph, parameter_list, pauli_dict):
