# RELATÓRIO DE RESULTADOS EXPERIMENTAIS — AULA 13
## OPERADORES EVOLUCIONÁRIOS E OTIMIZAÇÃO MULTIOBJETIVO

**Data de execução:** 18/11/2026 
**Alunos:** Gabriel Orides - 106541 | Davi Kazussuke - 90613

---

## 1. ETAPA 1 — VARIÁVEIS INTEIRAS NA OTIMIZAÇÃO DO SOC

### Exercício 1 — Fronteira de Pareto discreta

**Objetivo:** Configurar o NSGA-II para dimensionar Pods e analistas de nível 2 utilizando apenas valores inteiros.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 30.
- Número de gerações: 40.
- Semente aleatória: 42.
- Variáveis de decisão:
  - Pods: de 1 a 30.
  - Analistas de nível 2: de 1 a 15.
- Operadores:
  - `IntegerRandomSampling` para gerar soluções inteiras.
  - `SBX` com `eta=15` e `RoundingRepair`.
  - `PM` com probabilidade 0.2, `eta=20` e `RoundingRepair`.
- Objetivos: minimizar latência e custo por hora.

**Resultado da execução:**

```text
Amostra de 5 solucoes inteiras encontradas (Pods, Analistas):
Pods: 30 | Analistas: 15 => Latencia: 23.33 ms | Custo: R$ 1215.00
Pods:  1 | Analistas:  1 => Latencia: 550.00 ms | Custo: R$ 63.00
Pods:  2 | Analistas:  1 => Latencia: 350.00 ms | Custo: R$ 81.00
Pods:  3 | Analistas:  1 => Latencia: 283.33 ms | Custo: R$ 99.00
Pods:  4 | Analistas:  1 => Latencia: 250.00 ms | Custo: R$ 117.00
```

**Análise:**  
O uso de `vtype=int`, `IntegerRandomSampling` e `RoundingRepair` manteve Pods e analistas como quantidades discretas. Sem a amostragem inteira e o reparo, operadores projetados para valores reais poderiam produzir frações de servidores ou analistas, como 2.7 Pods, que não representam uma escala operacional válida. A solução com 30 Pods e 15 analistas apresentou a menor latência da amostra, enquanto a configuração com 1 Pod e 1 analista apresentou o menor custo.

---

## 2. ETAPA 2 — DIMENSIONAMENTO INTEIRO DE CLUSTER KUBERNETES

### Exercício 2 — Tempo de resposta e custo mensal

**Objetivo:** Aplicar operadores inteiros ao dimensionamento de réplicas da API e worker nodes.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 25.
- Número de gerações: 35.
- Semente aleatória: 10.
- Variáveis de decisão:
  - Réplicas da API: de 2 a 40.
  - Worker nodes: de 1 a 12.
- Operadores inteiros: `IntegerRandomSampling`, `SBX` com `RoundingRepair` e `PM` com `RoundingRepair`.
- Objetivos: minimizar tempo de resposta e custo mensal.

**Resultado da execução:**

```text
Amostra de 5 solucoes encontradas (Replicas, Nodes):
Replicas:  2 | Nodes:  1 => Tempo: 500.00 ms | Custo: USD 109.00
Replicas: 40 | Nodes: 12 => Tempo: 31.67 ms | Custo: USD 1500.00
Replicas:  3 | Nodes:  1 => Tempo: 400.00 ms | Custo: USD 121.00
Replicas:  4 | Nodes:  1 => Tempo: 350.00 ms | Custo: USD 133.00
Replicas: 33 | Nodes:  8 => Tempo: 43.18 ms | Custo: USD 1076.00
```

**Análise:**  
As soluções mostram o compromisso entre capacidade e custo: aumentar réplicas e nós reduz o tempo de resposta, mas eleva o gasto mensal. Foram utilizados apenas números inteiros para representar recursos físicos e dimensionamento de infraestrutura.

---

## 3. ETAPA 3 — EXPLORAÇÃO CONTRA EXPLOTAÇÃO DOS OPERADORES

### Exercício 3 — Configuração A versus Configuração B

**Objetivo:** Comparar duas configurações do NSGA-II com comportamentos distintos de exploração e convergência.

**Configuração utilizada:**
- Problema com duas variáveis contínuas e dois objetivos.
- População: 30.
- Gerações: 20.
- Semente aleatória: 42.

| Configuração | SBX | PM | Comportamento |
|---|---|---|---|
| A — Exploração | `prob=0.9`, `eta=5` | `prob=0.5`, `eta=5` | Alta mutação e filhos mais distantes dos pais |
| B — Explotação | `prob=0.9`, `eta=30` | `prob=0.05`, `eta=30` | Baixa mutação e refinamento próximo aos pais |

**Resultado da execução:**  
Foi gerado o gráfico **“Exercicio 3 - Efeito dos Parametros SBX/PM em 20 Geracoes”**, comparando as fronteiras obtidas pelas Configurações A e B. A Configuração A foi representada pela cor laranja, enquanto a Configuração B foi representada por marcadores azuis em forma de X.

