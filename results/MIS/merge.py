import csv

n = 8
p = 0.4

result = []
phase_operator_type = 'original'

def readCSV(filename, AR, feasible, optimal):
    with open(filename) as f:
        csvreader = csv.reader(f, delimiter=',')

        for row in csvreader:
            AR += [float(row[6])]
            feasible += [float(row[7])]
            optimal += [float(row[8])]

for layer in range(5):
    with open(f'results/MIS/QAOA/{phase_operator_type}/MIS_QAOA{n}_{p}_{layer+1}_{phase_operator_type}.csv', "w") as f:
        for row in result:
            f.write(row);
