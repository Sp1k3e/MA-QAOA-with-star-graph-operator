import MA_QAOA_All
import heuristic_MA

n = 8
seed = 7
graph_type = ['random', 0.5]
# graph_type = ['regular', 3]
save = True

minimize_method = 'Nelder-Mead'
layer = 1

# for seed in range(10):
    # print('#')
    # MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)
    # heuristic_MA.select_layer2_MA(n, seed, graph_type, False) 

# MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, minimize_method='BFGS')


#! heuristic_MA
# heuristic_MA.select_MA(n, layer, seed, graph_type, True)
heuristic_MA.select_layer2_MA(n, seed, graph_type, False)