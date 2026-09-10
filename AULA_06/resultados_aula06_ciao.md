# RELATÓRIO FINAL — AULA 05
## ANT COLONY OPTIMIZATION (ACO)

**Data de execução:** 09/09/2026
**Alunos:** Gabriel Orides - 106541 | Davi Kazussuke - 90613

---

## 1. Objetivo

O objetivo dessa atividade é compreender o uso e desenvolvimento de um algoritmo de otimização utilizando ant colony optimization, um tipo de otimização utilizando de uma tecnica de feromonios que busca por uma rota mais eficiente via experiencia de outras "formigas" e orientação por custo de rota e atração por "feromonios"

---

# LABORATÓRIO — ACO: OTIMIZAÇÃO POR COLÔNIA DE FORMIGAS

## Objetivo: Implementar uma versão simples do **Ant Colony Optimization (ACO)** para encontrar uma boa rota em uma rede de nós.

## Resultado: Matriz inicial de feromônio:
```
[[1. 1. 1. 0. 0. 0.]
 [1. 1. 1. 1. 0. 0.]
 [1. 1. 1. 1. 1. 0.]
 [0. 1. 1. 1. 1. 1.]
 [0. 0. 1. 1. 1. 1.]
 [0. 0. 0. 1. 1. 1.]]
Vizinhos do nó 0: [1, 2]
Vizinhos do nó 2: [0, 1, 3, 4]

Rotas encontradas:
Formiga 1: None
Formiga 2: [0, 1, 2, 3, 4, 5]
Formiga 3: [0, 1, 2, 3, 4, 5]
Formiga 4: [0, 2, 1, 3, 4, 5]
Formiga 5: [0, 1, 3, 4, 5]

Rota: [0, 1, 2, 3, 4, 5]
Custo: 8.0

========== RESULTADO ==========
Melhor rota encontrada: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
```

## perguntas
1. Por que o ACO utiliza várias formigas em vez de apenas uma formiga procurando a melhor rota? Explique qual é a importância de explorar diferentes caminhos.
- O uso de várias formigas é fundamental porque o ACO é um algoritmo de inteligência de enxame que depende do trabalho cooperativo e da exploração paralela. Quantitativamente, ter várias formigas explorando caminhos diferentes ao mesmo tempo garante uma amostragem maior e evita que o algoritmo fique viciado em uma rota inicial ruim (preso em um ótimo local). Além disso, a multiplicidade de formigas agiliza o processo e viabiliza a própria mecânica do feromônio: se houvesse apenas uma formiga, o rastro evaporaria mais rápido do que ela conseguiria reforçar, quebrando o ciclo de aprendizado.

2. Por que uma rota de menor custo recebe mais feromônio? Explique como essa regra influencia o comportamento das próximas formigas.
- Cada feromonio tem um certo tempo de vida, de acordo com a evaporação já discutida, e a tecnica do feromonio é deixar um valor finito de feromonio em cada formiga que é aplicada de forma inversa ao custo da rota, com o tempo este valor abaixa para que percamos rotas longas e menos favoráveis, Como as próximas formigas fazem escolhas probabilísticas baseadas na atratividade, rotas com mais feromônio têm maior chance de serem escolhidas, criando um ciclo de feedback positivo nas rotas mais curtas.

3. O que poderia acontecer se não existisse evaporação do feromônio? Explique por que manter para sempre as primeiras informações encontradas poderia prejudicar a busca por soluções melhores.
- Teriamos um numero alto de vicios e sem a evaporação, os primeiros caminhos encontrados acumulariam feromônio para sempre. Isso causaria uma convergência prematura, onde a colônia inteira ficaria 'cega' para caminhos novos e melhores que fossem descobertos depois, ficando eternamente viciada nas primeiras rotas (que podem ser péssimas).

---

# LABORATÓRIO 02 — EXPERIMENTANDO O ACO

# Objetivo: compreender, por meio de experimentos, como os principais parâmetros do ACO influenciam a busca por uma boa rota.

Neste laboratório, o código principal já está pronto. O trabalho será modificar os parâmetros, executar novamente e registrar os resultados. *

## Resultado
```
========== RESULTADO DO EXPERIMENTO lab 2 ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 0.1
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0

====================================================

========== RESULTADO DO EXPERIMENTO lab 2 ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 5.0
BETA: 2.0
Taxa de evaporação: 0.5
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0

```
1. Pergunta para discussão:

