from matplotlib import pyplot as plt
import csv
import numpy as np

n = 8
p = 0.4

QAOA_AR = []
QAOA_feasible = []
QAOA_optimal = []
QAOA2_AR = []
QAOA2_feasible = []
QAOA2_optimal = []
QAOA3_AR = []
QAOA3_feasible = []
QAOA3_optimal = []
QAOA4_AR = []
QAOA4_feasible = []
QAOA4_optimal = []

QAOA_fewer_RZ_AR = []
QAOA_fewer_RZ_feasible = []
QAOA_fewer_RZ_optimal = []
QAOA2_fewer_RZ_AR = []
QAOA2_fewer_RZ_feasible = []
QAOA2_fewer_RZ_optimal = []
QAOA3_fewer_RZ_AR = []
QAOA3_fewer_RZ_feasible = []
QAOA3_fewer_RZ_optimal = []
QAOA4_fewer_RZ_AR = []
QAOA4_fewer_RZ_feasible = []
QAOA4_fewer_RZ_optimal = []

QAOA_additional_RX_AR = []
QAOA_additional_RX_feasible = []
QAOA_additional_RX_optimal = []
QAOA2_additional_RX_AR = []
QAOA2_additional_RX_feasible = []
QAOA2_additional_RX_optimal = []
QAOA3_additional_RX_AR = []
QAOA3_additional_RX_feasible = []
QAOA3_additional_RX_optimal = []
QAOA4_additional_RX_AR = []
QAOA4_additional_RX_feasible = []
QAOA4_additional_RX_optimal = []

MA_AR = []
MA_feasible = []
MA_optimal = []
MA2_AR = []
MA2_feasible = []
MA2_optimal = []

def readCSV(filename, AR, feasible, optimal):
    with open(filename) as f:
        csvreader = csv.reader(f, delimiter=',')

        for row in csvreader:
            AR += [float(row[6])]
            feasible += [float(row[7])]
            optimal += [float(row[8])]

readCSV(f'results/MIS/customized/MIS_QAOA{n}_{p}_1_.csv', QAOA_AR, QAOA_feasible, QAOA_optimal)
readCSV(f'results/MIS/customized/fewer_RZ/MIS_QAOA{n}_{p}_1_fewer_RZ.csv', QAOA_fewer_RZ_AR, QAOA_fewer_RZ_feasible, QAOA_fewer_RZ_optimal)
readCSV(f'results/MIS/customized/additional_RX/MIS_QAOA{n}_{p}_1_additional_RX.csv', QAOA_additional_RX_AR, QAOA_additional_RX_feasible, QAOA_additional_RX_optimal)

readCSV(f'results/MIS/customized/MIS_QAOA{n}_{p}_2_.csv', QAOA2_AR, QAOA2_feasible, QAOA2_optimal)
readCSV(f'results/MIS/customized/fewer_RZ/MIS_QAOA{n}_{p}_2_fewer_RZ.csv', QAOA2_fewer_RZ_AR, QAOA2_fewer_RZ_feasible, QAOA2_fewer_RZ_optimal)
readCSV(f'results/MIS/customized/additional_RX/MIS_QAOA{n}_{p}_2_additional_RX.csv', QAOA2_additional_RX_AR, QAOA2_additional_RX_feasible, QAOA2_additional_RX_optimal)

readCSV(f'results/MIS/customized/MIS_QAOA{n}_{p}_3_.csv', QAOA3_AR, QAOA3_feasible, QAOA3_optimal)
readCSV(f'results/MIS/customized/fewer_RZ/MIS_QAOA{n}_{p}_3_fewer_RZ.csv', QAOA3_fewer_RZ_AR, QAOA3_fewer_RZ_feasible, QAOA3_fewer_RZ_optimal)
readCSV(f'results/MIS/customized/additional_RX/MIS_QAOA{n}_{p}_3_additional_RX.csv', QAOA3_additional_RX_AR, QAOA3_additional_RX_feasible, QAOA3_additional_RX_optimal)

