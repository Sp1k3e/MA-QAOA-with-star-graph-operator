import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

n = '8'
depth = '1'

graph_type = 'random0.5'
# graph_type = 'random0.7'

counts = 0
TR_QAOA = []

QAOA = []
TR_Most_MA = []
TR_All_MA = []
MA = []

QAOA2 = []
TR_Most_MA2 = []
TR_All_MA2 = []
MA2 = []

skip_seed = ['25', '56', '85', '92']

# TR-QAOA
# skip_seed = []
# with open('results/QAOA/TR_QAOA.csv', newline='') as f:
#     csvreader = csv.reader(f, delimiter=',')

#     i = 0
#     for row in csvreader:
#         if row[-3] == depth and row[1] == n and row[2] == graph_type:
#             if str(i) != row[-2]:
#                 skip_seed += [str(i)]
#                 i += 1

#             i += 1
#             counts += 1
#             TR_QAOA += [float(row[-1])]
# print(f'skip seed {skip_seed}')    


# QAOA
with open(f'results/QAOA/QAOA_{depth}.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    for row in csvreader:
        if row[-3] == depth and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue

            QAOA += [float(row[-1])]

with open(f'results/QAOA/QAOA_2.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    for row in csvreader:
        if row[-3] == '2' and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue

            QAOA2 += [float(row[-1])]
# TR-All MA-QAOA
# with open('results/MA-QAOA/TR_All_MA.csv', newline='') as f:
with open(f'results/MA-QAOA/TR_All_MA_Ne_{depth}.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == depth and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue

            TR_All_MA += [float(row[-1])]

with open(f'results/MA-QAOA/TR_All_MA_Ne_2.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == '2' and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue

            TR_All_MA2 += [float(row[-1])]

# TR-Most MA-QAOA
# with open('results/MA-QAOA/TR_Most_MA.csv', newline='') as f:
with open(f'results/MA-QAOA/TR_Most_MA_Ne_{depth}.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == depth and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue
            else:
                TR_Most_MA += [float(row[-1])]

with open(f'results/MA-QAOA/TR_Most_MA_Ne_2.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == '2' and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue

            TR_Most_MA2 += [float(row[-1])]

# MA-QAOA
with open(f'results/MA-QAOA/MA-QAOA{depth}.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == depth and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue

            MA += [float(row[-1])]

with open(f'results/MA-QAOA/MA-QAOA2.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == '2' and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue

            MA2 += [float(row[-1])]


# l = len(TR_All_MA)
# print('average AR:')
# print(f'TR-QAOA:        {sum(TR_QAOA)/l}')
# print(f'QAOA:           {sum(QAOA)/l}')
# print(f'TR-Most MA-QAOA:{sum(TR_Most_MA)/l}')
# print(f'TR-All MA-QAOA: {sum(TR_All_MA)/l}')
# print(f'MA-QAOA:        {sum(MA)/l}')


#box plot
all_data = [QAOA, TR_Most_MA, TR_All_MA, MA, QAOA2, TR_Most_MA2, TR_All_MA2, MA2]
# labels = ['QAOA', 'TRMA-QAOA', 'MA-QAOA']
labels = ['QAOA', 'TR-Most MA-QAOA', 'TR-All MA-QAOA', 'MA-QAOA', 'QAOA', 'TR-Most MA-QAOA', 'TR-All MA-QAOA', 'MA-QAOA']

positions = [0.1, 0.2, 0.3, 0.4, 0.8,0.9,1.0,1.1]

fig, ax = plt.subplots()
bplot = ax.boxplot(all_data,patch_artist=True, positions=positions, showfliers=False, widths=0.08)
# 虚线
plt.axhline(y=1, color='black', linestyle='--', label='Horizontal Dashed Line')

colors = ['pink', 'green', 'lightblue', 'red','pink', 'green', 'lightblue', 'red']  # 可以根据需要选择更多颜色
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

ax.legend(bplot['boxes'], labels[:4], loc='lower right', prop=FontProperties(size=8))

ax.set_title(f'Approximate Ratio {graph_type}')
ax.set_xlabel('p')
ax.set_ylabel('AR')

ax.set_xticks([0.25, 0.95])
ax.set_xticklabels(['1', '2'])
plt.tight_layout()
# plt.savefig('results/my_plot.eps', format='eps', dpi=1000)
plt.savefig('results/my_plots.pdf', format='pdf')
plt.show()