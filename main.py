import MA_QAOA_All
import heuristic_MA

n = 10
layer = 1
seed = 3
graph_type = ['random', 0.5]
# graph_type = ['regular', 3]
save = True

MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)

# for seed in range(10):
#     print('#')
#     MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)

# MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)
# heuristic_MA.mst(n,layer, seed, graph_type, False)