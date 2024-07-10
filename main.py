import MA_QAOA_All

n = 10
layer = 1
graph_type = 'regular'
for seed in range(10):
    MA_QAOA_All.MA_All(n, layer, seed)
