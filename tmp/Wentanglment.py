from pyqpanda import *
import numpy as np
from scipy.optimize import minimize

def question1(n_qubits_):
    '''
    :rtype: Dict[str:float]
    '''
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n_qubits_)
    cbits = qvm.cAlloc_many(1)
    result = {}

    x0 = np.random.rand(n_qubits_-2)
    
    def fun(para):

        prog = QProg()

        prog << RY(qubits[0], para[0])
        for i in range(n_qubits_-3):
            prog << RY(qubits[i+1], para[i+1]).control(qubits[i])

        prog << H(qubits[n_qubits_-2]).control(qubits[n_qubits_-3])
        for i in range(n_qubits_-1):
            prog << CNOT(qubits[n_qubits_-2-i],qubits[n_qubits_-1-i])

        prog << X(qubits[0])

        #print(prog)
        prob = qvm.prob_run_dict(prog, qubits, -1)
        #print(prob)
        prob = list(prob.values())

        tar = 1/n_qubits_
        loss = 0
        j = 1
        for i in range(2 ** n_qubits_):
            if i == j:
                loss += abs(prob[i] - tar)
                j *= 2
            else:
                loss += prob[i]
        return loss
    
    res = minimize(fun,x0,method='COBYLA')
    para = res.x

    prog = QProg()
    prog << RY(qubits[0], para[0])
    for i in range(n_qubits_-3):
        prog << RY(qubits[i+1], para[i+1]).control(qubits[i])
    prog << H(qubits[n_qubits_-2]).control(qubits[n_qubits_-3])
    for i in range(n_qubits_-1):
        prog << CNOT(qubits[n_qubits_-2-i],qubits[n_qubits_-1-i])
    prog << X(qubits[0])

    prob = qvm.prob_run_dict(prog, qubits, -1)
    #print(prob)
    filtered_dict = {key: value for key, value in prob.items() if key.count('1') == 1}
    print(filtered_dict)

    return filtered_dict



if __name__ == '__main__':
    question1(4)
