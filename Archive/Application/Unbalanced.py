from src_code import build_operators
from src_code import useful_methods
from src_code import generate_graphs
from scipy.optimize import minimize
import numpy as np
from qiskit import quantum_info as qi
from scipy import sparse
import math

depth = 1

D = np.array([[6,10], [3,5]])
G = np.array([7,7])
optimal_value = 16

flatten_D = D.flatten()
m = len(D) #num_of_customer
n = len(G) #num_of_factory
no_qubits = m * n + n
pauli_dict = build_operators.build_my_paulis(no_qubits)

lambda0 = 1
lambda1 = 1
lambda2 = 1
 
def problem_hamiltonian():
    pauli_strings = [None] * ()
    coeffs =  [None]
    index = 0
    # cost
    for i in range(m * n):
        tmp_str = 'I' * (i) + 'Z' + 'I' * (no_qubits - i - 1)
        tmp_str = tmp_str[::-1]
        pauli_strings[i] = tmp_str
        coeffs[index] = (-0.5) * flatten_D[i]
        index += 1
    
    for i in range(n):
        tmp_str = 'I' * (m * n + i) + 'Z' + 'I' * (no_qubits - i - 1)
        tmp_str = tmp_str[::-1]
        pauli_strings[i] = tmp_str
        coeffs[index] = (-0.5) * G[i]
        index += 1

    # penalization
    for i in range(n):
        for j in range(m * n):
            tmp_str = 'I' * (i) + 'Z' + 'I' * (no_qubits - i - 1)
            tmp_str = tmp_str[::-1]
            pauli_strings[i] = tmp_str
            coeffs[index] = lambda1
            index += 1

    hamiltonian_operator = qi.SparsePauliOp(pauli_strings, np.array(coeffs)).to_operator()

    # return sparse.csr_matrix(hamiltonian_operator.data)
    return hamiltonian_operator.data
 
hamiltonian = problem_hamiltonian()
# print(hamiltonian)
max_ham_eigenvalue = max(np.linalg.eig(hamiltonian)[0])
print(max_ham_eigenvalue)


def phase_unitary(para):
    first = True
    # cost
    for i in range(m * n):
        weight = flatten_D[i]
        total_param = 0.5 * para * weight
        key = 'Z' + str(i)
        
        tmp_matrix = pauli_dict['I'] * math.cos(total_param) + pauli_dict[key] * math.sin(total_param) * 1j
        if first:
            result = tmp_matrix
            first = False
        else:
            result = tmp_matrix * result

    for i in range(n):
        weight = G[i]
        total_param = 0.5 * para * weight
        key = 'Z' + str(m * n + i)
        tmp_matrix = pauli_dict['I'] * math.cos(total_param) + pauli_dict[key] * math.sin(total_param) * 1j
        result = tmp_matrix * result

    # penalization
    for i in range():
        
    return result

def build_QAOA(parameter):
    ham_parameters = parameter[:depth]
    mixer_parameters = parameter[depth:]

    #! initial state 
    dens_mat = build_operators.initial_density_matrix(m)
    
    for layer in range(depth):
        cut_unit = phase_unitary(ham_parameters[layer])
        dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())

        mix_unit = build_operators.mixer_unitary('standard_x', mixer_parameters[layer], pauli_dict, m)
        dens_mat = (mix_unit * dens_mat) * (mix_unit.transpose().conj())

    return dens_mat


def obj_func(parameter_values):
    dens_mat = build_QAOA(parameter_values)
    expectation_value = (hamiltonian * dens_mat).trace().real
    return expectation_value * -1.0

initial_parameter = [0.1] * depth + [1] * depth

result = minimize(obj_func, initial_parameter)

parameter_list = result.x
dens_mat = build_QAOA(parameter_list)
hamiltonian_expectation = (hamiltonian * dens_mat).trace().real
print(hamiltonian_expectation)
ar = (hamiltonian_expectation + optimal_value - max_ham_eigenvalue) / optimal_value

print(f"parameter:{parameter_list}")
print(f"AR:{ar}")