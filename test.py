from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Sampler
from qiskit_aer.primitives import Sampler as AerSampler
 
# exact statevector simulation
sampler = Sampler()
 
# another option
sampler = AerSampler(backend_options={"method": "statevector"},
                        run_options={"shots": None, "seed": 42})
 
optimizer = COBYLA()
qaoa = QAOA(sampler, optimizer, reps=2)
 
# diagonal operator
qubit_op = SparsePauliOp.from_list([("ZIII", 1),("IZII", 1), ("IIIZ", 1), ("IIZI", 1)])
result = qaoa.compute_minimum_eigenvalue(qubit_op)
 
print(result.eigenvalue)