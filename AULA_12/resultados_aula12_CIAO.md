# RELATÓRIO DE RESULTADOS EXPERIMENTAIS — AULA 12
## OTIMIZAÇÃO MULTIOBJETIVO COM ALGORITMO NSGA-II

**Data de execução:** Não informada no notebook  
**Alunos:** Gabriel Orides - 106541 | Davi Kazussuke - 90613

---

## 1. ETAPA 1 — OTIMIZAÇÃO DE RECURSOS EM CLOUD

### Exercício 1 — Fronteira de Pareto: Cloud

**Objetivo:** Encontrar soluções que equilibrem o custo de infraestrutura e a latência de processamento.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 20.
- Número de gerações: 30.
- Semente aleatória: 1.
- Variável de decisão: quantidade de vCPUs, limitada entre 1 e 32.
- Objetivos: minimizar custo e latência.

**Funções utilizadas:**
- Custo: `vCPUs * 15`, considerando R$ 15 por vCPU.
- Latência: `300 / vCPUs`, diminuindo conforme a quantidade de vCPUs aumenta.

**Resultado da execução:**

O notebook apresentou o gráfico **“Exercício 1 — Fronteira de Pareto: Cloud”**, com custo no eixo X e latência no eixo Y. Não foi exibida uma lista numérica das soluções no console.

**Análise:**

O gráfico representa o equilíbrio entre o custo e o desempenho da infraestrutura. Aumentar a quantidade de vCPUs eleva o custo, mas reduz a latência. Portanto, não existe uma única solução que seja melhor em todos os aspectos: a escolha depende do quanto se deseja investir para obter uma resposta mais rápida.

---

## 2. ETAPA 2 — ALOCAÇÃO DE RECURSOS PARA UM SOC

### Exercício 2 — Custo e Tempo de Resposta

**Objetivo:** Avaliar diferentes combinações de analistas e recursos de segurança para minimizar o custo e o tempo de resposta de um SOC.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 30.
- Número de gerações: 40.
- Semente aleatória: 42.
- Variáveis de decisão:
  - Analistas: de 1 a 50.
  - Regimentos de segurança: de 1 a 10.
- Objetivos: minimizar custo e tempo de resposta.

**Funções utilizadas:**
- Custo: `(analistas * 100) + (regimento * 50)`.
- Tempo de resposta: `(200 / analistas) + (50 / regimento)`.

**Comando de saída:**
```python
print("Soluções do Exercício 2 (Custo, Tempo):")
print(res2.F[:5])
```

**Resultado do console:**
```text
Soluções do Exercício 2 (Custo, Tempo):
[[5499.15144291    9.00078892]
 [ 150.09223137  249.82575583]
 [4566.67075111    9.92824149]
 [ 639.59112553   57.59677282]
 [2419.49997264   15.42802542]]
```

**Análise:**

As cinco soluções apresentadas mostram diferentes combinações de custo e tempo de resposta. As soluções com custo mais alto apresentam tempos menores, enquanto as alternativas mais econômicas possuem tempos de resposta maiores. O resultado demonstra o conflito entre investir em mais recursos e reduzir o tempo necessário para responder aos incidentes.

---

## 3. ETAPA 3 — OTIMIZAÇÃO DE OPERAÇÕES COM DRONES

### Exercício 3 — Fronteira de Pareto 3D

**Objetivo:** Avaliar o equilíbrio entre tempo de operação, custo e emissão de CO₂ em uma operação com drones.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 40.
- Número de gerações: 50.
- Semente aleatória: 42.
- Variáveis de decisão:
  - Velocidade: de 10 a 80.
  - Carga: de 1 a 5.
- Objetivos: minimizar tempo, custo e emissão de CO₂.

**Funções utilizadas:**
- Tempo: `1000 / velocidade`.
- Custo: `(velocidade ** 2) * 0.1 + (carga * 50)`.
- Emissão de CO₂: `(velocidade * 1.5) / carga`.

**Resultado da execução:**

Foi gerado o gráfico tridimensional **“Exercício 3 — Pareto 3D: Drones”**, com os eixos de tempo, custo e CO₂. O notebook não apresentou os valores das soluções no console.

**Análise:**

O gráfico permite visualizar as alternativas encontradas considerando três objetivos ao mesmo tempo. Aumentar a velocidade reduz o tempo de operação, mas também pode elevar o custo. A carga influencia tanto o custo quanto a emissão calculada. Assim, a solução mais adequada depende da prioridade da operação: rapidez, economia ou redução das emissões.

---

