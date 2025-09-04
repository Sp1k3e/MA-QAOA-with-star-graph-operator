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

def calculate_pro(G, probabilities, solution):
    # print("probabilities:")
    invalid_pro = 0
    optimal_pro = 0
    no_vertices = G.number_of_nodes()
    for i in range(2**no_vertices):
        if(probabilities[i] > 0.001):
            feasible = True
            current_solution = format(i, f'0{no_vertices}b')
            current_solution = current_solution[::-1]
            # print(current_solution, end = ' ')

            result_vertices = []
            for j in range(no_vertices):
                if current_solution[j] == '1':
                    result_vertices += [j]
            n = len(result_vertices)

            if(n > solution):
                invalid_pro += probabilities[i]
                # print("invalide solution", end = ' ')
                # print(probabilities[i])
                continue

            for x in range(n):
                if feasible == False:
                    break
                for y in range(x+1, n):
                    a = result_vertices[x]
                    b = result_vertices[y]
                    if G.has_edge(a,b):
                        # print(a,b, end = ' ')
                        # print("invalide solution", end = ' ')
                        invalid_pro += probabilities[i]
                        feasible = False
                        break

            if feasible and n == solution:
                # print("optimal solution", end = ' ')
                optimal_pro += probabilities[i]
            
            # print(probabilities[i])
    print('\nresults:')
    # print('  unfeasible_solution_probability: ', invalid_pro)
    print('  feasible_solution_probablity: ', 1 - invalid_pro)
    print('  optimal_solution_probablity: ', optimal_pro)
    return [float(1 - invalid_pro), float(optimal_pro)]

