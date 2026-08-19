# Laboratórios de Otimização Combinatória

Este repositório reúne três atividades práticas sobre **força bruta**, **crescimento combinatório** e **heurísticas de otimização**.

## Conteúdo

- [Lab 01 — Problema da Mochila por força bruta](#lab-01--problema-da-mochila-por-força-bruta)
- [Lab 02 — Problema do Caixeiro-Viajante por força bruta](#lab-02--problema-do-caixeiro-viajante-por-força-bruta)
- [Lab 03 — Heurística Gulosa e Gap de Otimalidade](#lab-03--heurística-gulosa-e-gap-de-otimalidade)
- [Conclusão](#conclusão)

---

## Lab 01 — Problema da Mochila por força bruta

### Objetivo

Resolver uma instância do **Problema da Mochila** por força bruta. O algoritmo avalia todas as combinações possíveis e seleciona os itens com maior valor total sem ultrapassar a capacidade disponível.

### Resultados

| Métrica | Resultado |
|---|---:|
| Soluções avaliadas | 32 |
| Tempo de execução | 0,000224 s |
| Melhor valor encontrado | 9 |
| Combinação ótima | `(1, 1, 0, 1, 1)` |

Na combinação apresentada, `0` significa que o item não foi escolhido e `1` significa que o item foi escolhido.

### Itens escolhidos

| Item | Peso | Valor |
|---|---:|---:|
| Livro | 2 | 3 |
| Fone | 1 | 2 |
| Carregador | 1 | 3 |
| Chocolate | 1 | 1 |
| **Total** | **5** | **9** |

### Questões

#### 1. Por que o total de soluções avaliadas é exatamente 32?

Existem cinco itens e, para cada um, há duas possibilidades: levar ou não levar. Portanto, o total de combinações é:

```text
2⁵ = 2 × 2 × 2 × 2 × 2 = 32
```

#### 2. O que aconteceria se fossem utilizados 15 itens?

O número de possibilidades aumentaria exponencialmente:

```text
2¹⁵ = 32.768 combinações
```

Isso exigiria mais processamento. Para quantidades ainda maiores de itens, o tempo de execução aumentaria rapidamente.

#### 3. Qual problema da vida real é semelhante a este?

Um exemplo é a organização de uma mala para viagem. Cada objeto possui peso e importância, enquanto a mala tem capacidade limitada. É necessário escolher os itens mais importantes sem ultrapassar o peso permitido.

---

## Lab 02 — Problema do Caixeiro-Viajante por força bruta

### Objetivo

Resolver pequenas instâncias do **Problema do Caixeiro-Viajante**, também chamado de **Traveling Salesman Problem (TSP)**, avaliando todas as rotas possíveis.

O objetivo é encontrar a rota de menor custo que saia da cidade inicial, visite todas as outras cidades uma vez e retorne ao ponto de partida.

### Resultados do código

| Cidades | Rotas avaliadas | Melhor custo | Melhor rota | Tempo de execução |
|---:|---:|---:|---|---:|
| 4 | 6 | 80 | `(0, 1, 3, 2, 0)` | 0,000124 s |
| 5 | 24 | 41 | `(0, 1, 2, 3, 4, 0)` | 0,000110 s |
| 6 | 120 | 91 | `(0, 1, 3, 4, 5, 2, 0)` | 0,000587 s |

> Os tempos podem variar entre execuções devido ao sistema operacional, ao processador e aos demais processos ativos no computador.

### Tabela da reflexão

| Número de cidades | Rotas avaliadas | Tempo medido | Melhor custo |
|---:|---:|---:|---:|
| 4 | 6 | 0,000099 s | 80 |
| 5 | 24 | 0,000085 s | 41 |
| 6 | 120 | 0,000944 s | 91 |

### Crescimento do número de rotas

Como a cidade inicial permanece fixa, o número de rotas avaliadas é dado por `(n − 1)!`.

| Número de cidades | Cálculo | Rotas possíveis |
|---:|---:|---:|
| 4 | `3!` | 6 |
| 5 | `4!` | 24 |
| 6 | `5!` | 120 |
| 10 | `9!` | 362.880 |
| 15 | `14!` | 87.178.291.200 |

### Questões

#### 1. O número de rotas cresce de forma linear, quadrática ou mais rapidamente?

O número de rotas cresce de forma **fatorial**, seguindo `(n − 1)!`. Foram avaliadas 6 rotas com 4 cidades, 24 com 5 e 120 com 6. Portanto, o crescimento é muito mais rápido que o linear ou o quadrático.

#### 2. Quanto tempo levaria para 10 cidades no mesmo computador?

Com 10 cidades, seriam avaliadas:

```text
9! = 362.880 rotas
```

No teste com 6 cidades, 120 rotas levaram 0,000944 segundo. A quantidade de rotas para 10 cidades seria 3.024 vezes maior:

```text
0,000944 × 3.024 ≈ 2,85 segundos
```

Assim, estima-se um tempo de aproximadamente **2,85 segundos**, embora o valor real possa variar entre execuções.

#### 3. Por que o TSP é considerado um problema difícil?

O TSP é difícil porque a quantidade de rotas cresce fatorialmente conforme novas cidades são adicionadas. Dessa forma, a força bruta rapidamente se torna inviável. Em termos formais, a versão de otimização do TSP é classificada como **NP-difícil**, o que motiva o uso de algoritmos mais eficientes, aproximações e heurísticas em instâncias maiores.

---

## Lab 03 — Heurística Gulosa e Gap de Otimalidade

### Objetivo

Comparar uma solução ótima do Problema da Mochila, encontrada por força bruta, com uma solução produzida por uma **heurística gulosa**.

A heurística ordena os itens pela relação `valor/peso` e adiciona primeiro aqueles com maior densidade de valor. Para medir a diferença entre as soluções, utiliza-se o **gap de otimalidade**:

```text
Gap (%) = ((valor ótimo − valor da heurística) / valor ótimo) × 100
```

Um gap de `0%` indica que a heurística encontrou o mesmo valor da solução ótima. Quanto maior o gap, maior a diferença entre as soluções.

### Código completo

```python
import numpy as np
import itertools


# ----------------------------------------------------------
# 1. Função que resolve a mochila por força bruta (ótima)
# ----------------------------------------------------------
def mochila_otima(pesos, valores, capacidade):
    n = len(pesos)
    melhor = 0

    for comb in itertools.product([0, 1], repeat=n):
        peso = sum(pesos[i] for i in range(n) if comb[i] == 1)

        if peso <= capacidade:
            valor = sum(valores[i] for i in range(n) if comb[i] == 1)

            if valor > melhor:
                melhor = valor

    return melhor


# ----------------------------------------------------------
# 2. Heurística gulosa
# ----------------------------------------------------------
def mochila_gulosa(pesos, valores, capacidade):
    n = len(pesos)
    densidade = [(valores[i] / pesos[i], i) for i in range(n)]
    densidade.sort(reverse=True)

    valor_total = 0
    peso_atual = 0

    for dens, i in densidade:
        if peso_atual + pesos[i] <= capacidade:
            peso_atual += pesos[i]
            valor_total += valores[i]

    return valor_total


# ----------------------------------------------------------
# 3. Calcula o gap percentual
# ----------------------------------------------------------
def calcular_gap(valor_heuristica, valor_otimo):
    if valor_otimo == 0:
        return 0

    gap = ((valor_otimo - valor_heuristica) / valor_otimo) * 100
    return gap


# ----------------------------------------------------------
# 4. Experimento com várias instâncias aleatórias
# ----------------------------------------------------------
np.random.seed(42)

n_itens = 12
capacidade = 30
n_instancias = 20
gaps = []

print("Rodando", n_instancias, "instâncias...")

for k in range(n_instancias):
    pesos = np.random.randint(1, 15, size=n_itens)
    valores = np.random.randint(10, 50, size=n_itens)

    otimo = mochila_otima(pesos, valores, capacidade)
    heur = mochila_gulosa(pesos, valores, capacidade)

    gap = calcular_gap(heur, otimo)
    gaps.append(gap)

    print(
        f"Instância {k + 1:2d} | "
        f"Ótimo: {otimo:4d} | "
        f"Gulosa: {heur:4d} | "
        f"Gap: {gap:5.1f}%"
    )


# ----------------------------------------------------------
# 5. Estatísticas finais
# ----------------------------------------------------------
print("\n===== RESUMO =====")
print(f"Gap médio     : {np.mean(gaps):.2f}%")
print(f"Gap mínimo    : {np.min(gaps):.2f}%")
print(f"Gap máximo    : {np.max(gaps):.2f}%")
print(f"Desvio padrão : {np.std(gaps):.2f}%")
```

### Resultados por instância

| Instância | Valor ótimo | Valor da gulosa | Gap |
|---:|---:|---:|---:|
| 1 | 199 | 199 | 0,0% |
| 2 | 170 | 170 | 0,0% |
| 3 | 155 | 155 | 0,0% |
| 4 | 147 | 147 | 0,0% |
| 5 | 261 | 261 | 0,0% |
| 6 | 214 | 214 | 0,0% |
| 7 | 191 | 187 | 2,1% |
| 8 | 183 | 183 | 0,0% |
| 9 | 215 | 206 | 4,2% |
| 10 | 174 | 174 | 0,0% |
| 11 | 262 | 262 | 0,0% |
| 12 | 206 | 206 | 0,0% |
| 13 | 231 | 231 | 0,0% |
| 14 | 309 | 309 | 0,0% |
| 15 | 294 | 294 | 0,0% |
| 16 | 247 | 247 | 0,0% |
| 17 | 136 | 134 | 1,5% |
| 18 | 212 | 212 | 0,0% |
| 19 | 243 | 243 | 0,0% |
| 20 | 193 | 193 | 0,0% |

### Resumo estatístico

| Estatística | Resultado |
|---|---:|
| Gap médio | 0,39% |
| Gap mínimo | 0,00% |
| Gap máximo | 4,19% |
| Desvio padrão | 1,03% |

Em **17 das 20 instâncias**, equivalentes a **85% dos testes**, a heurística gulosa encontrou o mesmo valor da solução ótima. Nas três instâncias restantes, os gaps foram pequenos, e o maior deles foi de 4,19%.

### Questão

#### 1. A heurística gulosa é boa o suficiente para este problema? Quando utilizá-la?

Nos testes realizados, a heurística gulosa apresentou bom desempenho, com gap médio de apenas **0,39%** e solução ótima em **85% das instâncias**. Portanto, ela é adequada quando se precisa encontrar rapidamente uma solução satisfatória, especialmente em problemas com muitos itens, nos quais a força bruta demoraria demais.

Entretanto, a heurística não garante a solução ótima. É preferível gastar mais tempo procurando o ótimo quando o problema possui poucos itens ou quando uma pequena diferença no resultado pode causar grande impacto, como em decisões financeiras, industriais ou logísticas importantes.

---

## Conclusão

Os experimentos demonstram que algoritmos de força bruta conseguem encontrar soluções ótimas, mas apresentam crescimento exponencial ou fatorial, tornando-se inviáveis para entradas grandes.

As heurísticas oferecem uma alternativa mais rápida. Embora não garantam o resultado ótimo, podem produzir soluções muito próximas dele em pouco tempo. No Lab 03, a estratégia gulosa apresentou um gap médio baixo e encontrou o ótimo na maioria das instâncias, mostrando um bom equilíbrio entre qualidade da solução e velocidade de execução.