## 4. ETAPA 4 — OTIMIZAÇÃO DE CARTEIRA DE INVESTIMENTOS

### Exercício 4 — Risco versus Retorno

**Objetivo:** Comparar diferentes distribuições de investimento entre renda fixa e ações, buscando equilibrar retorno esperado e risco.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 40.
- Número de gerações: 50.
- Semente aleatória: 42.
- Variáveis de decisão:
  - Renda fixa: de 0% a 100%.
  - Ações: de 0% a 100%.
- Objetivos: maximizar o retorno esperado e minimizar o risco.

**Funções utilizadas:**
- Retorno esperado: `rf * 0.08 + acoes * 0.18`.
- Risco: `rf * 0.02 + acoes * 0.25`.

Para utilizar o algoritmo, o retorno foi multiplicado por -1, permitindo que o NSGA-II tratasse os dois objetivos como minimizações. No gráfico, o sinal foi revertido para apresentar o retorno real.

**Resultado da execução:**

Foi gerado o gráfico **“Exercício 4 — Risco vs Retorno (Portfólio)”**, com risco no eixo X e retorno esperado no eixo Y. Não foram impressos valores numéricos no console.

**Análise:**

O gráfico apresenta as alternativas de investimento encontradas pelo algoritmo. Ações possuem retorno esperado maior na função utilizada, mas também apresentam um risco maior. Já a renda fixa possui risco menor e retorno esperado mais baixo. O resultado demonstra o compromisso entre buscar maior retorno e controlar o risco da carteira.

---

## 5. ETAPA 5 — AJUSTE DE HIPERPARÂMETROS DE MACHINE LEARNING

### Exercício 5 — Erro versus Tempo de Inferência

**Objetivo:** Encontrar combinações de profundidade da árvore e quantidade de estimadores que equilibrem o erro do modelo e o tempo de inferência.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 30.
- Número de gerações: 40.
- Semente aleatória: 7.
- Variáveis de decisão:
  - Profundidade da árvore: de 1 a 30.
  - Número de estimadores: de 10 a 200.
- Objetivos: minimizar erro e latência.

**Funções utilizadas:**
- Erro: `0.5 / (depth * log10(n_trees))`.
- Latência: `(depth * 0.2) + (n_trees * 0.5)`.

**Resultado da execução:**

Foi gerado o gráfico **“Exercício 5 — Erro vs. Tempo de Inferência (ML)”**, relacionando o erro do modelo com o tempo de resposta. O notebook não imprimiu uma lista numérica das soluções.

**Análise:**

A função utilizada indica que o erro diminui com o aumento da profundidade e da quantidade de estimadores. Por outro lado, essas alterações elevam o tempo de inferência. O gráfico representa as alternativas de compromisso entre obter um modelo com menor erro e manter um tempo de resposta reduzido.

---

## 6. ETAPA 6 — OTIMIZAÇÃO DE RECARGA E DESGASTE DE BATERIA

### Exercício 6 — Soluções Viáveis para Baterias de Veículos Elétricos

**Objetivo:** Encontrar configurações de potência e temperatura que reduzam o tempo de recarga e o desgaste da bateria, respeitando o limite de desgaste definido.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 40.
- Número de gerações: 50.
- Semente aleatória: 42.
- Variáveis de decisão:
  - Potência: de 10 a 150.
  - Temperatura: de 15 a 45.
- Objetivos: minimizar tempo de recarga e desgaste da bateria.
- Restrição: desgaste da bateria menor ou igual a 1500.

**Funções utilizadas:**
- Tempo de recarga: `3000 / potencia`.
- Desgaste: `(potencia ** 1.5) * (temp / 20)`.
- Restrição: `desgaste - 1500 <= 0`.

