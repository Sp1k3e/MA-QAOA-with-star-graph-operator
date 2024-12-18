import csv
import matplotlib.pyplot as plt

n = '8'
depth = '1'
counts = 0
QAOA = []
TR_QAOA = []
TR_Most_MA = []
TR_All_MA = []
MA = []
skip_seed = []

# TR-QAOA
with open('results/QAOA/TR_QAOA.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')

    i = 0
    for row in csvreader:
        if row[-3] == depth and row[1] == n:
            if str(i) != row[-2]:
                skip_seed += [str(i)]
                i += 1

            i += 1
            counts += 1
            TR_QAOA += [float(row[-1])]
print(f'skip seed {skip_seed}')    

# QAOA
with open('results/QAOA/QAOA.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    for row in csvreader:
        if row[-3] == depth and row[1] == n:
            if row[-2] in skip_seed:
                continue

            QAOA += [float(row[-1])]

# TR-All MA-QAOA
with open('results/MA-QAOA/TR_All_MA.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == depth and row[1] == n:
            if row[-2] in skip_seed:
                continue

        TR_All_MA += [float(row[-1])]

with open('results/MA-QAOA/TR_Most_MA.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == depth and row[1] == n:
            if row[-2] in skip_seed:
                continue

        TR_Most_MA += [float(row[-1])]

# MA-QAOA
with open('results/MA-QAOA/MA-QAOA.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == depth and row[1] == n:
            if row[-2] in skip_seed:
                continue

        MA += [float(row[-1])]



l = len(TR_All_MA)
print('average AR:')
print(f'TR-QAOA:        {sum(TR_QAOA)/l}')
print(f'QAOA:           {sum(QAOA)/l}')
print(f'TR-Most MA-QAOA:{sum(TR_Most_MA)/l}')
print(f'TR-All MA-QAOA: {sum(TR_All_MA)/l}')
print(f'MA-QAOA:        {sum(MA)/l}')


#box plot
all_data = [QAOA, TR_Most_MA, TR_All_MA, MA,]
# labels = ['QAOA', 'TRMA-QAOA', 'MA-QAOA']
labels = ['QAOA', 'TR-Most MA-QAOA', 'TR-All MA-QAOA', 'MA-QAOA']

positions = [0.1, 0.2, 0.3, 0.4]

fig, ax = plt.subplots()
bplot = ax.boxplot(all_data,patch_artist=True, positions=positions, showfliers=False, widths=0.08)
plt.axhline(y=1, color='black', linestyle='--', label='Horizontal Dashed Line')

colors = ['pink', 'green', 'lightblue', 'red']  # 可以根据需要选择更多颜色
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

ax.legend(bplot['boxes'], labels)

ax.set_title('Approximate Ratio')
ax.set_xlabel('p')
ax.set_ylabel('AR')

ax.set_xticks([0.2])
ax.set_xticklabels(['1'])

plt.show()