Quando aumentamos o ALPHA, a influência da experiência acumulada pelas formigas aumenta ou diminui?
- Os graficos visualmente mudam de acordo com a configuração, demonstrando variação e aparente diminui.

```
========== RESULTADO DO EXPERIMENTO lab 2 ==========
Número de formigas: 20
Número de iterações: 50
ALPHA: 5.0
BETA: 2.0
Taxa de evaporação: 0.9
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
*sem mudanças visiveis nos grafos*
```

2. Pergunta para discussão:

O que acontece quando o algoritmo esquece rapidamente as experiências anteriores?
- embora não foi possivel recriar uma demonstração visual nos graficos, em um teste desse tipo de algoritmo, supomos que caminhos viciados e cheios de gargalos de optimização estariam prezentes

---

# LABORATÓRIO 03 — COMPLETANDO O ACO

## Objetivo: implementar partes importantes do ACO a partir do código estudado no Laboratório 01.

## Resultado
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0


## perguntas
1. - Por que a fórmula da atratividade utiliza $1 / custo$ em vez de utilizar diretamente o custo?
- Porque o objetivo do algoritmo é encontrar o caminho mais curto (minimizar o custo). Se usássemos o custo diretamente, caminhos mais longos e caros teriam uma atratividade maior. Ao usar a proporção inversa ($1 / custo$), garantimos que quanto menor o custo, maior será a atratividade

2. - O que acontece com a atratividade quando uma rota recebe mais feromônio?
- A atratividade aumenta. O algoritmo usa um sistema de feedback positivo: caminhos que são bons recebem mais feromônio, e como a quantidade de feromônio multiplica o valor da atratividade, isso faz com que a probabilidade das próximas formigas escolherem essa mesma rota seja cada vez maior.

3. - Por que a função construir_rota() precisa impedir que a formiga visite novamente um nó que já está na rota?
- Para evitar loops infinitos. Se a formiga pudesse voltar para um nó que já visitou, ela poderia ficar presa andando em círculos entre dois ou mais nós para sempre, falhando em construir um caminho válido do ponto de origem até o destino.

## Análise
    O algoritmo obteve sucesso ao encontrar a rota de menor custo possível da rede ([0, 1, 2, 3, 4, 5], custo 8.0). Esse resultado demonstra na prática o funcionamento da inteligência de enxame: as rotas ineficientes foram descartadas pela evaporação contínua, enquanto o trajeto mais curto recebeu reforço progressivo de feromônio, fazendo com que as formigas convergissem de forma autônoma para a solução ótima do problema.


---

# LABORATÓRIO 04 — ACO DO ZERO

## Missão: Construir, do zero, um algoritmo capaz de encontrar uma boa rota entre dois nós de uma rede utilizando o conceito de ACO.

Codigo completo: 

