from pyqpanda import *
import numpy as np
from pyvqnet.qnn.template import BasicEntanglerTemplate
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

    x0 = np.random.rand(n_qubits_*3)
    
    def fun(para):
        '''
        weights = np.array(args).reshape(1, -1)
        circuit = BasicEntanglerTemplate(weights,n_qubits_)
        result = circuit.create_circuit(qubits)
        circuit.print_circuit(qubits)

        prob = qvm.prob_run_dict(result, qubits, -1)
        prob = list(prob.values())
        print(prob)
        '''
        prog = QProg()
        for i in range(n_qubits_):
            prog << RX(qubits[i], para[i]) << RY(qubits[i], para[i+1]) << RZ(qubits[i], para[i+2])
        for i in range(n_qubits_):
            prog << CNOT(qubits[i], qubits[(i+1)%n_qubits_])

        print(prog)
        prob = qvm.prob_run_dict(prog, qubits, -1)
        print(prob)
        prob = list(prob.values())

        tar = 1/3
        loss = 0
        j = 1
        for i in range(8):
            if i == j:
                loss += abs(prob[i] - tar)
                j *= 2
            else:
                loss += prob[i]
        return loss
    
    res = minimize(fun,x0,method='COBYLA')
    print(res.fun)

    '''
    weights = np.array(res.x).reshape(1, -1)
    circuit = BasicEntanglerTemplate(weights,n_qubits_)
    result = circuit.create_circuit(qubits)
    circuit.print_circuit(qubits)

    prob = qvm.prob_run_dict(result, qubits, -1)
    print(prob)
    '''

    #return result



if __name__ == '__main__':
    question1(3)
