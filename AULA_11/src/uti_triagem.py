import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def criar_sistema_triagem_uti():
    # 1. Variáveis
    freq_cardiaca = ctrl.Antecedent(np.arange(40, 161, 1), 'freq_cardiaca')
    spo2 = ctrl.Antecedent(np.arange(70, 101, 1), 'spo2')
    risco = ctrl.Consequent(np.arange(0, 101, 1), 'risco')

    risco.defuzzify_method = 'centroid'

    # 2. Funções de Pertinência
    freq_cardiaca['bradicardia'] = fuzz.trimf(freq_cardiaca.universe, [40, 40, 60])
    freq_cardiaca['normal']      = fuzz.trimf(freq_cardiaca.universe, [50, 75, 100])
    freq_cardiaca['taquicardia']  = fuzz.trapmf(freq_cardiaca.universe, [90, 110, 160, 160])

    spo2['critica']   = fuzz.trapmf(spo2.universe, [70, 70, 88, 91])
    spo2['limitrofe'] = fuzz.trimf(spo2.universe, [89, 93, 96])
    spo2['normal']    = fuzz.trapmf(spo2.universe, [94, 97, 100, 100])

    risco['baixo']    = fuzz.trimf(risco.universe, [0, 0, 35])
    risco['moderado'] = fuzz.trimf(risco.universe, [25, 50, 75])
    risco['critico']  = fuzz.trapmf(risco.universe, [65, 85, 100, 100])

    # 3. Regras Clínicas
    r1 = ctrl.Rule(spo2['critica'], risco['critico'])
    r2 = ctrl.Rule(freq_cardiaca['bradicardia'] & spo2['limitrofe'], risco['critico'])
    r3 = ctrl.Rule(freq_cardiaca['taquicardia'] & spo2['limitrofe'], risco['critico'])
    r4 = ctrl.Rule(freq_cardiaca['normal'] & spo2['limitrofe'], risco['moderado'])
    r5 = ctrl.Rule(freq_cardiaca['normal'] & spo2['normal'], risco['baixo'])

    uti_ctrl = ctrl.ControlSystem([r1, r2, r3, r4, r5])
    return ctrl.ControlSystemSimulation(uti_ctrl)

def avaliar_paciente(simulador, bpm, spo2_val):
    if not (40 <= bpm <= 160):
        raise ValueError(f"Frequência cardíaca fora do intervalo fisiológico [40, 160]: {bpm}")
    if not (70 <= spo2_val <= 100):
        raise ValueError(f"Saturação de Oxigénio SpO2 fora do intervalo [70, 100]: {spo2_val}")

    simulador.input['freq_cardiaca'] = bpm
    simulador.input['spo2'] = spo2_val
    simulador.compute()
    return simulador.output['risco']

if __name__ == "__main__":
    sim = criar_sistema_triagem_uti()
    print("Sistema de UTI instanciado com sucesso!")
