from pyqpanda import *
import numpy as np
from scipy.optimize import minimize

def question1(n_qubits):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n_qubits)
    cbits = qvm.cAlloc_many(1)
    result = {}

    x0 = np.random.rand(n_qubits-2)
    
    def fun(para):
        prog = QProg()

        prog << RY(qubits[0], para[0])
        for i in range(n_qubits-3):
            prog << RY(qubits[i+1], para[i+1]).control(qubits[i])

        prog << H(qubits[n_qubits-2]).control(qubits[n_qubits-3])
        for i in range(n_qubits-1):
            prog << CNOT(qubits[n_qubits-2-i],qubits[n_qubits-1-i])

        prog << X(qubits[0])

        prob = qvm.prob_run_dict(prog, qubits, -1)
        prob = list(prob.values())

        tar = 1/n_qubits
        loss = 0
        j = 1
        for i in range(2 ** n_qubits):
            if i == j:
                loss += abs(prob[i] - tar) ** 2
                j *= 2
            else:
                loss += prob[i] ** 2
        return loss
    
    res = minimize(fun,x0,method='COBYLA')
    para = res.x

    prog = QProg()
    prog << RY(qubits[0], para[0])
    for i in range(n_qubits-3):
        prog << RY(qubits[i+1], para[i+1]).control(qubits[i])
    prog << H(qubits[n_qubits-2]).control(qubits[n_qubits-3])
    for i in range(n_qubits-1):
        prog << CNOT(qubits[n_qubits-2-i],qubits[n_qubits-1-i])
    prog << X(qubits[0])

    print(prog)

    prob = qvm.prob_run_dict(prog, qubits, -1)
    result = {key: value for key, value in prob.items() if key.count('1') == 1}

    print(result)
    return result


def question2(n_qubits):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n_qubits)
    cbits = qvm.cAlloc_many(1)
    result = {}



    return result

if __name__ == '__main__':
    question1(5)
