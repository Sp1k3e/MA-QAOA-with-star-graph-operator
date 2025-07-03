import csv
import matplotlib.pyplot as plt
import numpy as np

pi = np.pi
gammas = []
betas = []

# with open('results/parameters/star_graph/star_parameters.csv') as f:
with open('results/parameters/star_graph/test.csv') as f:
    reader = csv.reader(f)

    for row in reader:
        gammas += row[6:-int(row[1])]
        betas += row[-int(row[1]):]

print(len(gammas))
print(len(betas))

gammas = [float(x) for x in gammas]
betas = [float(x) for x in betas]

# print(gammas)
# print(betas)

for i in range(len(gammas)):
    if(gammas[i] > 3.15):
        gammas[i] = gammas[i] - 2 * np.pi
# print(gammas)

for i in range(len(betas)):
    if(betas[i] > 3.15):
        betas[i] = betas[i] - 2 * np.pi
# print(betas)

#! betas
x = range(len(betas))
y = betas
plt.figure(figsize=(10,4))
plt.plot(x, y, marker='o', markersize = 5, linewidth = 1)
# plt.title('Index vs Value')
plt.xlabel('Betas')
plt.xlim(left=0, right=len(betas)-1)

yticks = [-pi, -3*pi/4,-pi/2, -pi/4, 0, pi/4, pi/2, 3*pi/4, pi]
yticklabels = [r'$-\pi$',r'$-3\pi/4$',r'$\pi/2$', r'$-\pi/4$', '0', r'$\pi/4$', r'$\pi/2$',r'$3\pi/4$',r'$\pi$']
plt.yticks(yticks, yticklabels)

plt.grid(True)
plt.savefig(f'results/diagram/betas.eps', format = 'eps', dpi = 500)
plt.show()

#! gammas
x = range(len(gammas))
y = gammas
plt.figure(figsize=(10,4))
plt.plot(x, y, marker='o', markersize = 5, linewidth = 1)
# plt.title('Index vs Value')
plt.xlabel('Gammas')
plt.xlim(left=0, right=len(gammas)-1)

yticks = [-pi, -3*pi/4,-pi/2, -pi/4, 0, pi/4, pi/2, 3*pi/4, pi]
yticklabels = [r'$-\pi$',r'$-3\pi/4$',r'$-\pi/2$', r'$-\pi/4$', '0', r'$\pi/4$', r'$\pi/2$',r'$3\pi/4$',r'$\pi$']
plt.yticks(yticks, yticklabels)

plt.grid(True)
plt.savefig(f'results/diagram/gammas.eps', format = 'eps', dpi = 500)
plt.show()