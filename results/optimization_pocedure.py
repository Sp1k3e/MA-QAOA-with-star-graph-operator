import csv
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.font_manager import FontProperties

n=10

QAOA3=[0 for _ in range(1000)]
QAOA5=[0 for _ in range(1000)]
MA_QAOA1=[0 for _ in range(1000)]
MA_QAOA2=[0 for _ in range(1000)]
star_MA_QAOA1=[0 for _ in range(1000)]

with open(f'./results/optimizer_consumption/optimization_pocedure/QAOA_{n}_3.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    count = 0
    for row in csvreader:
        count+=1
        current_len = int(len(row)/2)
        for i in range(1000):
            if(i >= current_len):
                QAOA3[i]+=float(row[2*current_len-1])
            else:
                QAOA3[i]+=float(row[2*i + 1])
    QAOA3 = [x/count for x in QAOA3]

with open(f'./results/optimizer_consumption/optimization_pocedure/QAOA_{n}_5.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    count = 0
    for row in csvreader:
        count+=1
        current_len = int(len(row)/2)
        for i in range(1000):
            if(i >= current_len):
                QAOA5[i]+=float(row[2*current_len-1])
            else:
                QAOA5[i]+=float(row[2*i + 1])
    QAOA5 = [x/count for x in QAOA5]

with open(f'./results/optimizer_consumption/optimization_pocedure/MA-QAOA_{n}_1.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    count = 0
    for row in csvreader:
        count+=1
        current_len = int(len(row)/2)
        for i in range(1000):
            if(i >= current_len):
                MA_QAOA1[i]+=float(row[2*current_len-1])
            else:
                MA_QAOA1[i]+=float(row[2*i + 1])
    MA_QAOA1 = [x/count for x in MA_QAOA1]

with open(f'./results/optimizer_consumption/optimization_pocedure/MA-QAOA_{n}_2.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    count = 0
    for row in csvreader:
        count+=1
        current_len = int(len(row)/2)
        for i in range(1000):
            if(i >= current_len):
                MA_QAOA2[i]+=float(row[2*current_len-1])
            else:
                MA_QAOA2[i]+=float(row[2*i + 1])
    MA_QAOA2 = [x/count for x in MA_QAOA2]

with open(f'./results/optimizer_consumption/optimization_pocedure/star-QAOA_{n}_1.csv') as f:
    csvreader = csv.reader(f, delimiter=',')

    count = 0
    for row in csvreader:
        count+=1
        current_len = int(len(row)/2)
        for i in range(1000):
            if(i >= current_len):
                star_MA_QAOA1[i]+=float(row[2*current_len-1])
            else:
                star_MA_QAOA1[i]+=float(row[2*i + 1])
    star_MA_QAOA1 = [x/count for x in star_MA_QAOA1]


plt.rcParams.update({
    'font.size': 16,
    'legend.fontsize': 12,    
    'xtick.labelsize':12,
    'ytick.labelsize':12,
})
font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc")

plt.figure(figsize=(8, 5))


plt.plot(QAOA3,label = r'$\text{QAOA}^3$')
plt.plot(QAOA5,label = r'$\text{QAOA}^5$')
plt.plot(MA_QAOA1,label = r'$\text{MA-QAOA}^1$')
plt.plot(MA_QAOA2,label = r'$\text{MA-QAOA}^2$')
plt.plot(star_MA_QAOA1,label=r'$\text{Star MA-QAOA}^1$')
hline = plt.axhline(y=0.878, color="#00000091", linestyle='--', linewidth = 1.5, label='GW',zorder=-1)

plt.legend(loc='lower right')
plt.ylabel('近似比',fontproperties=font)
plt.xlabel('线路运行次数',fontproperties=font)

plt.tight_layout()
plt.savefig(f'./results/optimizer_consumption/optimization_pocedure/optimization_pocedure_{n}.pdf')
# plt.show()