readCSV(f'results/MIS/customized/MIS_QAOA{n}_{p}_4_.csv', QAOA4_AR, QAOA4_feasible, QAOA4_optimal)
readCSV(f'results/MIS/customized/fewer_RZ/MIS_QAOA{n}_{p}_4_fewer_RZ.csv', QAOA4_fewer_RZ_AR, QAOA4_fewer_RZ_feasible, QAOA4_fewer_RZ_optimal)
readCSV(f'results/MIS/customized/additional_RX/MIS_QAOA{n}_{p}_4_additional_RX.csv', QAOA4_additional_RX_AR, QAOA4_additional_RX_feasible, QAOA4_additional_RX_optimal)

positions = ['1', '2', '3','4'] # different layer
x = np.arange(len(positions))
width = 0.2

QAOA_AR = [np.average(QAOA_AR), np.average(QAOA2_AR), np.average(QAOA3_AR), np.average(QAOA4_AR)]
QAOA_feasible = [np.average(QAOA_feasible), np.average(QAOA2_feasible), np.average(QAOA3_feasible), np.average(QAOA4_feasible)]
QAOA_optimal = [np.average(QAOA_optimal), np.average(QAOA2_optimal), np.average(QAOA3_optimal), np.average(QAOA4_optimal)]

QAOA_fewer_RZ_AR = [np.average(QAOA_fewer_RZ_AR), np.average(QAOA2_fewer_RZ_AR), np.average(QAOA3_fewer_RZ_AR), np.average(QAOA4_fewer_RZ_AR)]
QAOA_fewer_RZ_feasible = [np.average(QAOA_fewer_RZ_feasible), np.average(QAOA2_fewer_RZ_feasible), np.average(QAOA3_fewer_RZ_feasible), np.average(QAOA4_fewer_RZ_feasible)]
QAOA_fewer_RZ_optimal = [np.average(QAOA_fewer_RZ_optimal), np.average(QAOA2_fewer_RZ_optimal), np.average(QAOA3_fewer_RZ_optimal), np.average(QAOA4_fewer_RZ_optimal)] 

QAOA_additional_RX_AR = [np.average(QAOA_additional_RX_AR), np.average(QAOA2_additional_RX_AR), np.average(QAOA3_additional_RX_AR), np.average(QAOA4_additional_RX_AR)]
QAOA_additional_RX_feasible = [np.average(QAOA_additional_RX_feasible), np.average(QAOA2_additional_RX_feasible), np.average(QAOA3_additional_RX_feasible), np.average(QAOA4_additional_RX_feasible)]
QAOA_additional_RX_optimal = [np.average(QAOA_additional_RX_optimal), np.average(QAOA2_additional_RX_optimal), np.average(QAOA3_additional_RX_optimal), np.average(QAOA4_additional_RX_optimal)] 

# AR
plt.figure()
plt.bar(x - width, QAOA_AR, width, label='QAOA')
plt.bar(x, QAOA_fewer_RZ_AR, width, label='QAOA_fewer_RZ')
plt.bar(x + width, QAOA_additional_RX_AR, width, label='QAOA_additional_RX')

# plt.title('AR')
plt.ylabel('AR')
plt.xlabel('p')
plt.xticks(x, positions)
plt.legend()

plt.tight_layout()
plt.savefig(f'results/MIS/MIS_diagram/{n}_{p}tmp_AR.pdf', format = 'pdf')


# feasible
plt.figure()
plt.bar(x - width, QAOA_feasible, width, label='QAOA')
plt.bar(x, QAOA_fewer_RZ_feasible, width, label='QAOA_fewer_RZ')
plt.bar(x + width, QAOA_additional_RX_feasible, width, label='QAOA_additional_RX')

plt.ylabel('probability of feasible solution')
plt.xlabel('p')
plt.xticks(x, positions)
plt.legend()

plt.tight_layout()
plt.savefig(f'results/MIS/MIS_diagram/{n}_{p}tmp_feasible.pdf', format = 'pdf')


# optimal
plt.figure()
plt.bar(x - width, QAOA_optimal, width, label='QAOA')
plt.bar(x, QAOA_fewer_RZ_optimal, width, label='QAOA_fewer_RZ')
plt.bar(x + width, QAOA_additional_RX_optimal, width, label='QAOA_additional_RX')

plt.ylabel('probability of optimal solution')
plt.xlabel('p')
plt.xticks(x, positions)
plt.legend()

plt.tight_layout()
plt.savefig(f'results/MIS/MIS_diagram/{n}_{p}tmp_optimal.pdf', format = 'pdf')