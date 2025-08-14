import networkx as nx

edge_list = [(0,1), (0,2)] #三角形少一条边
G = nx.Graph()
G.add_edges_from(edge_list)

no_vertices = G.number_of_nodes()

MIS = nx.approximation.maximum_independent_set(G)
# print(MIS)
MIS_value = len(MIS)
print("MIS value:", MIS_value)

binary_solution = ['0'] * no_vertices
for i in MIS:
    binary_solution[i] = '1'
solution = len(MIS)
print("MIS solution:", ''.join(binary_solution))

final_state = ['0','1','1']
result_vertices = []

for i in range(no_vertices):
    if final_state[i] == '1':
        result_vertices += [i]

probabilities = [0] * 7 + [1]
# print(result_vertices)

def calculate_pro(G, probabilities, solution):
    print("probabilities:")
    invalid_pro = 0
    optimal_pro = 0
    no_vertices = G.number_of_nodes()
    for i in range(2**no_vertices):
        if(probabilities[i] > 0.001):
            feasible = True
            current_solution = format(i, f'0{no_vertices}b')
            current_solution = current_solution[::-1]
            print(current_solution, end = ' ')

            result_vertices = []
            for j in range(no_vertices):
                if current_solution[j] == '1':
                    result_vertices += [j]
            n = len(result_vertices)

            if(n > solution):
                invalid_pro += probabilities[i]
                print("invalide solution", end = ' ')
                print(probabilities[i])
                continue

            for x in range(n):
                if feasible == False:
                    break
                for y in range(x+1, n):
                    a = result_vertices[x]
                    b = result_vertices[y]
                    if G.has_edge(a,b):
                        print(a,b, end = ' ')
                        print("invalide solution", end = ' ')
                        invalid_pro += probabilities[i]
                        feasible = False
                        break

            if feasible and n == solution:
                print("optimal solution", end = ' ')
                optimal_pro += probabilities[i]
            
            print(probabilities[i])
    print('\nresults:')
    print('  unfeasible_solution_probability: ', invalid_pro)
    print('  feasible_solution_probablity: ', 1 - invalid_pro)
    print('  optimal_solution_probablity: ', optimal_pro)
    return [float(1 - invalid_pro), float(optimal_pro)]

calculate_pro(G, probabilities, solution)