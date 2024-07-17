import MA_QAOA_All

n = 8
layer = 1
seed = 0
graph_type = ['random', 0.6]
# graph_type = ['regular', 3]
save = True

# MA_QAOA_All.MA_All(n, 1, seed, graph_type, save)


for seed in range(10):
    print('#')
    MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)

