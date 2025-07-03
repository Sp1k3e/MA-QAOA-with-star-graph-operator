import csv

with open('results/optimizer_consumption/expressive1.csv') as f1, open("results/tmp_expressive1.csv") as f2:
    reader1 = csv.reader(f1)
    reader2 = csv.reader(f2)
    # print(type(reader1[0][3]))

    rows2 = list(reader2)

    with open("results/optimizer_consumption/expressive.csv", 'a', newline='') as fout:
        writer = csv.writer(fout)

        for row1 in reader1:
            # print(row1[6])
            if(float(row1[6]) > 0.99):
                writer.writerow(row1)
            seed = row1[5]
            type = row1[3]
            for row2 in rows2:
                if(row2[5] == seed and row2[3] == type):
                    if(row1[6] > row2[6]):
                        writer.writerow(row1)
                    else:
                        writer.writerow(row2)
                    f2.seek(0)
                    reader2 = csv.reader(f2)
                    break
