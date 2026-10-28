# RELATÓRIO DE VALIDAÇÃO EXPERIMENTAL — AULA 11
## CALCULO DE INCIDENTES - MOTOR FUZZY

**Data de execução:** 21/10/2026  
**Alunos:** Gabriel Orides - 106541 | Davi Kazussuke - 90613  

---

- PARTE 1 - CRONOGRAMA PROJETO TECH
- PARTE 2 - Explicação e Demo aula
- PARTE 3 - CONSTRUÇÃO E ENTREGA DA AC3 - ETAPA 3(FINAL) - VALOR DE 0,5 PONTO


## 1. ETAPA 1 — TESTES DO MOTOR FUZZY DE INCIDENTES (`test_fuzzy_engine.py`)

### Rodada 1 — Execução Sem Erros (Inicial)

**Comandos executados:**
```bash
pytest -v AULA_11/test_fuzzy_engine.py
pytest -s AULA_11/test_fuzzy_engine.py
```

**Resultado do Console:**
```text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items                                                              

AULA_11/test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED       [ 25%]
AULA_11/test_fuzzy_engine.py::test_monotonicidade_impacto PASSED         [ 50%]
AULA_11/test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED [ 75%]
AULA_11/test_fuzzy_engine.py::test_latencia_inferencia PASSED            [100%]

============================== 4 passed in 2.48s ===============================

============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items                                                              

AULA_11/test_fuzzy_engine.py ...
Tempo médio por inferência: 3.657 ms
.

============================== 4 passed in 1.75s ===============================
```

---

### Rodada 2 — Execução Com Erros Induzidos

**Alteração realizada:** Ajustado o limite da asserção de latência em `test_fuzzy_engine.py` para `assert tempo_medio_ms < 0.0001` a fim de induzir uma falha de desempenho na suíte de testes.

**Comando executado:**
```bash
pytest -v AULA_11/test_fuzzy_engine.py
```

**Resultado do Console:**
```text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items                                                              

AULA_11/test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED       [ 25%]
AULA_11/test_fuzzy_engine.py::test_monotonicidade_impacto PASSED         [ 50%]
AULA_11/test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED [ 75%]
AULA_11/test_fuzzy_engine.py::test_latencia_inferencia FAILED            [100%]

=================================== FAILURES ===================================
___________________________ test_latencia_inferencia ___________________________

simulador = <skfuzzy.control.controlsystem.ControlSystemSimulation object at 0x7a3883636060>

    def test_latencia_inferencia(simulador):
        inicio = time.time()
        for _ in range(100):
            imp = np.random.uniform(0, 100)
            exp = np.random.uniform(0, 10)
            executar_inferencia(simulador, imp, exp)
        tempo_total = time.time() - inicio
        tempo_medio_ms = (tempo_total / 100) * 1000
        print(f"\nTempo médio por inferência: {tempo_medio_ms:.3f} ms")
>       assert tempo_medio_ms < 0.0001
E       assert 3.748948574066162 < 0.0001

AULA_11/test_fuzzy_engine.py:51: AssertionError
----------------------------- Captured stdout call -----------------------------

Tempo médio por inferência: 3.749 ms
=========================== short test summary info ============================
FAILED AULA_11/test_fuzzy_engine.py::test_latencia_inferencia - assert 3.748948574066162 < 0.0001
========================= 1 failed, 3 passed in 1.95s ==========================
```

---

### Rodada 3 — Execução Corrigida (Final)

**Alteração realizada:** Revertida a asserção de latência para o SLA funcional correto (`assert tempo_medio_ms < 10.0`).

**Comandos executados:**
```bash
pytest -v AULA_11/test_fuzzy_engine.py
pytest -s AULA_11/test_fuzzy_engine.py
```

**Resultado do Console:**
```text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items                                                              

AULA_11/test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED       [ 25%]
AULA_11/test_fuzzy_engine.py::test_monotonicidade_impacto PASSED         [ 50%]
AULA_11/test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED [ 75%]
AULA_11/test_fuzzy_engine.py::test_latencia_inferencia PASSED            [100%]

============================== 4 passed in 2.57s ===============================

============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 4 items                                                              

AULA_11/test_fuzzy_engine.py ...
Tempo médio por inferência: 4.510 ms
.

============================== 4 passed in 1.83s ===============================
```

---

## 2. ETAPA 2 — SISTEMA DE TRIAGEM MÉDICA DE UTI (`test_uti_triagem.py`)

**Comandos executados:**
```bash
pytest -v AULA_11/test_uti_triagem.py
pytest -s AULA_11/test_uti_triagem.py
```

**Resultado do Console:**
```text
============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 3 items                                                              

AULA_11/test_uti_triagem.py::test_paciente_saudavel_baixo_risco PASSED   [ 33%]
AULA_11/test_uti_triagem.py::test_salto_nao_linear_queda_spo2 PASSED     [ 66%]
AULA_11/test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED  [100%]

============================== 3 passed in 1.38s ===============================

============================= test session starts ==============================
platform linux -- Python 3.13.18, pytest-8.4.2, pluggy-1.7.0
rootdir: /content
plugins: platformdirs-4.13.5, anyio-4.15.1, typeguard-4.6.0, langsmith-0.14.12
collected 3 items                                                              

AULA_11/test_uti_triagem.py ...

============================== 3 passed in 1.40s ===============================
```