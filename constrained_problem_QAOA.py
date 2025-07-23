import networkx as nx
from src_code import build_operators
from src_code import constrained_operators
from src_code import unconstrained_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
import random
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
    no_vertices = G.number_of_nodes()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices)

    MIS = nx.approximation.maximum_independent_set(G)
    binary_solution = ['0'] * no_vertices
    for i in MIS:
        binary_solution[i] = '1'
    solution = len(MIS)
    print("MIS solution:", ''.join(binary_solution))
    max_ham_eigenvalue = solution - no_vertices/2

    if custom_phase_operator != None:
        target_graph = custom_phase_operator
    else:
        target_graph = G

    # initial_parameter = [gamma_0] * (depth) + [beta_0] * (depth)
    initial_parameter = [random.random() * 3 for _ in range(depth * 2)]
    #! use constrained circuits or not 
    if use_constrain_operator:
        print('Partial Mixer')
        hamiltonian = constrained_operators.MIS_hamiltonian(G)

        def obj_func(parameter_values):
            #! partial mixer
            dens_mat = constrained_operators.build_MIS_partial_mixer_QAOAnsatz(target_graph, parameter_values, pauli_ops_dict, initial_state)
            expectation_value = (hamiltonian * dens_mat).trace().real
            return expectation_value * (-1.0)

        result = minimize(obj_func, initial_parameter, method="BFGS")

        optimal_para = list(result.x)
        dens_mat = constrained_operators.build_MIS_partial_mixer_QAOAnsatz(target_graph, optimal_para, pauli_ops_dict, initial_state)

        hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
        approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution

    #! unconstrained circuit
    else:
        print('unconstrained QAOA  penalty term =', penalty_term)
        hamiltonian = unconstrained_operators.MIS_hamiltonian(G, penalty_term)

        def obj_func(parameter_values):
            dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(target_graph, parameter_values, pauli_ops_dict, penalty_term, initial_state)
            # dens_mat = build_operators.build_standard_qaoa_ansatz(G, parameter_values, pauli_ops_dict)
            expectation_value = (hamiltonian * dens_mat).trace().real
            return expectation_value * (-1.0)
        
        result = minimize(obj_func, initial_parameter, method="BFGS")

        optimal_para = list(result.x)
        dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(target_graph, optimal_para, pauli_ops_dict, penalty_term, initial_state)
        # dens_mat = build_operators.build_standard_qaoa_ansatz(G, optimal_para, pauli_ops_dict)

        #! use Hamiltonian without penalty to calculate the AR
        hamiltonian = constrained_operators.MIS_hamiltonian(G)
        hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
        approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution

    print(f'layers:{depth} MIS_QAOA')

    # print('solution hamiltonian eigenvalue:', max_ham_eigenvalue)
    # print('Hamiltonian expectation:', hamiltonian_expectation)
    print('AR:', approx_ratio)

    dens_mat = dens_mat.todense()
    v = dens_mat[:,0]
    v = v/np.sqrt(v[0])

    # print("probability:")
    # probabilities = np.array(np.square(np.abs(v)))
    # for i in range(2**no_vertices):
    #     if(probabilities[i] > 0.005):
    #         print(format(i, f'0{no_vertices}b'), end = ' ')
    #         print(probabilities[i])

    # print(np.array2string(np.square(np.abs(v)).flatten(), separator=', '))
    # print("norm:", np.linalg.norm(v))
    # print(np.outer(v,v))

    if use_constrain_operator and len(initial_state) != 0:
        print("initial state:", initial_state)
    print('optimal_parameters:', np.array(optimal_para)/3.1415, "pi")
    print('--------------------------------------------------------')

    # return v
    # return [x[0] for x in probabilities]


def MIS_MA_QAOA(G, depth, penalty_term, initial_state = []):
    gamma_0 = 1
    beta_0 = 0.7854
    no_vertices = G.number_of_nodes()
    for u,v in G.edges():
        G[u][v]['weight'] = 1

    no_edges = G.number_of_edges()
    pauli_ops_dict = build_operators.build_my_paulis(no_vertices)

    hamiltonian = unconstrained_operators.MIS_hamiltonian(G, penalty_term)

    MIS = nx.approximation.maximum_independent_set(G)
    solution = len(MIS)
    max_ham_eigenvalue = solution - no_vertices/2

    print(f'layers:{depth} MA-All')

    simulation_time = []

    def obj_func(parameter_values):
        start_time = time.perf_counter()

        dens_mat = build_operators.build_MA_qaoa_ansatz(G, parameter_values, depth, pauli_ops_dict, 'All', initial_state)

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        # seconds = execution_time % 60
        # print(f"One round simulation took {minutes}m {seconds:.2f}s.")
        simulation_time.append(execution_time)

        expectation_value = (hamiltonian * dens_mat).trace().real
        return expectation_value * (-1.0)

    start_time = time.perf_counter()

    # initial_parameter_guesses = [gamma_0] * (depth * no_edges) + [beta_0] * (depth * no_vertices)
    initial_parameter_guesses = [random.random() * 3 for _ in range(depth * (no_edges + no_vertices))] 
    # print(initial_parameter_guesses)
    result = minimize(obj_func, initial_parameter_guesses, method="BFGS", )

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    parameter_list = list(result.x)
    dens_mat = build_operators.build_MA_qaoa_ansatz(G, parameter_list, depth, pauli_ops_dict, 'All', initial_state)

    hamiltonian = constrained_operators.MIS_hamiltonian(G)
    hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
    cut_approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution

    # print('***************')
    # print("目标函数总调用次数:", result.nfev)
    # print(f'total iteration: {result.nit}')
    # print(f"Minimize time: {execution_time}s")
    # print(f"simulation time: {sum(simulation_time)}s")
    print(f'AR: {cut_approx_ratio}')

    dens_mat = dens_mat.todense()
    v = dens_mat[:,0]
    v = v/np.sqrt(v[0])

    print("probability:")
    probabilities = np.array(np.square(np.abs(v)))
    for i in range(2**no_vertices):
        if(probabilities[i] > 0.001):
            print(format(i, f'0{no_vertices}b'), end = ' ')
            print(probabilities[i])
    
    print("optimal parameters:", np.array(parameter_list)/3.1415, "pi")