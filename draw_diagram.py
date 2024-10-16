import csv

a = 0
MA = 0
b = 0
selectMA = 0
c = 0
standard = 0

with open('results/tmp.csv', newline='') as f:
    csvreader = csv.reader(f, delimiter=',')

    for row in csvreader:
        if  'MA_QAOA' in row[0]:
            MA += float(row[6])
            a += 1
        if 'select' in row[0]:
            selectMA += float(row[6])
            b += 1
        if 'standard' in row[0] and int(row[4]) == 1:
            standard += float(row[6])
            c += 1

# print(MA/a)
# print(b)
# print(selectMA/b)
# print(standard/c)