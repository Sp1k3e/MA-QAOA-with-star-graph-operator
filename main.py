import MA_QAOA_All

n = 6
layer = 2
seed = 0
graph_type = ['random', 0.4]
# graph_type = ['regular', 3]
# save = True
save = False

# for seed in range(10):
#     print('#')
#     MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)

MA_QAOA_All.MA_All(n, 1, seed, graph_type, save)
