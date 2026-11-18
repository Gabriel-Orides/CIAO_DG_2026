import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.optimize import minimize

class KubernetesClusterProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            xl=np.array([2, 1]),
            xu=np.array([40, 12]),
            vtype=int
        )

    def _evaluate(self, x, out, *args, **kwargs):
        replicas, nodes = x[0], x[1]
        
        # TODO 1 e 2 Resolvidos
        f1_tempo = (600.0 / replicas) + (200.0 / nodes)
        f2_custo = (replicas * 12.0) + (nodes * 85.0)

        out["F"] = [f1_tempo, f2_custo]

# TODO 3 Resolvido
algorithm = NSGA2(
    pop_size=25,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True
)

# TODO 4 Resolvido
res2 = minimize(KubernetesClusterProblem(), algorithm, termination=('n_gen', 35), seed=10)

print("Amostra de 5 solucoes encontradas (Replicas, Nodes):")
for sol_x, sol_f in zip(res2.X[:5], res2.F[:5]):
    print(f"Replicas: {sol_x[0]:2d} | Nodes: {sol_x[1]:2d} => Tempo: {sol_f[0]:6.2f}ms | Custo: USD {sol_f[1]:6.2f}")