from src_code import generate_graphs

seed = 5
graph = generate_graphs.generate_graph_type(8,['random', 0.5], seed)[0]

connected_v = [False] * graph.number_of_nodes()
edges = graph.edges()
degrees = dict(graph.degree())
sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
print(sorted_nodes)
selected_v = []
selected_e = []

#! 从度数较大的点找0点 
#todo 重写为函数
for n in sorted_nodes: #n[0]为点
    #如果度数一样，优先选还没被连接的点？
    if connected_v[n[0]]:
        for n1 in sorted_nodes:
            if n[1] == n1[1] and connected_v[n1[0]] == False:
                index1 = sorted_nodes.index(n)
                index2 = sorted_nodes.index(n1)
            
                sorted_nodes[index1], sorted_nodes[index2] = sorted_nodes[index2], sorted_nodes[index1]
                n = n1
    selected_v += [n[0]]
    connected_v[n[0]] = True 
    first = True 
    for edge in edges:
        if n[0] == edge[0]:
            if not connected_v[edge[1]]: #如果边上另一点还没有被连接
                connected_v[edge[1]] = True
                selected_e += [(edge)]
            else: #边上另一点被连接
                if edge[1] in selected_v:
                    continue
                if first:
                    first =False
                    continue
                # if first:
                    # first = False
                for e in selected_e:
                    if edge[1] in e:
                        selected_e.remove(e)
                        break
                # else:
                    # continue
                selected_e += [(edge)]

        elif n[0] == edge[1]:
            if not connected_v[edge[0]]:
                connected_v[edge[0]] = True
                selected_e += [(edge)]
            else:
                if edge[0] in selected_v:
                    continue
                if first:
                    first =False
                    continue
                # if first:
                    # first = False
                for e in selected_e:
                    if edge[0] in e:
                        selected_e.remove(e)
                        break
                # else:
                    # continue
                selected_e += [(edge)]

    if all(x == True for x in connected_v):
        break

print(f'selected nodes:{selected_v}')
print(f'selected edges:{selected_e}')