import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

n = '8'
# depth = '1'

graph_type = 'random0.5'
# graph_type = 'random0.7'

counts = 0
TR_QAOA = []

QAOA = []
TR_Most_MA = []
TR_All_Most_MA = []
TR_All_Most_MA = []
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
with open(f'results/QAOA/QAOA_1.csv', newline='') as f:
# with open(f'results/MA-QAOA/subgraph_MA_Ne_1.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    for row in csvreader:
        if row[-3] == '1' and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue

            QAOA += [float(row[-1])]

with open(f'results/QAOA/QAOA_2.csv', newline='') as f:
# with open(f'results/MA-QAOA/subgraph_MA_Ne_2.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    for row in csvreader:
        if row[-3] == '2' and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue

            QAOA2 += [float(row[-1])]

# TR-All MA-QAOA
# with open('results/MA-QAOA/TR_All_MA.csv', newline='') as f:
with open(f'results/MA-QAOA/TR_All_MA_Ne_1.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == '1' and row[1] == n and row[2] == graph_type:
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


with open(f'results/MA-QAOA/TR_All_without_Most_MA_Ne_1.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == '1' and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue
            else:
                TR_All_Most_MA += [float(row[-1])]


with open(f'results/MA-QAOA/TR_All_without_Most_MA_Ne_1.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == '1' and row[1] == n and row[2] == graph_type:
            if row[-2] in skip_seed:
                continue
            else:
                TR_All_Most_MA += [float(row[-1])]

# TR-Most MA-QAOA
# with open('results/MA-QAOA/TR_Most_MA.csv', newline='') as f:
with open(f'results/MA-QAOA/TR_Most_MA_Ne_1.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == '1' and row[1] == n and row[2] == graph_type:
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
with open(f'results/MA-QAOA/MA-QAOA1.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[-3] == '1' and row[1] == n and row[2] == graph_type:
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
# print(MA2)
# all_data = [QAOA, TR_Most_MA, TR_All_MA, MA, QAOA2, TR_Most_MA2, TR_All_MA2, MA2]
all_data = [QAOA, TR_All_Most_MA, TR_All_MA, MA, QAOA2, TR_Most_MA2, TR_All_MA2, MA2]
# labels = ['QAOA', 'TRMA-QAOA', 'MA-QAOA']
labels = ['QAOA', 'TR-Most MA-QAOA', 'TR-All MA-QAOA', 'MA-QAOA', 'QAOA', 'TR-Most MA-QAOA', 'TR-All MA-QAOA', 'MA-QAOA']

positions = [1,1.5,2,2.5, 5,5.5,6,6.5]


fig, ax = plt.subplots()
# boxplot fliter控制离异点
bplot = ax.boxplot(all_data,patch_artist=True,positions=positions,  medianprops={'color': 'orange', 'linewidth': 1.6}, widths=0.45)
# 虚线
plt.axhline(y=1, color='black', linestyle='--', linewidth = 0.8, label='Horizontal Dashed Line')

colors = ['pink', 'green', 'lightblue', 'red','pink', 'green', 'lightblue', 'red']  # 颜色
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

# 图例
ax.legend(bplot['boxes'], labels[:4], loc='lower right', prop=FontProperties(size=10))

# 标题
ax.set_title(f'Approximate Ratio with edge generation probability {graph_type[-3:]}')
# 横竖轴
ax.set_xlabel(r'$p$',fontsize=13)
# ax.set_xlabel('p', fontsize=14)
ax.set_ylabel('AR',fontsize = 13)

# x轴
plt.xlim(0,8)
plt.ylim(0.68,1.02)
# plt.margins(y=1)
ax.set_yticks([0.7,0.8,0.9,1])
ax.set_yticklabels([0.7,0.8,0.9,1])
ax.set_xticks([1.75, 5.75])
ax.set_xticklabels(['1', '2'])

plt.tight_layout()
# plt.savefig('results/my_plot.eps', format='eps', dpi=1000)
# plt.savefig('results/my_plots.pdf', format='pdf')

# plt.show()


print(graph_type)

#! 平均结果
# all_data_name = ['QAOA', 'TR_Most_MA', 'TR_All_MA', 'MA', 'QAOA2', 'TR_Most_MA2', 'TR_All_MA2', 'MA2']
# j = 0
# for l in all_data:
#     result = 0
#     for i in l:
#         result += i
#     print(f'{all_data_name[j]}: {result/len(l)}')
#     j += 1

#! TR-All和原版效果一样的例子
n = len(TR_All_MA)
same = 0

for i in range(n):
    if abs(TR_All_MA2[i] - MA2[i]) <= 0.005:
    # if TR_All_MA[i] > MA[i]: #greater 
        # print(TR_All_MA[i] - MA[i])
        same += 1

print(n)
print(same)

# same = 0
# n = len(MA2)
# for i in range(n):
#     if abs(TR_All_MA2[i] - MA2[i]) <= 0.005:
#     # if TR_All_MA2[i] > MA2[i]: 
#     #     print(TR_All_MA2[i] - MA2[i])
#         same += 1

# print(n)
# print(same)