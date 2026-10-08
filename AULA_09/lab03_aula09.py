"""
Etapa 1: Definição do problema
Problema escolhido: Saúde e bem-estar - Intensidade ideal de treino a partir de sono e frequência cardíaca de repouso[cite: 3].
O sistema possui duas entradas numéricas e uma saída numérica e utiliza variáveis descritas com termos vagos para uma decisão não trivial[cite: 3].
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ---------- Etapa 2: Modelagem ----------
# Universos de discurso
sono = ctrl.Antecedent(np.arange(0, 12.1, 0.5), "sono")               # horas de sono
fc_repouso = ctrl.Antecedent(np.arange(40, 101, 1), "fc_repouso")     # batimentos por minuto
intensidade = ctrl.Consequent(np.arange(0, 101, 1), "intensidade")    # % de intensidade do treino

# Conjuntos fuzzy (funções de pertinência)
sono["ruim"] = fuzz.trimf(sono.universe, [0, 0, 6])
sono["medio"] = fuzz.trimf(sono.universe, [4, 7, 9])
sono["bom"] = fuzz.trimf(sono.universe, [7, 12, 12])

fc_repouso["baixa"] = fuzz.trimf(fc_repouso.universe, [40, 40, 60])
fc_repouso["media"] = fuzz.trimf(fc_repouso.universe, [50, 70, 85])
fc_repouso["alta"] = fuzz.trimf(fc_repouso.universe, [75, 100, 100])

intensidade["leve"] = fuzz.trimf(intensidade.universe, [0, 0, 50])
intensidade["moderado"] = fuzz.trimf(intensidade.universe, [30, 60, 90])
intensidade["intenso"] = fuzz.trimf(intensidade.universe, [70, 100, 100])

# Base de regras (mínimo de 6 regras, usando E e OU ao menos uma vez cada)[cite: 3]
regras = [
    ctrl.Rule(sono["ruim"] | fc_repouso["alta"], intensidade["leve"]),
    ctrl.Rule(sono["ruim"] & fc_repouso["baixa"], intensidade["moderado"]),
    ctrl.Rule(sono["medio"] & fc_repouso["media"], intensidade["moderado"]),
    ctrl.Rule(sono["medio"] & fc_repouso["baixa"], intensidade["intenso"]),
    ctrl.Rule(sono["bom"] & (fc_repouso["baixa"] | fc_repouso["media"]), intensidade["intenso"]),
    ctrl.Rule(sono["bom"] & fc_repouso["alta"], intensidade["moderado"])
]

# ---------- Etapa 3: Implementação ----------
sistema = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema)

# ---------- Etapa 4: Testes ----------
# Teste com no mínimo 4 situações[cite: 3]
cenarios = [
    {"sono": 3, "fc_repouso": 90, "esperado": "Leve"},
    {"sono": 7, "fc_repouso": 65, "esperado": "Moderado"},
    {"sono": 9, "fc_repouso": 45, "esperado": "Intenso"},
    {"sono": 8, "fc_repouso": 80, "esperado": "Moderado"}
]

print("=== RESULTADOS DA AVALIAÇÃO FUZZY ===")
for i, c in enumerate(cenarios, 1):
    simulador.input["sono"] = c["sono"]
    simulador.input["fc_repouso"] = c["fc_repouso"]
    simulador.compute()
    resultado = simulador.output["intensidade"]
    print(f"Teste {i}: Sono = {c['sono']}h | FC = {c['fc_repouso']} bpm")
    print(f" -> Saída do sistema: {resultado:.1f}% (Esperado: {c['esperado']})\n")

print("-" * 50)
print("EXPLICAÇÃO DOS RESULTADOS (O que a lógica fuzzy realiza):")
print("A lógica fuzzy modela e resolve esse problema permitindo avaliar graus de pertinência em vez de valores binários e absolutos[cite: 1, 3].")
print("Em vez de classificar a intensidade do treino com cortes exatos (ex: se sono > 6), ela utiliza conjuntos que se sobrepõem, resultando em uma transição matemática suave de decisões[cite: 1].")

# (Opcional) Visualização
# sono.view()
# fc_repouso.view()
# intensidade.view(sim=simulador)
# plt.show()
