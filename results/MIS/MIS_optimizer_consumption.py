import csv
import numpy as np


QAOA_rounds = []
QAOA_evaluations = []

variational_lambda_rounds = []
variational_lambda_evaluations = []

variational_lambdas_rounds = []
variational_lambdas_evaluations = []

additional_RX_rounds = []
additional_RX_evaluations = []

def readCSV(filename, rounds, evaluations):
    with open(filename) as f:
        csvreader = csv.reader(f, delimiter=',')

        for row in csvreader:
            rounds += [float(row[-1])]
            evaluations += [float(row[-2])]
        
readCSV('results/MIS/QAOA/original/MIS_QAOA8_0.4_5_original.csv', QAOA_rounds, QAOA_evaluations)
readCSV('results/MIS/QAOA/variational_lambda/MIS_QAOA8_0.4_5_variational_lambda.csv',variational_lambda_rounds, variational_lambda_evaluations)
readCSV('results/MIS/QAOA/variational_lambdas/MIS_QAOA8_0.4_5_variational_lambdas.csv', variational_lambdas_rounds, variational_lambdas_evaluations)
readCSV('results/MIS/QAOA/additional_RX/MIS_QAOA8_0.4_5_additional_RX.csv', additional_RX_rounds, additional_RX_evaluations)


print('evaluations:')
print('QAOA', np.average(QAOA_evaluations))
print('variational_lambda', np.average(variational_lambda_evaluations))
print('variational_lambdas', np.average(variational_lambdas_evaluations))
print('additional_RX', np.average(additional_RX_evaluations))

print('rounds:')
print('QAOA', np.average(QAOA_rounds))
print('variational_lambda', np.average(variational_lambda_rounds))
print('variational_lambdas', np.average(variational_lambdas_rounds))
print('additional_RX', np.average(additional_RX_rounds))