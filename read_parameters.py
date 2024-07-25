import re
import ast

def read_parameters(file_path):
    gammas = []
    betas = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('('):
                gammas += [float(line.split(' ')[2])]
            if line.startswith("beta"):
                match = re.search(r'\[([^\]]+)\]', line)
                numbers_string = match.group(0)
                numbers_list = ast.literal_eval(numbers_string)
                betas += numbers_list

    return gammas + betas                


n = 10
p = 0.7
depth = 1
seed = 1
file_path = f"./results/parameters/{n}vertex/MA{n}_{p}random_layer{depth}_seed{seed}"
parameters = read_parameters(file_path)
print(parameters)