import pytest
from src.uti_triagem import criar_sistema_triagem_uti, avaliar_paciente

@pytest.fixture
def simulador_uti():
    return criar_sistema_triagem_uti()

def test_paciente_saudavel_baixo_risco(simulador_uti):
    risco = avaliar_paciente(simulador_uti, 75, 98)
    assert risco < 30.0, f"Risco esperado < 30.0%, obtido: {risco:.2f}%"

def test_salto_nao_linear_queda_spo2(simulador_uti):
    risco_normal = avaliar_paciente(simulador_uti, 75, 95)
    risco_queda = avaliar_paciente(simulador_uti, 75, 89)

    assert risco_normal < 38.0, f"Risco SpO2 95% esperado < 38.0%, obtido: {risco_normal:.2f}%"
    assert risco_queda > 65.0, f"Risco SpO2 89% esperado > 65.0%, obtido: {risco_queda:.2f}%"
    assert risco_queda > risco_normal, "O risco deve aumentar com a queda do SpO2"

def test_validacao_limites_fisiologicos(simulador_uti):
    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 35, 95)

    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 75, 105)
