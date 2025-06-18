from qiskit import quantum_info as qi
from networkx import Graph
import numpy as np
import networkx as nx
from src_code.mixers_density import *
from scipy import sparse
import math
from src_code import useful_methods

dim = 2**3

mat = np.zeros((dim,dim))
mat[0][0] = 1

# print(mat)

initial_state = [0b010]
initial_vector = np.zeros(dim)

for i in initial_state:
    initial_vector[i] = 1

initial_vector = initial_vector/np.linalg.norm(initial_vector)

density_matrix = qi.DensityMatrix(initial_vector)
print(initial_vector)
print("density matrix:\n", density_matrix)