from matplotlib import pyplot as plt
import csv
import numpy as np

n = 8
p = 0.4

QAOA_AR = [[] for _ in range(5)]
QAOA_feasible = [[] for _ in range(5)]
QAOA_optimal = [[] for _ in range(5)]

QAOA_fewer_RZ_AR = [[] for _ in range(5)]
QAOA_fewer_RZ_feasible = [[] for _ in range(5)]
QAOA_fewer_RZ_optimal = [[] for _ in range(5)]

QAOA_additional_RX_AR = [[] for _ in range(5)]
QAOA_additional_RX_feasible = [[] for _ in range(5)]
QAOA_additional_RX_optimal = [[] for _ in range(5)]

QAOA_variational_lambda_AR = [[] for _ in range(5)]
QAOA_variational_lambda_feasible = [[] for _ in range(5)]
QAOA_variational_lambda_optimal = [[] for _ in range(5)]

QAOA_variational_lambdas_AR = [[] for _ in range(5)]
QAOA_variational_lambdas_feasible = [[] for _ in range(5)]
QAOA_variational_lambdas_optimal = [[] for _ in range(5)]

def readCSV(filename, AR, feasible, optimal):
    with open(filename) as f:
        csvreader = csv.reader(f, delimiter=',')

        for row in csvreader:
            AR += [float(row[6])]
            feasible += [float(row[7])]
            optimal += [float(row[8])]

for layer in range(5):
    readCSV(f'results/MIS/QAOA/original/MIS_QAOA{n}_{p}_{layer+1}_original.csv', QAOA_AR[layer], QAOA_feasible[layer], QAOA_optimal[layer])
    readCSV(f'results/MIS/QAOA/fewer_RZ/MIS_QAOA{n}_{p}_{layer+1}_fewer_RZ.csv', QAOA_fewer_RZ_AR[layer], QAOA_fewer_RZ_feasible[layer], QAOA_fewer_RZ_optimal[layer])
    readCSV(f'results/MIS/QAOA/additional_RX/MIS_QAOA{n}_{p}_{layer+1}_additional_RX.csv', QAOA_additional_RX_AR[layer], QAOA_additional_RX_feasible[layer], QAOA_additional_RX_optimal[layer])
    readCSV(f'results/MIS/QAOA/variational_lambda/MIS_QAOA{n}_{p}_{layer+1}_variational_lambda.csv', QAOA_variational_lambda_AR[layer], QAOA_variational_lambda_feasible[layer], QAOA_variational_lambda_optimal[layer])
    readCSV(f'results/MIS/QAOA/variational_lambdas/MIS_QAOA{n}_{p}_{layer+1}_variational_lambdas.csv', QAOA_variational_lambdas_AR[layer], QAOA_variational_lambdas_feasible[layer], QAOA_variational_lambdas_optimal[layer])


QAOA_AR = [np.average(i) for i in QAOA_AR]
QAOA_feasible = [np.average(i) for i in QAOA_feasible]
QAOA_optimal = [np.average(i) for i in QAOA_optimal]

QAOA_additional_RX_AR = [np.average(i) for i in QAOA_additional_RX_AR]
QAOA_additional_RX_feasible = [np.average(i) for i in QAOA_additional_RX_feasible]
QAOA_additional_RX_optimal = [np.average(i) for i in QAOA_additional_RX_optimal]

QAOA_fewer_RZ_AR = [np.average(i) for i in QAOA_fewer_RZ_AR]
QAOA_fewer_RZ_feasible = [np.average(i) for i in QAOA_fewer_RZ_feasible]
QAOA_fewer_RZ_optimal = [np.average(i) for i in QAOA_fewer_RZ_optimal]

QAOA_variational_lambda_AR = [np.average(i) for i in QAOA_variational_lambda_AR]
QAOA_variational_lambda_feasible = [np.average(i) for i in QAOA_variational_lambda_feasible]
QAOA_variational_lambda_optimal = [np.average(i) for i in QAOA_variational_lambda_optimal]

QAOA_variational_lambdas_AR = [np.average(i) for i in QAOA_variational_lambdas_AR]
QAOA_variational_lambdas_feasible = [np.average(i) for i in QAOA_variational_lambdas_feasible]
QAOA_variational_lambdas_optimal = [np.average(i) for i in QAOA_variational_lambdas_optimal]

# draw diagram
positions = ['1', '2', '3','4','5'] # different layer
x = np.arange(len(positions))
width = 0.2
offsets = [x - 3*width/2, x - width/2, x + width/2, x+3*width/2]

# AR
plt.figure()
plt.bar(offsets[0], QAOA_AR, width, label='QAOA')
# plt.bar(x, QAOA_fewer_RZ_AR, width, label='QAOA_fewer_RZ')
plt.bar(offsets[1], QAOA_variational_lambda_AR, width, label='QAOA_variational_lambda')
plt.bar(offsets[2], QAOA_variational_lambdas_AR, width, label='QAOA_variational_lambdas')
plt.bar(offsets[3], QAOA_additional_RX_AR, width, label='QAOA_additional_RX')

# plt.title('AR')
plt.ylabel('AR')
plt.xlabel('p')
plt.xticks(x, positions)
plt.legend()

plt.tight_layout()
plt.savefig(f'results/MIS/MIS_diagram/{n}_{p}tmp_AR.pdf', format = 'pdf')


# feasible
plt.figure()
plt.bar(offsets[0], QAOA_feasible, width, label='QAOA')
# plt.bar(x, QAOA_fewer_RZ_feasible, width, label='QAOA_fewer_RZ')
plt.bar(offsets[1], QAOA_variational_lambda_feasible, width, label='variational-$\lambda$ QAOA')
plt.bar(offsets[2], QAOA_variational_lambdas_feasible, width, label='variational-$\lambda$s QAOA')
plt.bar(offsets[3], QAOA_additional_RX_feasible, width, label='additional-RX QAOA')

plt.ylim(0,1)
plt.ylabel('probability of feasible solution')
plt.xlabel('p')
plt.xticks(x, positions)
plt.legend()

plt.tight_layout()
plt.savefig(f'results/MIS/MIS_diagram/{n}_{p}tmp_feasible.pdf', format = 'pdf')


# optimal
plt.figure()
plt.bar(offsets[0], QAOA_optimal, width, label='QAOA')
# plt.bar(x, QAOA_fewer_RZ_optimal, width, label='QAOA_fewer_RZ')
plt.bar(offsets[1], QAOA_variational_lambda_optimal, width, label='variational-$\lambda$ QAOA')
plt.bar(offsets[2], QAOA_variational_lambdas_optimal, width, label='variational-$\lambda$s QAOA')
plt.bar(offsets[3], QAOA_additional_RX_optimal, width, label='additional-RX QAOA')

plt.ylabel('probability of optimal solution')
plt.xlabel('p')
plt.xticks(x, positions)
plt.legend()

plt.tight_layout()
plt.savefig(f'results/MIS/MIS_diagram/{n}_{p}tmp_optimal.pdf', format = 'pdf')