def MIS_QAOA(G, depth, use_constrain_operator, penalty_term = 1, initial_state = [], custom_phase_operator = None, save = False, seed = -1, p = 0, phase_operator_type = ''):
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

    evaluation = 0
    iteration = 0
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
        print(depth, 'layer unconstrained QAOA  penalty term =', penalty_term)
        print(phase_operator_type)
        hamiltonian = unconstrained_operators.MIS_hamiltonian(G, penalty_term)

        if phase_operator_type == 'fewer_RZ':
            def obj_func(parameter_values):
                dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_fewer_RZ(target_graph, parameter_values, pauli_ops_dict, penalty_term, initial_state)
                expectation_value = (hamiltonian * dens_mat).trace().real
                return expectation_value * (-1.0)

            result = minimize(obj_func, initial_parameter, method="BFGS")
            optimal_para = list(result.x)
            dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_fewer_RZ(target_graph, optimal_para, pauli_ops_dict, penalty_term, initial_state)

        elif phase_operator_type == 'additional_RX':
            def obj_func(parameter_values):
                dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_addtional_RX(target_graph, parameter_values, pauli_ops_dict, penalty_term, initial_state)
                expectation_value = (hamiltonian * dens_mat).trace().real
                return expectation_value * (-1.0)

            initial_parameter = [random.random() * 3 for _ in range(depth * 3)]
            result = minimize(obj_func, initial_parameter, method="BFGS")
            optimal_para = list(result.x)
            dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_addtional_RX(target_graph, optimal_para, pauli_ops_dict, penalty_term, initial_state)

        elif phase_operator_type == 'variational_lambdas':
            def obj_func(parameter_values):
                dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_variational_lambdas(target_graph, parameter_values, pauli_ops_dict, penalty_term, initial_state)
                expectation_value = (hamiltonian * dens_mat).trace().real
                return expectation_value * (-1.0)

            initial_parameter = [random.random() * 3 for _ in range(depth * 3)]
            result = minimize(obj_func, initial_parameter, method="BFGS")
            # bounds = [(0,3)]*(depth*3)
            # result = minimize(obj_func, initial_parameter, method="COBYLA", bounds=bounds)
            optimal_para = list(result.x)
            dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_variational_lambdas(target_graph, optimal_para, pauli_ops_dict, penalty_term, initial_state)
            print(optimal_para)

        elif phase_operator_type == 'variational_lambda':
            def obj_func(parameter_values):
                dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_variational_lambda(target_graph, parameter_values, pauli_ops_dict, penalty_term, initial_state)
                # hamiltonian = unconstrained_operators.MIS_hamiltonian(G, parameter_values[-1]) # taking the lambda in objective function into account
                expectation_value = (hamiltonian * dens_mat).trace().real
                return expectation_value * (-1.0)

            initial_parameter += [random.random() * 2 + 1]
            result = minimize(obj_func, initial_parameter, method="BFGS")

            # bounds = [(0,6.28)]*(depth*2) + [(1, 10)] # taking the lambda in objective function into account
            # result = minimize(obj_func, initial_parameter, method="COBYLA", bounds=bounds)

            optimal_para = list(result.x)
            dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_variational_lambda(target_graph, optimal_para, pauli_ops_dict, penalty_term, initial_state)
            print('lambda:', optimal_para[-1])

        elif phase_operator_type == 'multiply_gamma':
            def obj_func(parameter_values):
                dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_multiply_gamma(target_graph, parameter_values, pauli_ops_dict, penalty_term, initial_state)
                expectation_value = (hamiltonian * dens_mat).trace().real
                return expectation_value * (-1.0)

            result = minimize(obj_func, initial_parameter, method="BFGS")
            optimal_para = list(result.x)
            dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz_multiply_gamma(target_graph, optimal_para, pauli_ops_dict, penalty_term, initial_state)

        elif phase_operator_type == 'original':
            def obj_func(parameter_values):
                dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(target_graph, parameter_values, pauli_ops_dict, penalty_term, initial_state)
                expectation_value = (hamiltonian * dens_mat).trace().real
                return expectation_value * (-1.0)

            result = minimize(obj_func, initial_parameter, method="BFGS")
            optimal_para = list(result.x)
            dens_mat = unconstrained_operators.build_MIS_unconstrained_QAOAnsatz(target_graph, optimal_para, pauli_ops_dict, penalty_term, initial_state)

        #! use Hamiltonian without penalty to calculate the AR
        hamiltonian = constrained_operators.MIS_hamiltonian(G)
        hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
        approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution


    evaluation = result.nfev
    # if(phase_operator_type == 'variational_lambdas' or phase_operator_type == 'variational_lambda'):
    #     iteration = round(optimal_para[-1], 3)
    # else:
    iteration = result.nit

    # print('solution hamiltonian eigenvalue:', max_ham_eigenvalue)
    # print('Hamiltonian expectation:', hamiltonian_expectation)
    print('AR:', approx_ratio)

    dens_mat = dens_mat.todense()
    v = dens_mat[:,0]
    v = v/np.sqrt(v[0])
    probabilities = np.array(np.square(np.abs(v)))
    
    res = calculate_pro(G, probabilities, solution)
    feasible_pro = res[0]
    optimal_pro = res[1]

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
    # print('optimal_parameters:', np.array(optimal_para)/3.1415, "pi")
    print('--------------------------------------------------------')

    if(save):
        if(use_constrain_operator == False):
            with open(f"./results/MIS/QAOA/{phase_operator_type}/MIS_QAOA{no_vertices}_{p}_{depth}_{phase_operator_type}.csv", "a") as f:
            # with open(f"./results/MIS/unconstrained_QAOA{depth}.csv", "a") as f:
            # with open(f"./results/MIS/tmp/unconstrained_QAOA{depth}.csv", "a") as f:
                f.write(f'MIS_unconstrained_QAOA {phase_operator_type}, {no_vertices}, {p}, {seed}, {penalty_term}, {depth}, {approx_ratio}, {feasible_pro}, {optimal_pro}, {evaluation}, {iteration}\n')

        if(use_constrain_operator == True):
            with open(f"./results/MIS/constrained_QAOA{depth}.csv", "a") as f:
                f.write(f'MIS_constrained_QAOA, {no_vertices}, ER0.5, {depth}, {seed}, {approx_ratio}\n')

    # return v
    # return [x[0] for x in probabilities]


def MIS_MA_QAOA(G, depth, penalty_term, initial_state = [], save = False, seed = -1):
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
    approx_ratio = (hamiltonian_expectation + solution - max_ham_eigenvalue) / solution

    # print('***************')
    # print("目标函数总调用次数:", result.nfev)
    # print(f'total iteration: {result.nit}')
    # print(f"Minimize time: {execution_time}s")
    # print(f"simulation time: {sum(simulation_time)}s")
    # print("optimal parameters:", np.array(parameter_list)/3.1415, "pi")
    print(f'AR: {approx_ratio}')

    dens_mat = dens_mat.todense()
    v = dens_mat[:,0]
    v = v/np.sqrt(v[0])
    probabilities = np.array(np.square(np.abs(v)))

    res = calculate_pro(G, probabilities, solution)
    feasible_pro = res[0]
    optimal_pro = res[1]
    
    if(save):
        with open(f'results/MIS/MA-QAOA/MA-QAOA{depth}.csv', 'a') as f:
            f.write(f'MIS_MA-QAOA, {no_vertices}, {penalty_term}, {depth}, {seed}, {approx_ratio}\n')