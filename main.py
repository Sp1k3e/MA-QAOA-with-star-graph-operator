import MA_QAOA_All
import heuristic_MA

n = 8
layer = 1
seed = 2
graph_type = ['random', 0.5]
# graph_type = ['regular', 3]
save = True

minimize_method = 'Nelder-Mead'

# for seed in range(10):
#     print('#')
#     MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)

# MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, minimize_method='BFGS')

#! heuristic_MA
# heuristic_MA.mst(n,layer, seed, graph_type, False)
heuristic_MA.select_MA(n, layer, seed, graph_type, True)
# heuristic_MA.select_layer2_MA(n, seed, graph_type, False)