**Resultado do console:**
```text
Exercício 6 - Soluções viáveis (Tempo de Recarga, Desgaste):
[[ 299.98604101   23.71885687]
 [  20.00000264 1377.84937661]
 [ 199.88258764   43.62184173]
 [ 225.49117934   36.43538683]
 [ 110.09457407  106.68366754]
 [  88.13888565  148.94052149]
 [ 279.75495309   26.7701596 ]
 [ 102.54342556  118.70305345]
 [  65.95756475  230.07386301]
 [  24.66962036 1005.77384402]
 [ 140.41598948   74.0670296 ]
 [  22.52647754 1152.67080786]
 [  31.22086641  706.4442845 ]
 [ 191.40494603   46.53884795]
 [  50.75745971  340.7951525 ]
 [ 128.18176165   84.93452626]
 [  34.65669197  604.96460205]
 [ 269.93237692   27.7890969 ]
 [  81.54010929  170.21114393]
 [  42.03613343  452.18073953]
 [  37.73751663  531.59937479]
 [ 240.11668469   33.12175313]
 [ 176.30568202   52.64409924]
 [  39.71511117  492.39341786]
 [  57.44964052  285.67406107]
 [  58.9169561   282.77232303]
 [  25.77986544  941.54751728]
 [  23.62471253 1073.24069007]
 [ 256.67884744   29.96843348]
 [ 153.25738777   64.95566518]
 [  74.06071412  193.36818462]
 [ 251.81585308   32.00336601]
 [  21.98986991 1195.1181535 ]
 [  35.68651718  578.1749346 ]
 [  71.21886072  205.05561698]
 [  44.93615189  409.12758673]
 [ 230.93209183   35.11721308]
 [  23.72666108 1066.34021103]
 [ 130.08409439   83.78212807]
 [  27.36858611  860.72713304]]
```

**Análise:**

O algoritmo retornou 40 soluções para o problema, considerando a restrição de desgaste. Os resultados mostram que tempos de recarga menores estão associados a valores maiores de desgaste. Por exemplo, uma solução apresenta tempo de aproximadamente 20 e desgaste de 1377,85, enquanto outra apresenta tempo próximo de 299,99 e desgaste de 23,72.

Isso demonstra que aumentar a potência pode acelerar a recarga, mas também elevar o desgaste da bateria. A restrição impede que sejam consideradas soluções acima do limite estabelecido de 1500.

---

## 7. ETAPA 7 — OTIMIZAÇÃO DE FROTA DE ROBÔS

### Exercício 7 — Fronteira de Pareto e Soluções de Trade-off

**Objetivo:** Otimizar o custo total e o tempo médio de uma frota de robôs, respeitando uma restrição de consumo de energia.

**Configuração utilizada:**
- Algoritmo: NSGA-II (`NSGA2`).
- Tamanho da população: 40.
- Número de gerações: 60.
- Semente aleatória: 42.
- Variáveis de decisão:
  - Tamanho da frota: de 5 a 50.
  - Velocidade: de 1 a 4.
- Objetivos: minimizar custo total e tempo médio.
- Restrição de energia: `frota * (velocidade ** 1.5) <= 120`.

**Funções utilizadas:**
- Custo total: `(frota * 25) + ((velocidade ** 2) * 8)`.
- Tempo médio: `(120 / frota) + (40 / velocidade)`.
- Restrição: `(frota * (velocidade ** 1.5)) - 120 <= 0`.

**Resultado do console:**
```text
--- Exercício 7: As 3 melhores soluções de trade-off ---
1. Menor Custo : Custo = 133.02 mil | Tempo = 63.95 min
2. Solução Intermediária: Custo = 243.41 mil | Tempo = 30.88 min
3. Menor Tempo : Custo = 530.30 mil | Tempo = 17.93 min
```

**Resultado gráfico:**

Foi gerado o gráfico **“Exercício 7 — Fronteira de Pareto (Frota de Robôs)”**, relacionando o custo total e o tempo médio das soluções encontradas.

**Análise:**

As três soluções destacam diferentes prioridades:
- **Menor custo:** custo de R$ 133,02 mil e tempo de 63,95 minutos.
- **Solução intermediária:** custo de R$ 243,41 mil e tempo de 30,88 minutos.
- **Menor tempo:** custo de R$ 530,30 mil e tempo de 17,93 minutos.

A solução de menor custo apresenta o maior tempo, enquanto a solução mais rápida exige um investimento maior. A alternativa intermediária representa um equilíbrio entre os dois objetivos. Todas as soluções apresentadas foram obtidas dentro da otimização que considera a restrição de energia.

---

## 8. CONCLUSÃO GERAL

Os sete exercícios utilizaram o algoritmo NSGA-II para resolver problemas de otimização multiobjetivo em diferentes cenários, como infraestrutura em cloud, segurança, drones, investimentos, machine learning, baterias de veículos elétricos e frotas de robôs.

Os resultados mostram que na maioria dos casos, melhorar um objetivo pode prejudicar outro. Reduzir a latência pode aumentar o custo, acelerar uma recarga pode elevar o desgaste da bateria e diminuir o tempo de uma operação pode exigir mais recursos.

A utilização das fronteiras de Pareto permite visualizar essas alternativas e escolher uma solução de acordo com as prioridades de cada situação. Nos exercícios com restrições, o algoritmo também considera os limites definidos para que as soluções respeitem as condições do problema.
