import networkx as nx
from src_code import build_operators
from src_code import constrained_operators
from src_code import unconstrained_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.linalg import eigh


def MIS_QAOA(no_vertices, depth, G, use_constrain_operator, penalty_term = 1):
    """
    最大独立集QAOA
    """
    gamma_0 = 0.2
    beta_0 = 1

    MIS = nx.approximation.maximum_independent_set(G)
    solution = len(MIS)
    num = 0
    vec = np.zeros(2**no_vertices)
    for i in MIS:
        num += 2**i
        vec[num] = 1 / np.sqrt(solution)

    print(MIS)
    print("solution:", solution)
    print(vec)

    pauli_ops_dict = build_operators.build_my_paulis(no_vertices)
    if(use_constrain_operator):
        hamiltonian = constrained_operators.MIS_hamiltonian(G)
    else:
        hamiltonian = unconstrained_operators.MIS_hamiltonian(G, penalty_term)

    max_ham_eigenvalue = float(vec @ hamiltonian @ vec)
    # max_ham_eigenvalue = eigh(hamiltonian.todense())[0][-1]

    #! use constrained circuits or not 
    if use_constrain_operator:
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
    
    #! unconstrained circuit
    else:
        def obj_func(parameter_values):
            dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(G, parameter_values, pauli_ops_dict, penalty_term)
            expectation_value = (hamiltonian * dens_mat).trace().real
            return expectation_value * (-1.0)
        
        initial_parameter = [gamma_0] * (depth) + [beta_0] * (depth)
        result = minimize(obj_func, initial_parameter, method="BFGS")

        optimal_para = list(result.x)
        dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(G, optimal_para, pauli_ops_dict, penalty_term)

        #! 计算AR时用不带惩罚项的Hamiltonian
        hamiltonian = constrained_operators.MIS_hamiltonian(G)
        max_ham_eigenvalue = float(vec @ hamiltonian @ vec)

        hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
        approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution

    print(f'layers:{depth} MIS_QAOA')

    np.set_printoptions(precision=3, suppress=True)
    print('solution hamiltonian(without I) eigenvalue:', max_ham_eigenvalue)
    print('Hamiltonian(without I) expectation:', hamiltonian_expectation)
    print('AR:', approx_ratio)

    dens_mat = dens_mat.todense()
    # print('dens_mat \n', dens_mat)
    v = dens_mat[:,0]
    v = v/np.sqrt(v[0])
    # print(v.flatten())
    print(np.array2string(v.flatten(), separator=', '))
    # print(np.abs(v))
    print(np.array2string(np.square(np.abs(v)).flatten(), separator=', '))
    print("norm:", np.linalg.norm(v))
    # print(np.outer(v,v))

    print('optimal_parameters:', np.array(optimal_para)/3.1415, "pi")