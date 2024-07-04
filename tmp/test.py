import networkx

G = networkx.random_regular_graph(3,8)
G.number_of_edges()

import matplotlib.pyplot as plt
networkx.draw_networkx(G)
plt.show()