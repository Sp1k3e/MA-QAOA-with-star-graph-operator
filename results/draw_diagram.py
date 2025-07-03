import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

n = '8'
# depth = '1'

graph_type = 'random0.5'
graph_type = 'random0.7'

counts = 0
TR_QAOA = []

QAOA = []
TR_Most_MA = []
TR_All_Most_MA = []
TR_All_MA = []
MA = []
MA_star = []
expressive = []

QAOA2 = []
TR_Most_MA2 = []
TR_All_MA2 = []
MA2 = []
MA_star2 = []

skip_seed = ['25', '56', '85', '92']

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


# with open(f'results/MA-QAOA/TR_All_without_Most_MA_Ne_1.csv', newline='') as f:
#     csvreader = csv.reader(f, delimiter=',')
#     next(csvreader)

#     for row in csvreader:
#         if row[-3] == '1' and row[1] == n and row[2] == graph_type:
#             if row[-2] in skip_seed:
#                 continue
#             else:
#                 TR_All_Most_MA += [float(row[-1])]


# with open(f'results/MA-QAOA/TR_All_without_Most_MA_Ne_1.csv', newline='') as f:
#     csvreader = csv.reader(f, delimiter=',')
#     next(csvreader)

#     for row in csvreader:
#         if row[-3] == '1' and row[1] == n and row[2] == graph_type:
#             if row[-2] in skip_seed:
#                 continue
#             else:
#                 TR_All_Most_MA += [float(row[-1])]

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

# MA-star graph
# with open(f'results/star-graph/star_graph1.csv', newline='') as f:
#     csvreader = csv.reader(f, delimiter=',')
#     next(csvreader)

#     for row in csvreader:
#         if row[-3] == '1' and row[1] == n and row[2] == graph_type:
#             if row[-2] in skip_seed:
#                 continue

#             MA_star += [float(row[-1])]

# with open(f'results/star-graph/star_graph2.csv', newline='') as f:
#     csvreader = csv.reader(f, delimiter=',')
#     next(csvreader)

#     for row in csvreader:
#         if row[-3] == '2' and row[1] == n and row[2] == graph_type:
#             if row[-2] in skip_seed:
#                 continue

#             MA_star2 += [float(row[-1])]


with open(f'results/optimizer_consumption/expressive1.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')
    next(csvreader)

    for row in csvreader:
        if row[3] == '1' and row[1] == str(n) and row[2] == graph_type:
            expressive += [float(row[5])]

# l = len(TR_All_MA)
# print('average AR:')
# print(f'TR-QAOA:        {sum(TR_QAOA)/l}')
# print(f'QAOA:           {sum(QAOA)/l}')
# print(f'TR-Most MA-QAOA:{sum(TR_Most_MA)/l}')
# print(f'TR-All MA-QAOA: {sum(TR_All_MA)/l}')
# print(f'MA-QAOA:        {sum(MA)/l}')

MA2 = [0.995, 0.996, 0.997, 0.99999, 1.0, 0.9999]
expressive2 = [0.995, 0.996, 0.997, 0.99999, 1.0, 0.9999]
#box plot
all_data = [QAOA, TR_Most_MA, TR_All_MA, MA, expressive, QAOA2, TR_Most_MA2, TR_All_MA2, MA2, expressive2]
labels = ['QAOA', 'TR-Most MA-QAOA', 'TR-All MA-QAOA', 'MA-QAOA', 'XQAOA', 'QAOA', 'TR-Most MA-QAOA', 'TR-All MA-QAOA', 'MA-QAOA', 'XQAOA']

positions = [1,1.5,2,2.5,3,  5,5.5,6,6.5,7]


fig, ax = plt.subplots()
# boxplot showfliers控制离异点
bplot = ax.boxplot(all_data,patch_artist=True, showfliers = False, positions=positions,  medianprops={'color': 'orange', 'linewidth': 2.5}, widths=0.44, labels=labels)

# 虚线
hline = plt.axhline(y=1, color='#ff111191', linestyle='-.', linewidth = 1.5, label='Star Graph MA-QAOA')

colors = ['pink', 'green', 'lightblue', '#0cc', '#c0c','pink', 'green', 'lightblue', '#0cc', '#c0c']  # 颜色
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)

# 图例
# handles ,labels = ax.get_legend_handles_labels()

# blegend = ax.legend(bplot['boxes'], labels[:4], loc='lower right', prop=FontProperties(size=10))

# handles.append(bplot)
# labels.append('star graph')
# ax.legend(handles=handles, labels=labels)

# hlinelegend = ax.legend()
box_proxy1 = plt.Line2D([0], [0], color='pink', lw=5, label='QAOA')
box_proxy2 = plt.Line2D([0], [0], color='green', lw=5, label='TR-Most MA-QAOA')
box_proxy3 = plt.Line2D([0], [0], color='lightblue', lw=5, label='TR-All MA-QAOA')
box_proxy4 = plt.Line2D([0], [0], color='#0cc', lw=5, label='MA-QAOA')
box_proxy5 = plt.Line2D([0], [0], color='#c0c', lw=5, label='XQAOA')
ax.legend(handles=[box_proxy1,box_proxy2,box_proxy3,box_proxy4,box_proxy5,hline], loc='lower right', prop=FontProperties(size=9))

# 标题
ax.set_title(f'Approximate Ratio on ER graph (edge probabilty = {graph_type[-3:]})')
# 横竖轴
ax.set_xlabel(r'$p$',fontsize=13)
# ax.set_xlabel('p', fontsize=14)
ax.set_ylabel('AR',fontsize = 13)

# x轴
plt.xlim(-0.5,8.5)
plt.ylim(0.68,1.02)
# plt.margins(y=1)
ax.set_yticks([0.7,0.8,0.9,1])
ax.set_yticklabels([0.7,0.8,0.9,1])
ax.set_xticks([1.75, 5.75])
ax.set_xticklabels(['1', '2'])

plt.tight_layout()
plt.savefig(f'results/performance_diagram{graph_type[-3:]}.eps', format='eps', dpi=1000)
# plt.savefig(f'results/performance_diagram{graph_type[-3:]}.pdf', format='pdf')

plt.show()


print(graph_type)

#! 平均结果
all_data_name = ['QAOA', 'TR_Most_MA', 'TR_All_MA', 'MA', 'XQAOA', 'QAOA2', 'TR_Most_MA2', 'TR_All_MA2', 'MA2', 'XQAOA2']
j = 0
for l in all_data:
    result = 0
    for i in l:
        result += i
    print(f'{all_data_name[j]}: {result/len(l)}')
    j += 1

#! TR-All和原版效果一样的例子
# n = len(TR_All_MA)
# same = 0

# for i in range(n):
#     if abs(TR_All_MA[i] - MA[i]) <= 0.005:
#         same += 1

# print(n)
# print(same)
