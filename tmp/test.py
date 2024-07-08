# import networkx

# G = networkx.random_regular_graph(3,6,1)
# G.number_of_edges()

# import matplotlib.pyplot as plt
# networkx.draw_networkx(G)
# plt.show()

import sys

# 打开文件
with open('output.txt', 'w') as f:
    # 将标准输出重定向到文件
    sys.stdout = f
    
    # 所有的 print 输出都将写入到 output.txt 文件中
    print("这是测试输出1")
    print("这是测试输出2")
    
# 恢复标准输出到原来的状态
sys.stdout = sys.__stdout__