import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def construir_motor_inferencia():
    # 1. Definição das Variáveis e Universos de Discurso
    impacto = ctrl.Antecedent(np.arange(0, 101, 1), 'impacto')
    explorabilidade = ctrl.Antecedent(np.arange(0, 11, 1), 'explorabilidade')
    urgencia = ctrl.Consequent(np.arange(0, 101, 1), 'urgencia')

    # 2. Funções de Pertinência
    impacto['Baixo'] = fuzz.trimf(impacto.universe, [0, 0, 40])
    impacto['Médio'] = fuzz.trimf(impacto.universe, [20, 50, 80])
    impacto['Alto']  = fuzz.trimf(impacto.universe, [60, 100, 100])

    explorabilidade['Baixa']    = fuzz.trimf(explorabilidade.universe, [0, 0, 4])
    explorabilidade['Moderada'] = fuzz.trimf(explorabilidade.universe, [2, 5, 8])
    explorabilidade['Alta']     = fuzz.trimf(explorabilidade.universe, [6, 10, 10])

    urgencia['Urgência Baixa']   = fuzz.trimf(urgencia.universe, [0, 0, 33])
    urgencia['Urgência Média']   = fuzz.trimf(urgencia.universe, [15, 33, 66])
    urgencia['Urgência Alta']    = fuzz.trimf(urgencia.universe, [50, 66, 85])
    urgencia['Urgência Crítica'] = fuzz.trimf(urgencia.universe, [66, 100, 100])

    # 3. Base de Regras (3x3)
    rule1 = ctrl.Rule(impacto['Baixo'] & explorabilidade['Baixa'],    urgencia['Urgência Baixa'])
    rule2 = ctrl.Rule(impacto['Baixo'] & explorabilidade['Moderada'], urgencia['Urgência Baixa'])
    rule3 = ctrl.Rule(impacto['Baixo'] & explorabilidade['Alta'],     urgencia['Urgência Média'])

    rule4 = ctrl.Rule(impacto['Médio'] & explorabilidade['Baixa'],    urgencia['Urgência Média'])
    rule5 = ctrl.Rule(impacto['Médio'] & explorabilidade['Moderada'], urgencia['Urgência Alta'])
    rule6 = ctrl.Rule(impacto['Médio'] & explorabilidade['Alta'],     urgencia['Urgência Alta'])

    rule7 = ctrl.Rule(impacto['Alto']  & explorabilidade['Baixa'],    urgencia['Urgência Crítica'])
    rule8 = ctrl.Rule(impacto['Alto']  & explorabilidade['Moderada'], urgencia['Urgência Crítica'])
    rule9 = ctrl.Rule(impacto['Alto']  & explorabilidade['Alta'],     urgencia['Urgência Crítica'])

    # 4. Sistema de Controle
    urgencia_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    return ctrl.ControlSystemSimulation(urgencia_ctrl)
