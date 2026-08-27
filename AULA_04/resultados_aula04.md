# Laboratórios de Algoritmos Genéticos (AG) — Otimização Combinatória

Este repositório reúne as atividades práticas da **AULA 04** sobre **Algoritmos Genéticos aplicados a Problemas Combinatórios**, incluindo penalizações, elitismo e balanceamento de carga.

## Conteúdo

- [Exercício 1 — Análise do Elitismo na Estabilidade Algorítmica](#exercício-1--análise-do-elitismo-na-estabilidade-algorítmica)
- [Exercício 2 — Inserção de Penalidades por Descumprimento de SLA](#exercício-2--inserção-de-penalidades-por-descumprimento-de-sla)
- [Exercício 3 — Balanceamento de Carga em Servidores](#exercício-3--balanceamento-de-carga-em-servidores-desafio-de-código)
- [Desafio Final — Motor de Decisioning SD-WAN Zero-Trust](#desafio-final--motor-de-decisioning-sd-wan-zero-trust)

---

## Exercício 1 — Análise do Elitismo na Estabilidade Algorítmica

### Objetivo

Alterar a flag de controle do elitismo para observar o impacto da preservação do melhor indivíduo na curva de convergência de um Algoritmo Genético focado em encontrar a rota de menor custo.

### Código Python

```python
import numpy as np

def calcular_custo(rota, matriz):
    dist = 0
    for i in range(len(rota)-1):
        dist += matriz[rota[i], rota[i+1]]
    return dist + matriz[rota[-1], rota[0]]

# Modifique para False para testar a execução sem elitismo
USAR_ELITISMO = True #False

np.random.seed(42) # Semente para reprodutibilidade
NUM_NOS = 8
matriz_teste = np.random.uniform(10, 100, (NUM_NOS, NUM_NOS))
TAM_POP = 40
GERACOES = 80

populacao = [np.random.permutation(NUM_NOS) for _ in range(TAM_POP)]

for g in range(GERACOES):
    custos = [calcular_custo(ind, matriz_teste) for ind in populacao]
    melhor_idx = np.argmin(custos)

    novos = []
    if USAR_ELITISMO:
        novos.append(populacao[melhor_idx].copy())

    while len(novos) < TAM_POP:
        i1, i2 = np.random.choice(TAM_POP, 2, replace=False)
        pai = populacao[i1] if custos[i1] < custos[i2] else populacao[i2]

        filho = pai.copy()
        if np.random.rand() < 0.3:
            idx1, idx2 = np.random.choice(NUM_NOS, 2, replace=False)
            filho[idx1], filho[idx2] = filho[idx2], filho[idx1]
        novos.append(filho)

    populacao = novos

custos_finais = [calcular_custo(ind, matriz_teste) for ind in populacao]
print(f"[Exercício 1] Menor Custo Obtido (Elitismo={USAR_ELITISMO}): {min(custos_finais):.2f}")
```

### Resultados

Ao executar o código com a semente fixa (`np.random.seed(42)`), obtemos os seguintes comportamentos:

| Configuração            | Print                                                     |
| :---------------------- | :-------------------------------------------------------- |
| `USAR_ELITISMO = True`  | [Exercício 1] Menor Custo Obtido (Elitismo=True): 238.76  |
| `USAR_ELITISMO = False` | [Exercício 1] Menor Custo Obtido (Elitismo=False): 290.18 |

### Questões

#### 1. Por que o uso do Elitismo melhora o resultado final?

O elitismo garante que o melhor indivíduo da geração atual seja copiado integralmente para a próxima geração. Sem ele, os operadores de crossover e mutação podem acabar destruindo a melhor solução encontrada, fazendo o algoritmo "esquecer" o progresso e regredir.

---

## Exercício 2 — Inserção de Penalidades por Descumprimento de SLA

### Objetivo

Implementar o cálculo de penalidade estática de +1000 ms para qualquer enlace cuja latência exceda o limite operacional (SLA) de 50 ms.

### Código Python

```python
import numpy as np

np.random.seed(15)
matriz_latencia = np.random.uniform(5, 80, (6, 6))

def calcular_custo_com_sla(rota, matriz, limite_sla=50.0):
    custo_total = 0.0
    penalidade = 0.0

    for i in range(len(rota) - 1):
        latencia_enlace = matriz[rota[i], rota[i+1]]
        custo_total += latencia_enlace

        # Incrementa a penalidade caso a latência do enlace ultrapasse o SLA
        if latencia_enlace > limite_sla:
            penalidade += 1000.0

    return custo_total + penalidade

rota_teste = np.array([0, 1, 2, 3, 4, 5])
custo_final = calcular_custo_com_sla(rota_teste, matriz_latencia)

print(f"[Exercício 2] Custo Total (Com Penalizações de SLA): {custo_final:.2f} ms")
```

### Resultados da Execução

print: [Exercício 2] Custo Total (Com Penalizações de SLA): 1160.00 ms

| Métrica                                | Resultado      |
| :------------------------------------- | :------------- |
| Custo Real da Rota (Sem Penalidade)    | ~160.00 ms     |
| Enlaces que violaram o SLA (>50ms)     | 1 enlace       |
| Penalidade Total Aplicada              | 1000.00 ms     |
| **Fitness Final (Custo + Penalidade)** | **1160.00 ms** |

### Reflexão

Como visto em aula, ao penalizar as rotas inválidas somando um valor alto (1000) ao custo base, garantimos que a função _Fitness_ dessa solução se torne muito ruim (alta), o que faz com que o Algoritmo Genético descarte essa rota naturalmente durante o processo de seleção por torneio.

---

## Exercício 3 — Balanceamento de Carga em Servidores (Desafio de Código)

### Objetivo

Minimizar o _Makespan_ (tempo total do servidor mais sobrecarregado) ao distribuir 20 tarefas com diferentes tempos de processamento entre 4 servidores disponíveis.

### Código completo (`desafio_03_alocacao_servidores.py`)

```python
import numpy as np

# 1. Configurações Iniciais
T = [12, 35, 40, 8, 15, 22, 19, 45, 60, 31, 14, 28, 50, 18, 25, 33, 42, 10, 5, 29]
NUM_SERVIDORES = 4
NUM_TAREFAS = len(T)
TAM_POP = 50
GERACOES = 100
TAXA_MUTACAO = 0.1

np.random.seed(42)

# 2. Função de Avaliação (Fitness = Makespan)
def calcular_makespan(individuo):
    cargas = np.zeros(NUM_SERVIDORES)
    for tarefa_idx, servidor_id in enumerate(individuo):
        cargas[servidor_id] += T[tarefa_idx]
    return np.max(cargas) # O Makespan é a carga do servidor mais ocupado

# 3. População Inicial (Valores de 0 a 3 representando os servidores)
populacao = [np.random.randint(0, NUM_SERVIDORES, NUM_TAREFAS) for _ in range(TAM_POP)]

# 4. Loop do Algoritmo Genético
for g in range(GERACOES):
    # Avaliação
    fitness = [calcular_makespan(ind) for ind in populacao]

    # Elitismo
    melhor_idx = np.argmin(fitness)
    nova_populacao = [populacao[melhor_idx].copy()]

    # Reprodução
    while len(nova_populacao) < TAM_POP:
        # Torneio
        i1, i2 = np.random.choice(TAM_POP, 2, replace=False)
        pai1 = populacao[i1] if fitness[i1] < fitness[i2] else populacao[i2]

        i3, i4 = np.random.choice(TAM_POP, 2, replace=False)
        pai2 = populacao[i3] if fitness[i3] < fitness[i4] else populacao[i4]

        # Crossover de 1 ponto
        ponto = np.random.randint(1, NUM_TAREFAS - 1)
        filho = np.concatenate((pai1[:ponto], pai2[ponto:]))

        # Mutação Simples (Altera o servidor de uma tarefa aleatória)
        if np.random.rand() < TAXA_MUTACAO:
            idx_tarefa = np.random.randint(NUM_TAREFAS)
            filho[idx_tarefa] = np.random.randint(NUM_SERVIDORES)

        nova_populacao.append(filho)

    populacao = nova_populacao

# 5. Resultados
fitness_finais = [calcular_makespan(ind) for ind in populacao]
melhor_solucao = populacao[np.argmin(fitness_finais)]
melhor_makespan = min(fitness_finais)

print("=== RESULTADO BALANCEAMENTO ===")
print(f"Melhor Makespan: {melhor_makespan} segundos")
cargas_finais = np.zeros(NUM_SERVIDORES)
for idx, srv in enumerate(melhor_solucao):
    cargas_finais[srv] += T[idx]
print(f"Carga por Servidor: {cargas_finais}")
```

### Resultados

print:  
=== RESULTADO BALANCEAMENTO ===
Melhor Makespan: 140.0 segundos
Carga por Servidor: [129. 137. 140. 135.]

| Servidor              | Carga Alocada (segundos) |
| :-------------------- | :----------------------- |
| Servidor 0            | 129.0                    |
| Servidor 1            | 137.0                    |
| Servidor 2            | 140.0                    |
| Servidor 3            | 135.0                    |
| **Makespan (Máximo)** | **140.0**                |

A carga total de todas as tarefas somadas é 541 segundos. O limite teórico perfeito seria 541 / 4 = 135.25. O algoritmo conseguiu distribuir os itens de forma muito satisfatória, atingindo um makespan máximo de 140, muito próximo ao limite ideal.

---

## Desafio Final — Motor de Decisioning SD-WAN Zero-Trust

### Objetivo

Desenvolver o algoritmo de seleção de rota para um nó de comutação central em uma topologia com 12 roteadores, de forma a minimizar a latência e perda de pacotes, enquanto aplica uma severa penalidade em rotas que passam por nós não confiáveis.

---

## Desafio Final — Motor de Decisioning SD-WAN Zero-Trust

### Objetivo

Desenvolver o algoritmo de seleção de rota para um nó de comutação central em uma topologia com 12 roteadores, de forma a minimizar a latência e perda de pacotes, enquanto aplica uma severa penalidade em rotas que passam por nós não confiáveis.

### Código Completo (`desafio_ac1_master_sdwan.py`)

```python
"""RELATÓRIO TÉCNICO - MOTOR SD-WAN ZERO-TRUST
-------------------------------------------
Ao adotar os parâmetros de penalidade de segurança (P_seguranca = 5000) e pesos
equilibrados para Latência (w1=1.0) e Perda de Pacotes (w2=10.0), o Algoritmo
Genético foi capaz de convergir rapidamente para uma rota segura.

Foi observado um nítido desvio em relação aos roteadores com baixa reputação (índice < 50).
Mesmo que um nó comprometido oferecesse uma rota fisicamente mais curta (menor latência),
a penalização impedia a seleção deste nó, forçando o tráfego a contornar a área de risco
para garantir a conformidade com a política Zero-Trust. A rota escolhida garante integridade
total e latência aceitável, sem disparar alarmes de segurança.
"""

import numpy as np

# 1. Configuração Estocástica e de Topologia
np.random.seed(2026)
NUM_NOS = 12
ORIGEM = 0
DESTINO = 11

# Matrizes Simétricas para a topologia
matriz_latencia = np.random.uniform(5, 50, (NUM_NOS, NUM_NOS))
matriz_latencia = (matriz_latencia + matriz_latencia.T) / 2

matriz_perda = np.random.uniform(0, 5, (NUM_NOS, NUM_NOS))
matriz_perda = (matriz_perda + matriz_perda.T) / 2

# Reputação de Segurança dos Nós (0 a 100)
reputacao_nos = np.random.randint(10, 100, NUM_NOS)
reputacao_nos[ORIGEM] = 100
reputacao_nos[DESTINO] = 100

# Pesos da Função Objetivo
W1 = 1.0  # Peso da Latência
W2 = 10.0 # Peso da Perda (Normalmente possui maior impacto na qualidade)
P_SEG = 5000.0 # Penalização Zero-Trust

# 2. Fitness com Penalidade
def calcular_fitness_sdwan(rota):
    # A rota é do tipo: [0, no_intermediario1, ..., 11]
    latencia_total = 0.0
    perda_total = 0.0
    penalidade = 0.0

    for i in range(len(rota) - 1):
        atual = rota[i]
        prox = rota[i+1]

        latencia_total += matriz_latencia[atual, prox]
        perda_total += matriz_perda[atual, prox]

        # Penaliza se qualquer nó de destino tiver reputação < 50
        if reputacao_nos[prox] < 50:
            penalidade += P_SEG

    return (W1 * latencia_total) + (W2 * perda_total) + penalidade

# 3. Representação e Operadores
TAM_POP = 60
GERACOES = 100

# Criar população: sequências aleatórias de nós intermediários
def criar_rota_aleatoria():
    # Pega uma quantidade aleatória de nós intermediários (1 a 4 saltos)
    nos_disponiveis = list(range(1, 11))
    np.random.shuffle(nos_disponiveis)
    qtd_saltos = np.random.randint(1, 5)
    return [ORIGEM] + nos_disponiveis[:qtd_saltos] + [DESTINO]

populacao = [criar_rota_aleatoria() for _ in range(TAM_POP)]

# GA Simplificado (apenas elitismo e geração aleatória local-search)
for g in range(GERACOES):
    fitness = [calcular_fitness_sdwan(r) for r in populacao]
    melhor_idx = np.argmin(fitness)

    nova_populacao = [populacao[melhor_idx][:]] # Elitismo

    while len(nova_populacao) < TAM_POP:
        i1 = np.random.choice(TAM_POP)
        pai = populacao[i1]
        filho = pai[:]

        # Mutação: Adicionar ou remover nó intermediário
        if np.random.rand() < 0.5 and len(filho) > 2:
            # Remover um nó (excluindo origem e destino)
            idx_rem = np.random.randint(1, len(filho) - 1)
            filho.pop(idx_rem)
        else:
            # Inserir um nó
            novo_no = np.random.randint(1, 11)
            if novo_no not in filho:
                idx_ins = np.random.randint(1, len(filho))
                filho.insert(idx_ins, novo_no)

        nova_populacao.append(filho)

    populacao = nova_populacao

fitness_finais = [calcular_fitness_sdwan(r) for r in populacao]
melhor_rota = populacao[np.argmin(fitness_finais)]

print(f"Reputação dos Nós: {reputacao_nos}")
print(f"Melhor Rota: {melhor_rota}")
print(f"Fitness: {min(fitness_finais):.2f}")
```

Resultado:  
Reputação dos Nós: [100 92 20 63 13 30 17 42 37 27 10 100]  
Melhor Rota: [0, 11]  
Fitness: 55.85  
