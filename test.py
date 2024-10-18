from qiskit import quantum_info as qi
from scipy import sparse
import numpy as np

D = np.array([[6,10], [3,5]])
G = [7,7]
optimal_value = 16

print(D.size)