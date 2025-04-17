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
    num = 0
    for i in MIS:
        num += 2**i
    vec = np.zeros(2**no_vertices)
    vec[num] = 1
    print(MIS)
    print("solution:", solution)
    # print(vec)

    pauli_ops_dict = build_operators.build_my_paulis(no_vertices)
    hamiltonian = -constrained_operators.MIS_hamiltonian(G)

    max_ham_eigenvalue = float(vec @ hamiltonian @ vec)
    # print(float(max_ham_eigenvalue))

    def obj_func(parameter_values):
        dens_mat = constrained_operators.build_MIS_constrained_QAOAnsatz(G, parameter_values, pauli_ops_dict)
        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)
    

    initial_parameter = [gamma_0] * (depth) + [beta_0] * (depth)
    result = minimize(obj_func, initial_parameter, method="BFGS")

    optimal_para = list(result.x)
    dens_mat = constrained_operators.build_MIS_constrained_QAOAnsatz(G, optimal_para, pauli_ops_dict)
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution

    print(f'layers:{depth} MIS_QAOA')

    print('Hamiltonian_expectation:', hamiltonian_expectation)
    print('AR:', approx_ratio)
    np.set_printoptions(precision=2, suppress=True)
    print('dens_mat', dens_mat.todense())

    print('optimal_parameters:', optimal_para)