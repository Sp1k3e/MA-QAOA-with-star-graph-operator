import networkx as nx
import matplotlib.pylab  as plt
import re
import ast

def read_parameters(file_path, rounding):
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
    
    parameter_list = gammas + betas
    if rounding:
        for i in range(len(parameter_list)):
            if abs(parameter_list[i]) < 0.35:
                parameter_list[i] = 0;
            if parameter_list[i] > -0.9 and parameter_list[i] < -0.6:
                parameter_list[i] = -0.7854

    return parameter_list


def save_pic_para(file_path):
    return 1