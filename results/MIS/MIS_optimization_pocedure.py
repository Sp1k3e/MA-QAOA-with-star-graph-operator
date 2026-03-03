import csv
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.font_manager import FontProperties


QAOA1=[0 for _ in range(2000)]
QAOA2=[0 for _ in range(2000)]
QAOA3=[0 for _ in range(2000)]
QAOA4=[0 for _ in range(2000)]

with open('results/MIS/optimization_pocedure/original_6.csv',) as f:
    csvreader = csv.reader(f, delimiter=',')

    count = 0
    for row in csvreader:
        count+=1
        current_len = int(len(row))
        for i in range(2000):
            if(i >= current_len):
                QAOA1[i]+=float(row[current_len-1])
            else:
                QAOA1[i]+=float(row[i])
    QAOA1 = [x/count for x in QAOA1]

with open('results/MIS/optimization_pocedure/variational_lambda_6.csv',) as f:
    csvreader = csv.reader(f, delimiter=',')

    count = 0
    for row in csvreader:
        count+=1
        current_len = int(len(row))
        for i in range(2000):
            if(i >= current_len):
                QAOA2[i]+=float(row[current_len-1])
            else:
                QAOA2[i]+=float(row[i])
    QAOA2 = [x/count for x in QAOA2]

with open('results/MIS/optimization_pocedure/variational_lambdas_6.csv',) as f:
    csvreader = csv.reader(f, delimiter=',')

    count = 0
    for row in csvreader:
        count+=1
        current_len = int(len(row))
        for i in range(2000):
            if(i >= current_len):
                QAOA3[i]+=float(row[current_len-1])
            else:
                QAOA3[i]+=float(row[i])
    QAOA3 = [x/count for x in QAOA3]

with open('results/MIS/optimization_pocedure/additional_RX_6.csv',) as f:
    csvreader = csv.reader(f, delimiter=',')

    count = 0
    for row in csvreader:
        count+=1
        current_len = int(len(row))
        for i in range(2000):
            if(i >= current_len):
                QAOA4[i]+=float(row[current_len-1])
            else:
                QAOA4[i]+=float(row[i])
    QAOA4 = [x/count for x in QAOA4]


plt.rcParams.update({
    'font.size': 16,
    'legend.fontsize': 12,    
    'xtick.labelsize':12,
    'ytick.labelsize':12,
})
font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc")

plt.figure(figsize=(8, 5))


plt.plot(QAOA1,label = r'$\text{QAOA}^6$')
plt.plot(QAOA2,label = r'$\text{variational-}\lambda \text{ QAOA}^6$')
plt.plot(QAOA3,label = r'$\text{variational-}\lambda \text{s QAOA}^6$')
plt.plot(QAOA4,label = r'$\text{additional-RX QAOA}^6$')

plt.legend(loc='lower right')
plt.ylabel('测量到最优解的概率',fontproperties=font)
plt.xlabel('线路运行次数',fontproperties=font)

plt.tight_layout()
plt.savefig('results/MIS/optimization_pocedure/MIS_optimization_pocedure.pdf')
# plt.show()