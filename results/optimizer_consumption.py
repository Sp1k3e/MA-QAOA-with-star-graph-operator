import csv

"""
optimizer time and rounds
"""

star_AR = []
star_rounds = []
star_evaluations = []
star_time = []
star_simul_time = []

MA_AR = []
MA_rounds = []
MA_evaluations = []
MA_time = []
MA_simul_time = []

MA2_AR = []
MA2_rounds = []
MA2_evaluations = []
MA2_time = []
MA2_simul_time = []

QAOA3_AR = []
QAOA3_rounds = []
QAOA3_evaluations = []
QAOA3_time = []
QAOA3_simul_time = []

QAOA5_AR = []
QAOA5_rounds = []
QAOA5_evaluations = []
QAOA5_time = []
QAOA5_simul_time = []


with open(f'results/optimizer_consumption/star_graph.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        star_AR += [float(row[-5])]
        star_evaluations += [int(row[-4])]        
        star_rounds += [float(row[-3])]
        star_time += [float(row[-2])]
        star_simul_time += [float(row[-1])]

with open(f'results/optimizer_consumption/MA1.csv') as f:
# with open(f'results/tmp_MA1.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        MA_AR += [float(row[-5])]
        MA_evaluations += [int(row[-4])]        
        MA_rounds += [float(row[-3])]
        MA_time += [float(row[-2])]
        MA_simul_time += [float(row[-1])]

with open(f'results/optimizer_consumption/MA2.csv') as f:
# with open(f'results/tmp_MA2.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        MA2_AR += [float(row[-5])]
        MA2_evaluations += [int(row[-4])]        
        MA2_rounds += [float(row[-3])]
        MA2_time += [float(row[-2])]
        MA2_simul_time += [float(row[-1])]

with open(f'results/optimizer_consumption/QAOA3.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        QAOA3_AR += [float(row[-5])]
        QAOA3_evaluations += [int(row[-4])]        
        QAOA3_rounds += [float(row[-3])]
        QAOA3_time += [float(row[-2])]
        QAOA3_simul_time += [float(row[-1])]

with open(f'results/optimizer_consumption/QAOA5.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        QAOA5_AR += [float(row[-5])]
        QAOA5_evaluations += [int(row[-4])]        
        QAOA5_rounds += [float(row[-3])]
        QAOA5_time += [float(row[-2])]
        QAOA5_simul_time += [float(row[-1])]


print("star graph")
print(sum(star_evaluations)/len(star_evaluations))
print(sum(star_rounds)/len(star_rounds))
print(sum(star_time)/len(star_time))
print(sum(star_simul_time)/len(star_simul_time))
print("optimizer time:", sum(star_time)/len(star_time) - sum(star_simul_time)/len(star_simul_time))
print(sum(star_AR)/len(star_AR))
print("------------------------------")

print("MA1")
print(sum(MA_evaluations)/len(MA_evaluations))
print(sum(MA_rounds)/len(MA_rounds))
print(sum(MA_time)/len(MA_time))
print(sum(MA_simul_time)/len(MA_simul_time))
print("optimizer time:", sum(MA_time)/len(MA_time) - sum(MA_simul_time)/len(MA_simul_time))
print(sum(MA_AR)/len(MA_AR))
print("------------------------------")

print("MA2")
print(sum(MA2_evaluations)/len(MA2_evaluations))
print(sum(MA2_rounds)/len(MA2_rounds))
print(sum(MA2_time)/len(MA2_time))
print(sum(MA2_simul_time)/len(MA2_simul_time))
print("optimizer time:", sum(MA2_time)/len(MA2_time) - sum(MA2_simul_time)/len(MA2_simul_time))
print(sum(MA2_AR)/len(MA2_AR))
print("------------------------------")

print("QAOA3")
print(sum(QAOA3_evaluations)/len(QAOA3_evaluations))
print(sum(QAOA3_rounds)/len(QAOA3_rounds))
print(sum(QAOA3_time)/len(QAOA3_time))
print(sum(QAOA3_simul_time)/len(QAOA3_simul_time))
print("optimizer time:", sum(QAOA3_time)/len(QAOA3_time) - sum(QAOA3_simul_time)/len(QAOA3_simul_time))
print(sum(QAOA3_AR)/len(QAOA3_AR))
print("------------------------------")

print("QAOA5")
print(sum(QAOA5_evaluations)/len(QAOA5_evaluations))
print(sum(QAOA5_rounds)/len(QAOA5_rounds))
print(sum(QAOA5_time)/len(QAOA5_time))
print(sum(QAOA5_simul_time)/len(QAOA5_simul_time))
print("optimizer time:", sum(QAOA5_time)/len(QAOA5_time) - sum(QAOA5_simul_time)/len(QAOA5_simul_time))
print(sum(QAOA5_AR)/len(QAOA5_AR))
print("------------------------------")