import csv

star_AR = []
star_rounds = []
star_evaluations = []
star_time = []
star_simul_time = []

with open(f'results/tmp_star_graph.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        star_AR += [float(row[-5])]
        star_evaluations += [int(row[-4])]        
        star_rounds += [float(row[-3])]
        star_time += [float(row[-2])]
        star_simul_time += [float(row[-1])]

n = 4
j = 4
for i in star_AR:
    n+=1
    if(i > 0.99):
        j+=1


print(j)
print(j/n)