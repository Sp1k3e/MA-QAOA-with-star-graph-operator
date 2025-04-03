import networkx as nx
from src_code import build_operators
from src_code import constrained_operators
from src_code import constrained_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def MIS_QAOA(no_vertices, depth, G):
    """
    最大独立集QAOA
    """
    gamma_0 = 0.2
    beta_0 = 1

    MIS = nx.approximation.maximum_independent_set(G)
    solution = len(MIS)
    print("solution:", solution)
    print(MIS)

    pauli_ops_dict = build_operators.build_my_paulis(no_vertices)
    hamiltonian = constrained_operators.uncontrained_MIS_hamiltonian(G)


    def obj_func(parameter_values):
        dens_mat = constrained_operators.build_MIS_QAOAnsatz(G, parameter_values, pauli_ops_dict)
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)
    
    initial_parameter = [gamma_0] * (depth) + [beta_0] * (depth)
    result = minimize(obj_func, initial_parameter, method="BFGS")

    optimal_para = list(result.x)
    dens_mat = constrained_operators.build_MIS_QAOAnsatz(G, optimal_para, pauli_ops_dict)
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real

    print(hamiltonian_expectation)

    print(f'layers:{depth} MIS_QAOA')

    print('approximate ratio:', hamiltonian_expectation)