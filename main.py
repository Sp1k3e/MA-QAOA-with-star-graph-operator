import MA_QAOA_All
import heuristic_MA
import standard_QAOA
import heuristic_QAOA

n = 8
seed = 3
graph_type = ['random', 0.5]
# graph_type = ['regular', 3]
save = True
show = False

# minimize_method = 'Nelder-Mead'
minimize_method = 'BFGS'
layer = 2

for seed in range(100):
    # print('#')
    standard_QAOA.QAOA(n, layer, seed, graph_type, save)
    heuristic_QAOA.TR_QAOA(n, layer, seed, graph_type, save)

    # MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)
    # heuristic_MA.select_MA(n, layer, seed, graph_type, save) 
    # heuristic_MA.random_select_MA(n, layer, seed, graph_type, save)
    # heuristic_MA.TR_MA(n, layer, seed, graph_type, save)


#!standard-QAOA
# standard_QAOA.QAOA(n, layer, seed, graph_type, save)
# standard_QAOA.star_graph_QAOA(n, layer, seed, graph_type, save)
# heuristic_QAOA.TR_QAOA(n, layer, seed, graph_type, save)
#! MA-QAOA
# MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, show, minimize_method=minimize_method)

#! heuristic_MA
# heuristic_MA.select_MA(n, layer, seed, graph_type, True)
# heuristic_MA.select_layer2_MA(n, seed, graph_type, False)
# heuristic_MA.star_graph_MA(n, layer, seed, graph_type, save)
# heuristic_MA.TR_MA(n, layer, seed, graph_type, save)