import MA_QAOA_All

n = 6
layer = 1
graph_type = 'random'
# graph_type = 'regular'
save = False

for seed in range(10):
    print('#')
    MA_QAOA_All.MA_All(n, layer, seed, graph_type, save)
