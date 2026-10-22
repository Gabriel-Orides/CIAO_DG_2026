# RELATÓRIO FINAL — AULA 08
## OTIMIZAÇÃO DE SISTEMAS COMPUTACIONAIS E RESILIÊNCIA DE REDES

**Data de execução:** 30/09/2026
**Alunos:** Gabriel Orides - 106541 | Davi Kazussuke - 90613

---

## 1. Objetivo

Registrar as análises técnicas, gráficos/tabelas e outputs dos cenários solicitados para a avaliação AC-2. Os resultados a seguir foram obtidos executando os algoritmos de otimização em Python.

---

# LABORATÓRIO 01 — PSO PARA BALANCEAMENTO DINÂMICO DE CARGA EM DATACENTERS

## Objetivo
Encontrar o vetor de pesos contínuos W para redirecionamento dinâmico de tráfego, de forma a minimizar a temperatura média ponderada de 6 zonas de disponibilidade (AZs).

**Código:** `lab01_aula08.ipynb`

## Resultado

```text
RESULTADOS DO LAB 01 - PSO CONTÍNUO
==================================================
População: 10 partículas
Melhor Distribuição (W): [1.000e-04 9.995e-01 1.000e-04 1.000e-04 1.000e-04 1.000e-04]
Soma dos pesos (Validação): 1.0000
Fitness Final (Temp. Média): 5.83 °C
Temperaturas por AZ: [0.000e+00 3.498e+01 1.000e-02 0.000e+00 0.000e+00 1.000e-02] °C
--------------------------------------------------
População: 30 partículas
Melhor Distribuição (W): [1.000e-04 1.000e-04 1.000e-04 9.995e-01 1.000e-04 1.000e-04]
Soma dos pesos (Validação): 1.0000
Fitness Final (Temp. Média): 5.00 °C
Temperaturas por AZ: [0.000e+00 0.000e+00 1.000e-02 2.999e+01 0.000e+00 1.000e-02] °C
--------------------------------------------------
População: 50 partículas
Melhor Distribuição (W): [1.000e-04 1.000e-04 1.000e-04 9.995e-01 1.000e-04 1.000e-04]
Soma dos pesos (Validação): 1.0000
Fitness Final (Temp. Média): 5.00 °C
Temperaturas por AZ: [0.000e+00 0.000e+00 1.000e-02 2.999e+01 0.000e+00 1.000e-02] °C
--------------------------------------------------
```

## Análise técnica

1. **Evolução do fitness e validação da distribuição (W):**
   * O algoritmo garantiu com sucesso que a soma dos pesos fosse exatamente 1.0000 em todos os cenários, respeitando o operador de normalização exigido.
   * As populações com 30 e 50 partículas alcançaram um fitness ideal mais baixo de 5.00 °C, enquanto a de 10 partículas ficou presa num resultado de 5.83 °C. 
   * Isto demonstra que um número maior de partículas permitiu ao enxame escapar a mínimos locais e concentrar o tráfego de forma mais eficiente.

---

# LABORATÓRIO 02 — AG BINÁRIO COM REPARAÇÃO/PENALIDADE PARA SELEÇÃO DE MICROSSERVIÇOS

## Objetivo
Selecionar um subconjunto de 15 microsserviços para maximizar o Valor de Negócio acumulado, respeitando as restrições simultâneas de máximo de 16 GB de RAM e 8 cores de CPU.

**Código:** `lab02_aula08.ipynb`

## Resultado

```text
LAB 02 - ESTRATÉGIA A (Rígida)
Melhor Combinação: [0 0 1 0 1 0 1 1 0 0 1 0 1 1 0]
Fitness: 770.0
Média/Std finais: 399.20 / 318.43

LAB 02 - ESTRATÉGIA B (Proporcional)
Melhor Combinação: [1 1 1 1 1 1 1 1 1 1 1 0 1 1 1]
Fitness: 870.0
Média/Std finais: 852.40 / 22.52
```

## Análise técnica

1. **Qual das duas estratégias encontrou a melhor combinação final de microsserviços?**
   * A Estratégia B encontrou uma combinação superior, alcançando um fitness máximo de 870.0.
   * Em contraste, a Estratégia A estagnou num fitness de 770.0.

2. **Qual das duas estratégias preservou melhor a diversidade genética da população?**
   * A Estratégia A (Penalidade Rígida) apresentou uma média final muito baixa (399.20) e um desvio-padrão extremamente elevado (318.43). 
   * Isto ocorre porque indivíduos que ultrapassam os limites recebem o valor 0 abruptamente, criando um fosso que destrói material genético útil.
   * Em contrapartida, a Estratégia B reduziu o fitness de forma proporcional, resultando numa média final alta (852.40) e num desvio-padrão muito menor (22.52). 
   * Isto indica uma convergência e exploração genética muito mais estável, mantendo a diversidade sem aniquilar indivíduos ligeiramente acima da capacidade.

---

# LABORATÓRIO 03 — ACO PARA PROJETO DE TOPOLOGIA DE REDE DE BAIXA LATÊNCIA

## Objetivo
Conectar 10 switches de rede em uma topologia em árvore geradora que minimize a latência total acumulada entre pares críticos, incluindo verificação de ciclos.

**Código:** `lab03_aula08.ipynb`

## Resultado

```text
LAB 03 - ACO PARA TOPOLOGIA DE REDE
========================================
Latência Topologia Aleatória: 565.00
Latência Otimizada (ACO): 253.00
Ganho de Desempenho: 55.22%

Matriz de Adjacência Final (10x10):
[[0 1 0 0 1 0 0 0 0 0]
 [1 0 1 0 0 0 0 0 1 0]
 [0 1 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 1 0 0]
 [1 0 0 0 0 1 0 0 0 0]
 [0 0 0 0 1 0 0 0 0 0]
 [0 0 0 0 0 0 0 1 1 0]
 [0 0 0 1 0 0 1 0 0 1]
 [0 1 0 0 0 0 1 0 0 0]
 [0 0 0 0 0 0 0 1 0 0]]
```

## Análise técnica

1. **Ganho percentual e prevenção de ciclos:**
   * O algoritmo ACO reduziu a latência total da topologia de 565.00 para 253.00, o que representa um ganho de desempenho significativo de 55.22% em relação à abordagem aleatória.
   * A utilização da estrutura *Union-Find* funcionou corretamente, permitindo que a colónia de formigas construísse uma árvore de expansão livre de ciclos, facto comprovado pela matriz de adjacência validada gerada no *output* final.