```
import numpy as np
import random
import matplotlib.pyplot as plt

# 1 - Representar a rede utilizando uma matriz de custos
CUSTOS = np.array([
    [0, 2, 4, np.inf, np.inf, np.inf],
    [2, 0, 1, 5, np.inf, np.inf],
    [4, 1, 0, 2, 3, np.inf],
    [np.inf, 5, 2, 0, 1, 4],
    [np.inf, np.inf, 3, 1, 0, 2],
    [np.inf, np.inf, np.inf, 4, 2, 0]
])

ORIGEM = 0
DESTINO = 5

# Parâmetros mínimos
NUM_FORMIGAS = 20
NUM_ITERACOES = 50
ALPHA = 1.0
BETA = 2.0
TAXA_EVAPORACAO = 0.5
Q = 100

# 2 - Criar uma matriz de feromônio
feromonio = np.ones_like(CUSTOS, dtype=float)
feromonio[CUSTOS == np.inf] = 0

def obter_vizinhos(no):
    #Retorna os vizinhos acessíveis de um nó.
    return [i for i in range(len(CUSTOS)) if i != no and CUSTOS[no][i] != np.inf]

def calcular_atratividade(atual, proximo):
    #Calcula o quão atraente é o próximo nó.
    return (feromonio[atual][proximo] ** ALPHA) * ((1 / CUSTOS[atual][proximo]) ** BETA)

# 4 - Fazer cada formiga construir uma rota
def construir_rota():
    rota = [ORIGEM]
    atual = ORIGEM

    while atual != DESTINO:
        vizinhos = obter_vizinhos(atual)

        # 5 - Impedir que uma formiga visite novamente um nó (evita loops)
        candidatos = [n for n in vizinhos if n not in rota]

        if not candidatos:
            return None # Formiga ficou presa, rota inválida

        atratividades = [calcular_atratividade(atual, c) for c in candidatos]
        soma = sum(atratividades)
        probabilidades = [a / soma for a in atratividades]

        # Escolha probabilística baseada na atratividade
        proximo = random.choices(candidatos, weights=probabilidades, k=1)[0]
        rota.append(proximo)
        atual = proximo

    return rota

# 6 - Calcular o custo de cada rota
def calcular_custo(rota):
    return sum(CUSTOS[rota[i]][rota[i+1]] for i in range(len(rota) - 1))

# 8 - Aplicar evaporação
def evaporar_feromonio():
    global feromonio
    feromonio *= (1 - TAXA_EVAPORACAO)
    feromonio[CUSTOS == np.inf] = 0

# 7 - Reforçar as melhores rotas com feromônio
def depositar_feromonio(rota, custo):
    deposito = Q / custo
    for i in range(len(rota) - 1):
        feromonio[rota[i]][rota[i+1]] += deposito


# main

melhor_rota = None
melhor_custo = float('inf')
historico = []

# 9 - Repetir o processo por várias iterações
for _ in range(NUM_ITERACOES):
    rotas_da_iteracao = []

    # 3 - Criar várias formigas
    for _ in range(NUM_FORMIGAS):
        rota = construir_rota()
        if rota is not None:
            custo = calcular_custo(rota)
            rotas_da_iteracao.append((rota, custo))

            if custo < melhor_custo:
                melhor_custo = custo
                melhor_rota = rota.copy()

    evaporar_feromonio()

    for rota, custo in rotas_da_iteracao:
        depositar_feromonio(rota, custo)

    historico.append(melhor_custo)
print("\n========== RESULTADO ==========")
print("Melhor rota encontrada:")
print(melhor_rota)
print(f"\nMelhor custo:\n{melhor_custo}")
plt.figure(figsize=(8, 4))
plt.plot(historico, marker='o', linestyle='-', color='b')
plt.title("Convergência do ACO - Evolução do Melhor Custo")
plt.xlabel("Iteração")
plt.ylabel("Custo da Melhor Rota")
plt.grid(True)
plt.show()
```

# Resultado:
```
========== RESULTADO ==========
Melhor rota encontrada:
[0, 1, 2, 4, 5]

Melhor custo:
8.0
```
## perguntas:

1. - Explique, com suas palavras, como o feromônio ajuda o ACO a aprender quais caminhos são melhores.
- A Tecnica de feromonio ajuda pares e iterações de gerações de formigas a encontrar caminhos juntas sem comunicação direta e sem varias e varias gerações, oque permite algoritmos mais eficientes.

2. - Qual é a diferença entre explorar novos caminhos e aproveitar caminhos que já demonstraram ser bons?
- Exploração (Exploration): É a capacidade das formigas de desviarem das rotas óbvias e testarem caminhos novos, mesmo que tenham pouco feromônio. Isso evita que o algoritmo fique preso em uma solução "ok", mas que não é a melhor possível.

- Aproveitamento (Exploitation): É a tendência das formigas de seguirem os rastros fortes de feromônio deixados anteriormente, garantindo que boas soluções já descobertas sejam otimizadas e utilizadas. O ACO equilibra isso através do uso de probabilidades na hora da escolha do caminho.

3. - Se você precisasse melhorar o desempenho desse ACO para uma rede muito maior, qual parâmetro ou parte do algoritmo você investigaria primeiro? Justifique.
- Investigaria primeiro a relação entre a TAXA_EVAPORACAO e o ALPHA/BETA.
Justificativa: Em redes gigantes, o número de caminhos possíveis cresce absurdamente. Se a evaporação for muito baixa, as formigas podem se fixar rapidamente no primeiro caminho razoável que encontrarem (convergência prematura) e ignorar rotas melhores. Por outro lado, aumentar o peso do BETA ajudaria as formigas a serem mais inteligentes no início, preferindo ligações curtas logo de cara em vez de vagarem aleatoriamente em uma rede imensa. Adequar esses parâmetros é essencial para escalar o algoritmo.
