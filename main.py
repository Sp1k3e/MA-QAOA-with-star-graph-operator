import MA_QAOA_All
import heuristic_MA
import standard_QAOA

n = 6
seed = 0
graph_type = ['random', 0.6]
# graph_type = ['regular', 3]
save = False

# minimize_method = 'Nelder-Mead'
minimize_method = 'BFGS'
layer = 1

# for seed in range(100):
    # print('#')
    # standard_QAOA.QAOA(n, layer, seed, graph_type, save)
    # MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)
    # heuristic_MA.select_MA(n, layer, seed, graph_type, save) 
    # heuristic_MA.random_select_MA(n, layer, seed, graph_type, save)

standard_QAOA.QAOA(n, layer, seed, graph_type, save)
# MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, minimize_method=minimize_method)

#! heuristic_MA
# heuristic_MA.select_MA(n, layer, seed, graph_type, True)
# heuristic_MA.select_layer2_MA(n, seed, graph_type, False)
# heuristic_MA.random_select_MA(n, layer, seed, graph_type, save)