from qiskit import quantum_info as qi
from networkx import Graph
import numpy as np
import networkx as nx
from src_code.mixers_density import *
from scipy import sparse
import math
from src_code import useful_methods

dim = 4

mat = np.zeros((dim,dim))
mat[0][0] = 1

print(mat)

# 定义一个矩阵（2x3）
A = np.array([[1, 2],
              [4, 5]])

# 定义一个向量（3x1）
v = np.array([1,2])

initial_sate = np.array([1.0,1.0])
initial_sate *= 1/math.sqrt(2)
density_matrix = qi.DensityMatrix(initial_sate)
print("density matrix:\n", density_matrix)