import MA_QAOA_All
import heuristic_MA
import standard_QAOA
import heuristic_QAOA

n = 8
graph_type = ['random', 0.5]
skip_seed = [25, 56, 85, 92]

# graph_type = ['random', 0.7]
# skip_seed = []

# graph_type = ['regular', 3]
#! save
save = True
show = False

# minimize_method = 'Nelder-Mead'
minimize_method = 'COBYLA'
# minimize_method = 'BFGS'
layer = 5


print("save:", save)
print("minimize_method:", minimize_method)
print("---------------------------------")

for seed in range(100):
    if(seed in skip_seed):
        continue
    # print('#')
    # standard_QAOA.QAOA(n, layer, seed, graph_type, save)
    # heuristic_QAOA.TR_QAOA(n, layer, seed, graph_type, save)

    # MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, minimize_method=minimize_method)

    # ar = heuristic_MA.star_graph_MA(n, 1, seed, graph_type, save)
    # for _ in range(10):
        # ar = heuristic_MA.star_graph_MA(n, 1, seed, graph_type, save)
        # ar = MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, minimize_method=minimize_method)
        # if ar > 0.99:
            # break

    # heuristic_MA.TR_MA(n, layer, seed, graph_type, 'All',save, minimize_method)
    # heuristic_MA.TR_MA(n, layer, seed, graph_type, 'Most',save)
    # heuristic_MA.TR_MA(n, layer, seed, graph_type, 'All_without_Most',save)
    # heuristic_MA.sub_graph_MA(n, layer, seed, graph_type, save)


# !指定seed

seed = 31
# seeds = [51, 57, 65, 68, 86]
#!standard-QAOA
# for seed in seeds:
#     for _ in range(2):
#         standard_QAOA.QAOA(n, layer, seed, graph_type, save)
# heuristic_QAOA.TR_QAOA(n, layer, seed, graph_type, save)

#! MA-QAOA
# for seed in seeds:
#     for _ in range(10):
#         ar = MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, show, minimize_method=minimize_method)
#         if ar > 0.99:
#             break

#! heuristic_MA
# for _ in range(10):
    # heuristic_MA.star_graph_MA(n, 1, seed, graph_type, save)
# heuristic_MA.TR_MA(n, layer, seed, graph_type, 'All', save)
# heuristic_MA.complete_MA(n, layer, seed, graph_type, save)
# heuristic_MA.sub_graph_MA(n, layer, seed, graph_type, save)