**Análise:**  
Valores baixos de `eta` produzem filhos mais afastados dos pais e favorecem a exploração do espaço de busca. Valores altos de `eta` e menor probabilidade de mutação favorecem a manutenção e o refinamento das boas regiões já encontradas, caracterizando maior explotação.

---

## 4. ETAPA 4 — QUALIDADE DA FRONTEIRA PELO HIPERVOLUME

### Exercício 4 — Comparação entre 10 e 80 gerações

**Objetivo:** Avaliar numericamente a convergência do NSGA-II para o problema de consumo da bateria e perda de pacotes de uma rede de sensores.

**Configuração utilizada:**
- População: 40.
- Semente aleatória: 42.
- Configurações comparadas:
  - 10 gerações.
  - 80 gerações.
- Ponto de referência do Hipervolume: `(400.0, 600.0)`.
- Objetivos: minimizar consumo da bateria e perda de pacotes.

**Resultado da execução:**

```text
Hipervolume (10 geracoes): 226626.7047731528
Hipervolume (80 geracoes): 226715.93778257925
```

**Análise:**  
O Hipervolume foi maior com 80 gerações, indicando uma frente de Pareto com melhor cobertura do espaço de objetivos. A diferença foi de aproximadamente `89.2330` unidades de Hipervolume:

```text
226715.93778257925 - 226626.7047731528 = 89.23300942645
```

Embora o ganho seja relativamente pequeno em relação ao total calculado, ele demonstra que o aumento do número de gerações produziu uma pequena melhora na qualidade da fronteira. Em geral, quanto maior o Hipervolume em relação ao ponto de referência, melhor a cobertura e a convergência da solução.

---

## 5. ETAPA 5 — SELEÇÃO AUTOMÁTICA COM PSEUDOPESOS

### Exercício 5 — Configuração recomendada de banco de dados na nuvem

**Objetivo:** Converter a fronteira de Pareto em uma única recomendação prática usando pesos de negócio.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 40.
- Número de gerações: 50.
- Semente aleatória: 42.
- Variáveis: RAM de 4 a 128 GB e IOPS de 100 a 5000.
- Objetivos: minimizar custo por hora e tempo de consulta.
- Pesos MCDM:
  - 30% custo.
  - 70% desempenho da consulta.

**Resultado da execução:**

```text
Decisao Recomendada (Pesos 30% Custo / 70% Performance):
-> Configuracao: 76.6 GB RAM | 2755 IOPS
-> Resultado: US$ 56.52/h | Tempo de Query: 8.06 ms
```

**Análise:**  
A solução escolhida prioriza fortemente o desempenho da consulta, mas ainda considera o custo. Com 76.6 GB de RAM e 2755 IOPS, o modelo recomenda um banco com custo de US$ 56.52 por hora e tempo de consulta de 8.06 ms.

---

## 6. ETAPA 6 — OTIMIZAÇÃO INTEGRADA DE ESCALA HOSPITALAR

### Exercício 6 — Pipeline completo com restrição e MCDM

**Objetivo:** Integrar variáveis inteiras, restrição de espera e PseudoWeights para recomendar uma escala hospitalar.

**Configuração utilizada:**
- População: 40.
- Gerações: 50.
- Semente aleatória: 42.
- Variáveis de decisão:
  - Médicos plantonistas: de 2 a 20.
  - Enfermeiros: de 4 a 40.
- Objetivos:
  - Minimizar custo do plantão.
  - Minimizar tempo médio de espera.
- Restrição:
  - `g1 = tempo de espera - 25 <= 0`.
- Pesos MCDM:
  - 40% custo.
  - 60% tempo de espera.
- Operadores inteiros: `IntegerRandomSampling`, `SBX` com `RoundingRepair` e `PM` com `RoundingRepair`.

**Resultado da execução:**

```text
Escala Recomendada (MCDM - 40% Custo, 60% Espera):
-> 17 Medicos | 32 Enfermeiros
-> Custo: R$ 34800.00 | Tempo Espera: 18.09 min
```

**Análise:**  
A solução recomendada respeita a restrição hospitalar porque o tempo de espera de 18.09 minutos é inferior ao limite máximo de 25 minutos. Ela utiliza 17 médicos plantonistas e 32 enfermeiros, resultando em custo de R$ 34.800 por plantão.

A escala foi escolhida dando maior peso ao tempo de espera, mas sem ignorar o custo. Portanto, ela representa um compromisso prático para manter o atendimento dentro do SLA de 25 minutos.

---

## 7. CONCLUSÃO DA AULA

Os exercícios desta aula demonstraram que o NSGA-II pode ser aplicado a problemas contínuos e discretos. Para variáveis inteiras, `IntegerRandomSampling` e `RoundingRepair` evitaram que a otimização produza valores de infraestrutura que não possam ser implantados.

O Hipervolume mostrou, numericamente, que 80 gerações produziram uma pequena melhoria em relação à execução com 10 gerações. Por fim, a combinação de restrições e PseudoWeights permitiu transformar soluções multidimensionais em recomendações objetivas de operação. No caso hospitalar, a escala recomendada foi de 17 médicos e 32 enfermeiros, com custo de R$ 34.800 e tempo de espera de 18.09 minutos.
