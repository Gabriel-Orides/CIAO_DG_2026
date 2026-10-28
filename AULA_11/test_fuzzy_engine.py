import time
import pytest
import numpy as np
from src.engine import construir_motor_inferencia

@pytest.fixture
def simulador():
    return construir_motor_inferencia()

def executar_inferencia(simulador, impacto, explorabilidade):
    if not (0 <= impacto <= 100):
        raise ValueError(f"Impacto fora da escala [0, 100]: {impacto}")
    if not (0 <= explorabilidade <= 10):
        raise ValueError(f"Explorabilidade fora da escala [0, 10]: {explorabilidade}")

    simulador.input['impacto'] = impacto
    simulador.input['explorabilidade'] = explorabilidade
    simulador.compute()
    return simulador.output['urgencia']

def test_saida_dentro_do_universo(simulador):
    casos = [(0, 0), (50, 5), (100, 10), (30, 8), (80, 2)]
    for imp, exp in casos:
        res = executar_inferencia(simulador, imp, exp)
        assert 0.0 <= res <= 100.0, f"Falha: Saída {res} fora de [0, 100]"

def test_monotonicidade_impacto(simulador):
    exp_fixa = 5.0
    urg_baixa = executar_inferencia(simulador, 20.0, exp_fixa)
    urg_media = executar_inferencia(simulador, 50.0, exp_fixa)
    urg_alta = executar_inferencia(simulador, 90.0, exp_fixa)
    assert urg_baixa <= urg_media <= urg_alta

def test_entradas_invalidas_disparam_erro(simulador):
    with pytest.raises(ValueError):
        executar_inferencia(simulador, -10.0, 5.0)
    with pytest.raises(ValueError):
        executar_inferencia(simulador, 150.0, 5.0)
    with pytest.raises(ValueError):
        executar_inferencia(simulador, 50.0, 12.0)

def test_latencia_inferencia(simulador):
    inicio = time.time()
    for _ in range(100):
        imp = np.random.uniform(0, 100)
        exp = np.random.uniform(0, 10)
        executar_inferencia(simulador, imp, exp)
    tempo_total = time.time() - inicio
    tempo_medio_ms = (tempo_total / 100) * 1000
    print(f"\nTempo médio por inferência: {tempo_medio_ms:.3f} ms")
    assert tempo_medio_ms < 10.0
