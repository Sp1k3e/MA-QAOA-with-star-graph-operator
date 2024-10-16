from qiskit import quantum_info as qi
from scipy import sparse

no_qubits = 2
i = 0
pauli_string = 'I' * (i) + 'X' + 'I' * (no_qubits - i - 1)
pauli_string = pauli_string[::-1]
mixer_X = sparse.csr_matrix(qi.Pauli(pauli_string).to_matrix())
mixer_X = qi.Pauli(pauli_string).to_matrix()
print(f'mixer_X\n{mixer_X}')