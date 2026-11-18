import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.optimize import minimize
from pymoo.mcdm.pseudo_weights import PseudoWeights

class EscalaHospitalarProblem(ElementwiseProblem):
    def __init__(self):
        # TODO 1 Resolvido
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([2, 4]),
            xu=np.array([20, 40]),
            vtype=int
        )

    def _evaluate(self, x, out, *args, **kwargs):
        medicos, enfermeiros = x[0], x[1]

        f1_custo = (medicos * 1200.0) + (enfermeiros * 450.0)
        f2_espera = (180.0 / medicos) + (240.0 / enfermeiros)

        # TODO 2 Resolvido (G(x) <= 0)
        g1 = f2_espera - 25.0 

        out["F"] = [f1_custo, f2_espera]
        out["G"] = [g1]

# TODO 3 Resolvido
algorithm = NSGA2(
    pop_size=40,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15, vtype=float, repair=RoundingRepair()),
    mutation=PM(prob=0.2, eta=20, vtype=float, repair=RoundingRepair()),
    eliminate_duplicates=True
)

res6 = minimize(EscalaHospitalarProblem(), algorithm, termination=('n_gen', 50), seed=42)

# TODO 4 Resolvido
pesos = np.array([0.40, 0.60])
indice_escolhido = PseudoWeights(pesos).do(res6.F)

melhor_x = res6.X[indice_escolhido]
melhor_f = res6.F[indice_escolhido]

print("Escala Recomendada (MCDM - 40% Custo, 60% Espera):")
print(f"-> {melhor_x[0]} Medicos | {melhor_x[1]} Enfermeiros")
print(f"-> Custo: R$ {melhor_f[0]:.2f} | Tempo Espera: {melhor_f[1]:.2f} min")