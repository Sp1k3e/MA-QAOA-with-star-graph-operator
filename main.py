import MA_QAOA_All
import heuristic_MA
import standard_QAOA
import heuristic_QAOA

n = 8
graph_type = ['random', 0.5]
# graph_type = ['random', 0.7]
# graph_type = ['regular', 3]
# number_of_iteration = 100
#! save
save = False
show = False

# minimize_method = 'Nelder-Mead'
minimize_method = 'BFGS'
layer = 2

print("save:", save)
print("minimize_method:", minimize_method)
print("---------------------------------")

# for seed in range(87, 100):
    # print('#')
    # standard_QAOA.QAOA(n, layer, seed, graph_type, save)
    # heuristic_QAOA.TR_QAOA(n, layer, seed, graph_type, save)

    # MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, minimize_method=minimize_method)

    # heuristic_MA.star_graph_MA(n, layer, seed, graph_type, save)

    # heuristic_MA.TR_MA(n, layer, seed, graph_type, 'All',save, minimize_method)
    # heuristic_MA.TR_MA(n, layer, seed, graph_type, 'Most',save)
    # heuristic_MA.TR_MA(n, layer, seed, graph_type, 'All_without_Most',save)
    # heuristic_MA.sub_graph_MA(n, layer, seed, graph_type, save)


seed = 97
#!standard-QAOA
# standard_QAOA.QAOA(n, layer, seed, graph_type, save)
# standard_QAOA.star_graph_QAOA(n, layer, seed, graph_type, save)
# heuristic_QAOA.TR_QAOA(n, layer, seed, graph_type, save)

#! MA-QAOA
MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, show, minimize_method=minimize_method)

#! heuristic_MA
# heuristic_MA.star_graph_MA(n, layer, seed, graph_type, save)
# heuristic_MA.TR_MA(n, layer, seed, graph_type, 'All', save)
# heuristic_MA.complete_MA(n, layer, seed, graph_type, save)
# heuristic_MA.sub_graph_MA(n, layer, seed, graph_type, save)