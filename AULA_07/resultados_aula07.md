# RELATÓRIO FINAL — AULA 07
## LABORATÓRIO PRÁTICO DE META-HEURÍSTICAS

**Data de execução:** 17/09/2026  
**Alunos:** Gabriel Orides - 106541 | Davi Kazussuke - 90613

---

## 1. Objetivo

Testar cinco técnicas de otimização: ACO com busca local, algoritmo genético, PSO, atualização de feromônio e hill climbing. Os códigos completos estão neste diretório. Os resultados a seguir foram obtidos executando esses arquivos em Python; nos LABs 02, 03 e 05, os números podem mudar em outra execução porque não há semente aleatória definida.

---

# LABORATÓRIO 01 — ACO COM BUSCA LOCAL

## Objetivo

Encontrar um ciclo de baixo custo usando ACO e refiná-lo com 2-opt.

**Código:** [`lab01_aula07.py`](lab01_aula07.py)

## Resultado

```text
[LAB 01 - SUCESSO] Melhor Caminho: [0, 1, 3, 4, 2, 0] | Custo: 70
```

![Gráfico de convergência do LAB 01](convergencia_lab01.png)

## Questões técnicas

1. **Como o uso da busca local 2-opt afeta o equilíbrio entre Exploration e Exploitation na busca de caminhos?**
   - As formigas testam caminhos diferentes; o 2-opt melhora cada caminho encontrado invertendo trechos da rota. Assim, aumenta o aproveitamento das soluções e pode diminuir a variedade de rotas reforçadas.

2. **O que aconteceria com a convergência do algoritmo se a taxa de evaporação (`rho`) fosse definida em `0.0 (sem evaporação)`?**
   - O feromônio antigo nunca diminuiria. As primeiras rotas favorecidas tenderiam a receber cada vez mais atenção, podendo fazer o algoritmo se prender cedo a elas.

---

# LABORATÓRIO 02 — ALGORITMO GENÉTICO: SELEÇÃO, CROSSOVER E MUTAÇÃO

## Objetivo

Escolher itens da mochila com peso máximo de 15 por seleção, cruzamento e mutação.

**Código:** [`lab02_aula07.py`](lab02_aula07.py)

## Resultado

```text
[LAB 02] Melhor indivíduo da população final: [0, 1, 1, 1, 1]
[LAB 02] Peso: 8 | Valor/Fitness: 15
```

## Questões técnicas

1. **Explique qual é o papel do operador de Mutação em um Algoritmo Genético e o que ocorre se a taxa de mutação for configurada em 100%.**
   - A mutação ajuda a testar combinações novas. Com taxa de 100%, o código inverteria todos os bits de cada filho, dificultando a preservação das boas escolhas dos pais.

2. **Por que a penalização do fitness (atribuir 0 para indivíduos que estouram a capacidade) é fundamental para a convergência das restrições?**
   - Ela impede que soluções que ultrapassam o peso máximo ganhem torneios apenas por ter alto valor. Assim, a seleção tende a favorecer mochilas válidas.

---

# LABORATÓRIO 03 — PSO: INÉRCIA, COMPONENTE COGNITIVA E SOCIAL

## Objetivo

Aproximar as partículas do mínimo de `f(x, y) = x² + y²`, localizado em `(0, 0)`.

**Código:** [`lab03_aula07.py`](lab03_aula07.py)

## Resultado

```text
[LAB 03] Melhor posição encontrada pelo Enxame (gbest): [-0.00278982 -0.00347603]
```

## Questões técnicas

1. **O que acontece com o comportamento das partículas se zerarmos a componente cognitiva (`c1 = 0`)?**
   - Elas deixam de usar a própria melhor posição para ajustar a velocidade e passam a seguir apenas a inércia e a melhor posição do enxame. Isso pode diminuir a diversidade da busca.

2. **Qual a função do parâmetro de Inércia (`w`) na busca por mínimos globais?**
   - A inércia controla quanto da velocidade anterior é mantido. Valores maiores fazem as partículas explorar mais; valores menores ajudam a desacelerar perto de uma solução.

---

# LABORATÓRIO 04 — ACO: FEROMÔNIO, EVAPORAÇÃO E ATRATIVIDADE

## Objetivo

Evaporar 25% do feromônio e depositar `1/custo` nas arestas de dois caminhos de teste.

**Código:** [`lab04_aula07.py`](lab04_aula07.py)

## Resultado

```text
[LAB 04] Matriz de Feromônio Atualizada:
 [[0.75       0.91666667 0.91666667 0.75      ]
 [0.75       0.75       0.75       1.08333333]
 [0.75       0.91666667 0.75       0.75      ]
 [0.75       0.75       0.75       0.75      ]]
```

As entradas percorridas pelos dois caminhos recebem depósito; a aresta `1 → 3`, comum aos dois, recebe dois depósitos.

## Questões técnicas

1. **Por que a evaporação do feromônio é necessária no algoritmo ACO?**
   - Ela diminui a influência de caminhos antigos, deixando espaço para testar outros. Aqui, cada valor inicial `1` cai para `0,75` antes dos depósitos.

2. **O que ocorreria em grafos complexos sem ela? Qual a relação matemática entre a latência de um enlace e sua atratividade inicial (`eta`) para as formigas?**
   - Sem evaporação, os caminhos escolhidos no começo poderiam dominar a busca. A atratividade usual é `eta = 1/latência`: quanto menor a latência, mais atraente é o enlace. Este código atualiza apenas o feromônio; não calcula `eta`.

---

# LABORATÓRIO 05 — MEMÉTICO: META-HEURÍSTICA + BUSCA LOCAL

## Objetivo

Refinar uma solução da função Rastrigin por pequenas mudanças aceitas apenas quando reduzem o fitness.

**Código:** [`lab05_aula07.py`](lab05_aula07.py). O roteiro testa aqui só a busca local, sem um algoritmo populacional completo.

## Resultado

```text
[LAB 05] Solução Inicial: [ 2.5 -3.1] | Fitness: 37.7698
[LAB 05] Solução Refinada: [ 2.47884131 -3.01739915] | Fitness: 35.2208
```

## Questões técnicas

1. **Qual a diferença fundamental de conceito entre um Algoritmo Genético Puro e um Algoritmo Memético?**
   - O genético evolui uma população por seleção, cruzamento e mutação. O memético acrescenta uma busca local para melhorar indivíduos. Este laboratório mostra apenas essa etapa local.

2. **Em termos de custo computacional, qual o impacto de executar a busca local sobre todos os indivíduos de uma população a cada geração?**
   - O programa precisa avaliar muitos vizinhos extras. Com `P` indivíduos, `G` gerações e `S` tentativas locais, isso pode acrescentar até cerca de `P × G × S` avaliações.

---

## Análise

Os cinco testes mostram maneiras diferentes de procurar soluções melhores. O ACO reforça rotas, o algoritmo genético combina escolhas, o PSO ajusta posições em grupo e a busca local melhora uma solução por vez. Os outputs registram uma execução dos códigos, e os valores aleatórios dos LABs 02, 03 e 05 podem variar.
