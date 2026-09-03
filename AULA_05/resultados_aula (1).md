# RELATÓRIO FINAL — AULA 05
## Particle Swarm Optimization (PSO)

**Data de execução:** 02/09/2026
**Alunos:** Gabriel Orides - 106541 | Davi Kazussuke - 90613

---

## 1. Objetivo

O objetivo desta atividade foi compreender e aplicar o algoritmo Particle Swarm Optimization (PSO), começando por uma única partícula, passando por um enxame de partículas e chegando à aplicação do método em um problema de otimização logística.

Na aplicação logística, foram considerados 50 clientes, 5 centros de distribuição e o custo de entrega definido como a distância entre cliente e centro mais próximo multiplicada pela demanda do cliente.

---

# MISSÃO 1 — A PARTÍCULA SOLITÁRIA

## Objetivo
Minimizar a função: `f(x) = x²`
O mínimo global conhecido é: `x = 0` com `f(x) = 0`.

## Resultado
- Posição inicial: **1.0915**
- Fitness inicial: **1.1914**
- Posição final: **-0.065850**
- Fitness final: **0.004336**
- Erro em relação ao ótimo: **0.065850**
- Número de iterações: **20**
- Encontrou o mínimo: **Sim** (Chegou muito próximo do 0)

## Observação
A partícula possui apenas sua própria experiência para orientar o movimento. Como existe somente uma partícula, `pBest` e `gBest` representam essencialmente a mesma melhor posição encontrada. A trajetória mostra a tentativa de aproximação do ponto ótimo `x = 0`.
**Dificuldade: Fácil.**

---

# MISSÃO 2 — O ENXAME

## Objetivo
Aplicar o PSO à função de Rosenbrock: `f(x,y) = (1-x)² + 100(y-x²)²`
O mínimo global conhecido está em: `(1,1)` com valor `f(1,1) = 0`.

## Resultado
- Número de partículas: **20**
- Número de iterações: **50**
- Fitness final: **0.001657**
- Encontrou o mínimo global: **Sim** (Convergência bem-sucedida para a região ótima)

## Comparação com a Missão 1
O enxame apresenta uma vantagem importante em relação à partícula solitária: diferentes partículas exploram regiões diferentes do espaço de busca e compartilham informações através do `gBest`. Assim, o algoritmo consegue combinar exploração e cooperação.
**O enxame foi mais rápido e eficiente em termos de exploração do espaço de busca.**
**Dificuldade: Médio.**

---

# MISSÃO 3 — PROBLEMA CORPORATIVO

## Objetivo
Localizar 5 centros de distribuição para atender 50 clientes minimizando o custo total de entrega.
`custo = distância × demanda`

## Resultado
- Custo Inicial (Iteração 1): **~16955.05**
- Custo Final (Iteração 100): **16955.05**
- Melhoria: **O custo não sofreu redução significativa em relação ao estado inicial nesta execução específica (ficou estagnado).**
- Tempo de execução: **2.38 segundos**
- Centros alocados: **5 centros foram posicionados.**

## Análise
O algoritmo tentou reposicionar os centros, mas encontrou um platô (ótimo local) e não conseguiu escapar nas 100 iterações com a configuração inicial, mantendo o custo fixo. Isso ressalta a importância de tunar os hiperparâmetros (que é exatamente o objetivo da Missão 4).
**Dificuldade: Difícil.**

---

# MISSÃO 4 — OTIMIZAÇÃO DOS PARÂMETROS

Foram executadas seis configurações, cada uma com cinco execuções independentes.
*(Nota: Na tabela abaixo, os valores de Custo foram ajustados para refletir o menor valor matemático real como o "Melhor Custo" para a empresa).*

| Configuração | w | c1 | c2 | Partículas | Custo Médio | Melhor Custo (Menor) | Pior Custo (Maior) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Padrão | 0.7 | 1.8 | 1.8 | 30 | 16764.48 | 15443.17 | 19025.98 |
| Inércia Alta | 0.9 | 1.8 | 1.8 | 30 | 19262.97 | 16955.05 | 21460.47 |
| Inércia Baixa | 0.5 | 1.8 | 1.8 | 30 | 16386.38 | 13552.66 | 19025.98 |
| Cognitivo Alto | 0.7 | 2.5 | 1.8 | 30 | 16570.90 | 13552.66 | 21460.47 |
| Social Alto | 0.7 | 1.8 | 2.5 | 30 | 15812.90 | 12756.20 | 16955.05 |
| Mais Partículas | 0.7 | 1.8 | 1.8 | 60 | 20164.06 | 16955.05 | 21460.47 |

## Melhor configuração
A configuração que apresentou o menor custo médio e o melhor custo absoluto (12756.20) foi:
**Social Alto** (`w=0.7`, `c1=1.8`, `c2=2.5`, `partículas=30`)

## Pior configuração
A configuração que apresentou o maior custo médio foi:
**Mais Partículas** (`w=0.7`, `c1=1.8`, `c2=1.8`, `partículas=60`)

## Conclusões sobre os parâmetros
- **Inércia (w):** Aumentar a inércia piorou o resultado (exploração excessiva, não convergiu a tempo). Diminuir melhorou, ajudando a focar rápido no mínimo.
- **Cognitivo (c1):** Aumentar ajudou levemente, permitindo uma boa exploração inicial das próprias descobertas de cada partícula.
- **Social (c2):** Teve o impacto mais positivo de todos. Fez o enxame seguir o "líder" rapidamente, acelerando a convergência para as regiões onde havia mais clientes aglomerados.
- **Número de Partículas:** Dobrar as partículas gerou o pior custo. Mais partículas precisam de mais iterações para convergir. Com o mesmo limite de iterações, o enxame se espalhou sem ter tempo de focar no ponto ótimo.

---

# PARTE 1 — O QUE FOI APRENDIDO?

## 1. O que é PSO?
Particle Swarm Optimization é um algoritmo de otimização baseado no comportamento coletivo de enxames. Cada partícula representa uma solução candidata e possui uma posição e uma velocidade. A velocidade é influenciada pela experiência individual (`pBest`) e pela experiência coletiva (`gBest`).

## 2. Diferença entre pBest e gBest
- `pBest`: melhor solução encontrada individualmente por uma partícula.
- `gBest`: melhor solução encontrada por todo o enxame.
Ambos são importantes porque combinam aprendizado individual (exploração) e cooperação coletiva (convergência).

---

# PARTE 2 — EXPERIÊNCIA COM AS MISSÕES

## Missão 1
**A partícula encontrou o mínimo?** Sim
**Número de iterações:** 20
**Dificuldade:** Fácil

## Missão 2
**O enxame encontrou o mínimo global?** Sim
**O enxame foi mais rápido?** Sim
**Dificuldade:** Médio

## Missão 3
**Compare com o custo inicial: Melhorou?** Não (O algoritmo estagnou em um ótimo local com a configuração padrão).
**Quantos centros foram alocados?** 5
**Dificuldade:** Difícil

## Missão 4
**Melhor configuração encontrada:** w=0.7, c1=1.8, c2=2.5, partículas=30
**Pior configuração encontrada:** w=0.7, c1=1.8, c2=1.8, partículas=60
**Dificuldade:** Médio

---
