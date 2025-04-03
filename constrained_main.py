import constrained_QAOA
from src_code import generate_graphs
import networkx as nx

no_vertices = 2
depth = 1
seed = 0

G = nx.Graph()
edge_list = [(0,1)]
G.add_edges_from(edge_list)

constrained_QAOA.MIS_QAOA(no_vertices, depth, G)
