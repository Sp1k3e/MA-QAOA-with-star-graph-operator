import networkx as nx
from src_code import build_operators
from src_code import constrained_operators
from src_code import unconstrained_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import math
import time
import matplotlib.pyplot as plt
from scipy.linalg import eigh


def MIS_QAOA(G, depth, use_constrain_operator, penalty_term = 1, initial_state = [], custom_phase_operator = None):
    """
    MIS variants of QAOA
    """
    gamma_0 = 0.5
    beta_0 = 0.5
    # np.set_printoptions(precision=3, suppress=True)
    no_vertices = G.number_of_nodes()

    MIS = nx.approximation.maximum_independent_set(G)
    solution = len(MIS)
    # num = 0
    # vec = np.zeros(2**no_vertices)
    # for i in MIS:
    #     num += 2**i
    # vec[num] = 1
    # print(MIS)
    # print("solution:", solution)
    # print(vec)

    pauli_ops_dict = build_operators.build_my_paulis(no_vertices)

    if(use_constrain_operator == 1):
        print('partial Mixer')
        hamiltonian = constrained_operators.MIS_hamiltonian(G)
    else:
        print('unconstrained QAOA')
        hamiltonian = unconstrained_operators.MIS_hamiltonian(G, penalty_term)

    # hamiltonian = constrained_operators.MIS_hamiltonian(G)
    # max_ham_eigenvalue = (vec @ hamiltonian @ vec).real
    # print(max_ham_eigenvalue)
    max_ham_eigenvalue = solution - no_vertices/2

    target_graph = G
    if custom_phase_operator != None:
        target_graph = custom_phase_operator

    #! use constrained circuits or not 
    if use_constrain_operator:
        def obj_func(parameter_values):
            #! partial mixer
            dens_mat = constrained_operators.build_MIS_partial_mixer_QAOAnsatz(target_graph, parameter_values, pauli_ops_dict, initial_state)
            expectation_value = (hamiltonian * dens_mat).trace().real
            return expectation_value * (-1.0)

        initial_parameter = [gamma_0] * (depth) + [beta_0] * (depth)
        result = minimize(obj_func, initial_parameter, method="BFGS")

        optimal_para = list(result.x)
        dens_mat = constrained_operators.build_MIS_partial_mixer_QAOAnsatz(target_graph, optimal_para, pauli_ops_dict, initial_state)

        hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
        approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution

    
    #! unconstrained circuit
    else:
        def obj_func(parameter_values):
            dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(target_graph, parameter_values, pauli_ops_dict, penalty_term)
            expectation_value = (hamiltonian * dens_mat).trace().real
            return expectation_value * (-1.0)
        
        initial_parameter = [gamma_0] * (depth) + [beta_0] * (depth)
        result = minimize(obj_func, initial_parameter, method="BFGS")

        optimal_para = list(result.x)
        dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(target_graph, optimal_para, pauli_ops_dict, penalty_term)

        #! use Hamiltonian without penalty to calculate the AR
        hamiltonian = constrained_operators.MIS_hamiltonian(G)
        hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
        approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution

    print(f'layers:{depth} MIS_QAOA')

    print('solution hamiltonian eigenvalue:', max_ham_eigenvalue)
    print('Hamiltonian expectation:', hamiltonian_expectation)
    print('AR:', approx_ratio)

    dens_mat = dens_mat.todense()
    # print('dens_mat \n', dens_mat)
    v = dens_mat[:,0]
    v = v/np.sqrt(v[0])

    # print("probability:")
    # probabilities = np.array(np.square(np.abs(v)))
    # for i in range(2**no_vertices):
    #     print(format(i, f'0{no_vertices}b'), end = ' ')
    #     print(probabilities[i])

    # print(np.array2string(np.square(np.abs(v)).flatten(), separator=', '))
    # print("norm:", np.linalg.norm(v))
    # print(np.outer(v,v))

    if initial_state is not None:
        print("initial state:", initial_state)
    print('optimal_parameters:', np.array(optimal_para)/3.1415, "pi")
