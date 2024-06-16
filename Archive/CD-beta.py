import networkx
import random
from src_code import build_operators
from src_code import useful_methods
from sympy import symbols, Eq, solve, diff
import math
import matplotlib.pyplot as plt


def generate_graph(n, seed=1):
    graph = networkx.Graph()
    edge_list = []
    for n1 in range(n):
        for n2 in range(n1+1,n):
            edge_list.append((n1,n2))
    
    graph.add_edges_from(edge_list)
    random.seed(seed)
    weights = [random.random() for i in range(len(edge_list))]

    for index, edge in enumerate(graph.edges()):
        graph.get_edge_data(*edge)['weight'] = weights[index]

    return graph, weights

no_vertices = 8
graph = generate_graph(no_vertices)[0]

hamiltonian = build_operators.cut_hamiltonian(graph=graph)
mix_hamiltonian = build_operators.mix_hamiltonian(graph)

gradient_ops_dict = build_operators.build_all_mixers(graph=graph)
pauli_ops_dict = build_operators.build_all_paulis(no_vertices)
pauli_mixers_split_ops_dict = build_operators.split_all_mixers(graph)

max_cut_solution = useful_methods.find_optimal_cut(graph)
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]
ham_offset = max_cut_value - max_ham_eigenvalue

beta = 1
beta_last = 0
delta_t = 0.08
#delta_ts =[0.2,0.15,0.1,0.08,0.06,0.04,0.02]
mix_type = 'standard_x'
ham_approx_ratios = []
hamiltonian_expectation_t = 0
cut_approx_ratios = [0]

max_layers = 20
layer = 0

curr_dens_mat = build_operators.initial_density_matrix(no_vertices)

def get_alpha(beta_last):
    """get alpha for a layer to compute beta
    need to know beta?
    """
    H_deri_lambda = delta_t * mix_hamiltonian / (delta_t + beta_last)
    H_lambda = delta_t * hamiltonian + beta_last * mix_hamiltonian
    '''
    A_alpha = 1j * alpha *(H_lambda * H_deri_lambda - H_deri_lambda * H_lambda)

    S = H_deri_lambda - 1j*(A_alpha*H_lambda - H_lambda * A_alpha)
    S = (S * S).trace()
    dS = diff(S, alpha)
    alpha = solve(Eq(dS, 0), alpha)
    print(alpha)
    '''
    commutor = H_lambda * H_deri_lambda - H_deri_lambda * H_lambda
    alpha = (commutor * commutor).trace().real
    commutor2 = commutor * H_lambda - H_lambda * commutor
    alpha = alpha / (commutor2 * commutor2).trace().real

    print(alpha)
    return alpha


def build_layer(curr_dens_mat,beta, mix_type, delta_t):
    """ one layer 
    """
    cut_unit = build_operators.cut_unitary(graph,delta_t,pauli_ops_dict)
    curr_dens_mat = (cut_unit * curr_dens_mat) * (cut_unit.transpose().conj())

    mix_unit = build_operators.mixer_unitary(mix_type, beta * delta_t, pauli_ops_dict, no_vertices)
    curr_dens_mat = (mix_unit * curr_dens_mat) * (mix_unit.transpose().conj())

    return curr_dens_mat


def update_beta(beta_last):
    """retrive beta directly 
    without measurement
    """
    gamma = delta_t
    lambda_last = gamma / (gamma + beta_last)

    beta = -2 * gamma * get_alpha(beta_last) + 2 * lambda_last * gamma
    beta = beta / (gamma - 2 * lambda_last)

    return beta


#with open("adapt_feed_back_result.txt",'a') as f:   
#    print("v=", no_vertices,"delta_t=", delta_t, file=f)

while layer < max_layers:
    layer +=1
    curr_dens_mat = build_layer(curr_dens_mat, beta, mix_type, delta_t)
    hamiltonian_expectation = (hamiltonian * curr_dens_mat).trace().real
    cut_approx_ratios.append((hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value)

    print("layer", layer, ": ", format(cut_approx_ratios[layer],'.10f'), "  beta: ", format(beta, '.8f'),sep='')
    beta_last = beta
    beta = update_beta(beta_last)




'''
    with open("adapt_feed_back_result.txt",'a') as f:   
        print("layer", layer, ': ', format(cut_approx_ratios[layer],'.10f'), "  beta: ", beta,"  mix_type: ", mix_type, sep='', file = f)
'''

'''
plt.plot(cut_approx_ratios[1:])

plt.title('node= ', no_vertices)
plt.xlabel('layer')
plt.ylabel('Approximate ratio')

plt.show()
'''