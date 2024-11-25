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
n = D.size
pauli_dict = build_operators.build_my_paulis(n)
 
def problem_hamiltonian():
    no_ops = n
    pauli_strings = [None] * no_ops
    coeffs = [None] * no_ops
    for i in range(n):
        tmp_str = 'I' * (i) + 'Z' + 'I' * (n - i - 1)
        tmp_str = tmp_str[::-1]
        pauli_strings[i] = tmp_str
        coeffs[i] = (-0.5) * flatten_D[i]

    hamiltonian_operator = qi.SparsePauliOp(pauli_strings, np.array(coeffs)).to_operator()

    # return sparse.csr_matrix(hamiltonian_operator.data)
    return hamiltonian_operator.data
 
hamiltonian = problem_hamiltonian()
# print(hamiltonian)
max_ham_eigenvalue = max(np.linalg.eig(hamiltonian)[0])
print(max_ham_eigenvalue)


def initial_density_matrix(n):
    

def cut_unitary(para):
    first = True
    for i in range(n):
        weight = flatten_D[i]
        total_param = 0.5 * para * weight
        key = 'Z' + str(i)
        
        tmp_matrix = pauli_dict['I'] * math.cos(total_param) + pauli_dict[key] * math.sin(total_param) * 1j
        if first:
            result = tmp_matrix
            first = False
        else:
            result = tmp_matrix * result
    return result

def build_QAOA(parameter):
    ham_parameters = parameter[:depth]
    mixer_parameters = parameter[depth:]

    #! initial state |1010>
    dens_mat = build_operators.initial_density_matrix(n)
    
    for layer in range(depth):
        cut_unit = cut_unitary(ham_parameters[layer])
        dens_mat = (cut_unit * dens_mat) * (cut_unit.transpose().conj())

        #! XX+YY
        mix_unit = build_operators.mixer_unitary('standard_x', mixer_parameters[layer], pauli_dict, n)
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