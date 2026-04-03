import csv
import MA_QAOA_All
import heuristic_MA
import standard_QAOA
import heuristic_QAOA

n = 8
graph_type = ['random', 0.5]
skip_seed = [25, 56, 85, 92] #when set to 0.5 ER graph with 8 vertices, the graph may not be connected in these seeds

# graph_type = ['random', 0.7]
# skip_seed = []

# graph_type = ['regular', 3]
#! save
save = False # save to CSV

show = False # show the parameters of each gate of the original MA-QAOA in a graph

# minimize_method = 'Nelder-Mead'
# minimize_method = 'COBYLA'
minimize_method = 'BFGS'
layer = 1

print("save:", save)
print("minimize_method:", minimize_method)
print("---------------------------------")

for seed in range(0, 100):
    skip = False
    if(seed in skip_seed):
        continue
    # print('#')
    # standard_QAOA.QAOA(n, layer, seed, graph_type, save)
    # heuristic_QAOA.TR_QAOA(n, layer, seed, graph_type, save)

    # MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, minimize_method=minimize_method)

    # heuristic_MA.star_graph_MA(n, layer, seed, graph_type, save)

    # with open(f"./results/optimizer_consumption/expressive{layer}.csv") as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         if(row[5] == str(seed) and row[3] == ' ' + str(graph_type[1]) + ']'):
    #             if(float(row[6]) > 0.99):
    #                 skip = True    
    # if skip:
    #     continue

    # heuristic_MA.expressive_QAOA(n, layer, seed, graph_type, save)
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


# ! test specific seed
seed = 0
# seeds = [51, 57, 65, 68, 86]
# seeds = list(range(10,20))
layer = 5
#!standard-QAOA
# for seed in seeds:
    # standard_QAOA.QAOA(n, layer, seed, graph_type, save)
#     for _ in range(10):
#         standard_QAOA.QAOA(n, layer, seed, graph_type, save)

standard_QAOA.QAOA(n, layer, seed, graph_type, save)
# heuristic_QAOA.TR_QAOA(n, layer, seed, graph_type, save)

#! MA-QAOA
# seeds = list(range(100))
# for seed in seeds:
    # if(seed in skip_seed):
    #     continue
    # MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, show, minimize_method=minimize_method)
#     for _ in range(10):
#         ar = MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, show, minimize_method=minimize_method)
#         if ar > 0.99:
#             break
# MA_QAOA_All.MA_All(n, layer, seed, graph_type, save, show, minimize_method=minimize_method)

#! heuristic_MA
# for seed in seeds:
    # heuristic_MA.star_graph_MA(n, 1, seed, graph_type, save)
    # for _ in range(10):
        # heuristic_MA.star_graph_MA(n, 1, seed, graph_type, save)
# heuristic_MA.star_graph_MA(n, 1, seed, graph_type, save)

# heuristic_MA.TR_MA(n, layer, seed, graph_type, 'All', save)
# heuristic_MA.complete_MA(n, layer, seed, graph_type, save)
# heuristic_MA.sub_graph_MA(n, layer, seed, graph_type, save)