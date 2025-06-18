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
import random

# no_vertices = 5

# for seed in range(100):
#     G = generate_graphs.generate_graph_type(no_vertices,['random',0.5],seed)[0]

#     MIS = nx.approximation.maximum_independent_set(G)
#     solution = len(MIS)
#     num = 0
#     vec = np.zeros(2**no_vertices)
#     for i in MIS:
#         num += 2**i
#     vec[num] = 1

#     pauli_ops_dict = build_operators.build_my_paulis(no_vertices)

#     hamiltonian = constrained_operators.MIS_hamiltonian(G)
#     max_ham_eigenvalue = (vec @ hamiltonian @ vec).real

#     # print("solution:", solution - 4)
#     # print(max_ham_eigenvalue)

#     if(max_ham_eigenvalue != solution - no_vertices/2):
#         print("False")
#         break
