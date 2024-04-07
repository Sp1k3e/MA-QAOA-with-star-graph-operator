import networkx
import random
from src_code import build_operators
from src_code import useful_methods
import math

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

no_vertices = 5
graph = generate_graph(no_vertices)[0]
''' draw graph
pos=networkx.circular_layout(graph)
networkx.draw_networkx(graph, pos)
labels = networkx.get_edge_attributes(graph,'weight')
for edge in labels:
    labels[edge] = round(labels[edge], 3)
tmp = networkx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
'''

hamiltonian = build_operators.cut_hamiltonian(graph=graph)
gradient_ops_dict = build_operators.build_all_mixers(graph=graph)
pauli_ops_dict = build_operators.build_all_paulis(no_vertices)
pauli_mixers_split_ops_dict = build_operators.split_all_mixers(graph)

max_cut_solution = useful_methods.find_optimal_cut(graph)
max_cut_value = max_cut_solution[1]
max_ham_eigenvalue = max_cut_solution[2]
ham_offset = max_cut_value - max_ham_eigenvalue

hamiltonian = build_operators.cut_hamiltonian(graph)
#mix_hamiltonian = build_operators.mix_hamiltonian(graph)

beta = 0
delta_t = 0.1
mix_type = 'standard_x'
ham_approx_ratios = []
cut_approx_ratios = []

max_layers = 100
layer = 0

curr_dens_mat = build_operators.initial_density_matrix(no_vertices)

def build_layer(curr_dens_mat,beta, mix_type):
    """ one layer 
    """
    cut_unit = build_operators.cut_unitary(graph,delta_t,pauli_ops_dict)
    curr_dens_mat = (cut_unit * curr_dens_mat) * (cut_unit.transpose().conj())

    mix_unit = build_operators.mixer_unitary(mix_type, beta * delta_t, pauli_ops_dict, no_vertices)
    curr_dens_mat = (mix_unit * curr_dens_mat) * (mix_unit.transpose().conj())

    return curr_dens_mat


def update_beta_mix(curr_dens_mat):
    """ find mix and beta for next layer
    """
    all_mixer_gradients = useful_methods.find_mixer_gradients(curr_dens_mat, gradient_ops_dict, pauli_ops_dict, graph, apply_ham_unitary=True) 
    best_mixer = all_mixer_gradients[0][0]

    if 'standard' not in best_mixer:
        mix_hamiltonian = pauli_ops_dict[best_mixer]
    else:
        mix_hamiltonian = build_operators.mix_hamiltonian(graph)

    A = 1j*(mix_hamiltonian*hamiltonian - hamiltonian * mix_hamiltonian) * curr_dens_mat
    expectation = A.trace().real
    return [expectation, best_mixer]


while layer < max_layers:
    layer +=1
    curr_dens_mat = build_layer(curr_dens_mat, beta, mix_type)
    [beta, mix_type] = update_beta_mix(curr_dens_mat)

    hamiltonian_expectation = (hamiltonian * curr_dens_mat).trace().real
    ham_approx_ratio = hamiltonian_expectation / max_ham_eigenvalue
    cut_approx_ratio = (hamiltonian_expectation + max_cut_value - max_ham_eigenvalue) / max_cut_value

    print("beta: ", beta, "  layer", layer, ": ", cut_approx_ratio,sep='')


