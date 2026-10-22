# RELATÓRIO TÉCNICO — AULA 10
## MOTOR DE INFERÊNCIA MAMDANI E SUPERFÍCIE DE DECISÃO 3D

**Data de execução:** 21/10/2026  
**Alunos:** Gabriel Orides - 106541 | Davi Kazussuke - 90613  

---

## 1. Objetivo

Registrar as análises técnicas, respostas conceituais do "Desafio dos Extremos" e a validação do motor de inferência fuzzy Mamdani desenvolvido em Python (Sprint 2 da AC-3). O objetivo do sistema é classificar a porcentagem de Urgência de um incidente de segurança da informação com base no seu Impacto e na sua Explorabilidade, gerando uma superfície de decisão 3D contínua.

---

# LABORATÓRIO 01 — AVALIAÇÃO DE INCIDENTES E DESAFIO DOS EXTREMOS (AULA 10)

## Objetivo

Mapear um conjunto de funções de pertinência e codificar uma matriz completa de 9 regras de inferência fuzzy (3x3) para calcular a porcentagem de Urgência de atendimento de um incidente. O laboratório visa investigar por que o método de defuzzificação por Centroide não atinge os limites exatos ($0\%$ e $100\%$) e comparar abordagens de correção.

**Código:** `lab01_aula10.py`

## Modelagem e Matriz de Regras (3 x 3 = 9 Regras)

### Universos de Discurso e Conjuntos Fuzzy

* **Impacto (Entrada 1):** Universo $[0, 100]\%$. Termos: `Baixo` ($0-40$), `Médio` ($20-80$), `Alto` ($60-100$).
* **Explorabilidade (Entrada 2):** Universo $[0, 10]$. Termos: `Baixa` ($0-4$), `Moderada` ($2-8$), `Alta` ($6-10$).
* **Urgência (Saída):** Universo $[0, 100]\%$. Termos: `Urgência Baixa`, `Urgência Média`, `Urgência Alta`, `Urgência Crítica`.

### Matriz de Decisão Codificada

| Impacto \\ Explorabilidade | Baixa (0–4) | Moderada (2–8) | Alta (6–10) |
| :--- | :--- | :--- | :--- |
| **Baixo (0–40)** | Urgência Baixa | Urgência Baixa | Urgência Média |
| **Médio (20–80)** | Urgência Média | Urgência Alta | Urgência Alta |
| **Alto (60–100)** | Urgência Crítica | Urgência Crítica | Urgência Crítica |

### Regras Mapeadas no Algoritmo

1. **SE** (Impacto é Baixo) **E** (Explorabilidade é Baixa) **ENTÃO** (Urgência é Baixa)
2. **SE** (Impacto é Baixo) **E** (Explorabilidade é Moderada) **ENTÃO** (Urgência é Baixa)
3. **SE** (Impacto é Baixo) **E** (Explorabilidade é Alta) **ENTÃO** (Urgência é Média)
4. **SE** (Impacto é Médio) **E** (Explorabilidade é Baixa) **ENTÃO** (Urgência é Média)
5. **SE** (Impacto é Médio) **E** (Explorabilidade é Moderada) **ENTÃO** (Urgência é Alta)
6. **SE** (Impacto é Médio) **E** (Explorabilidade é Alta) **ENTÃO** (Urgência é Alta)
7. **SE** (Impacto é Alto) **E** (Explorabilidade é Baixa) **ENTÃO** (Urgência é Crítica)
8. **SE** (Impacto é Alto) **E** (Explorabilidade é Moderada) **ENTÃO** (Urgência é Crítica)
9. **SE** (Impacto é Alto) **E** (Explorabilidade é Alta) **ENTÃO** (Urgência é Crítica)

---

## Resultado

```text
RESULTADOS DA SIMULAÇÃO - AVALIAÇÃO DE URGÊNCIA DE INCIDENTES
======================================================================
[Caso Mínimo]  Impacto: 0%   | Explorabilidade: 0.0 -> Urgência: 11.00%
[Caso Médio]   Impacto: 50%  | Explorabilidade: 5.0 -> Urgência: 67.00%
[Caso Máximo]  Impacto: 100% | Explorabilidade: 10.0 -> Urgência: 88.67%
----------------------------------------------------------------------
Status de Execução: OK (9 de 9 regras cobertas sem lacunas)
Saída Gráfica: ![Superfície de Decisão 3D](superficie_decisao.png)
```

---

## Análise Técnica

### 1. Resposta ao "Desafio dos Extremos": Por que o Centroide Triangular não atinge 0% e 100%?

* O método de defuzzificação por **Centroide** calcula o centro de massa geométrico (ponto de equilíbrio) da área agregada gerada pelas regras.
* Ao definir a saída com triângulos nas pontas da escala (como a `Urgência Crítica` variando na borda superior), a figura geométrica possui massa distribuída à esquerda do limite $100\%$.
* Como a área ativada "puxa" o centro de gravidade para o interior do gráfico, o valor calculado matematicamente nunca atinge a ponta exata. Na entrada máxima `(100%, 10)`, a massa acumulada estabiliza o centroide em **$88.67\%$**. O mesmo ocorre no extremo inferior `(0%, 0)`, onde o ponto de equilíbrio geométrico fica em **$11.00\%$**.

---

### 2. Comparação de Soluções: Abordagem A vs. Abordagem B

#### Abordagem A: Uso de Trapézio (`trapmf`) nas bordas superiores/inferiores
* **Mecanismo:** Substitui-se a função de pertinência triangular nas extremidades (`Urgência Baixa` no início e `Urgência Crítica` no topo) por funções trapezoidais que mantêm pertinência $1.0$ contínua até os limites $0\%$ e $100\%$.
* **Efeito:** Adiciona bloco uniforme de massa geométrica rente às bordas do universo de discurso, deslocando o centroide para bem mais próximo de $0\%$ e $100\%$.
* **Vantagem:** Preserva a resposta contínua e a transição suave de acionamento do motor fuzzy no miolo da escala.

#### Abordagem B: Alteração da Defuzzificação para `MOM` (*Mean of Maximum*)
* **Mecanismo:** O método MOM calcula a média dos pontos numéricos onde o grau de pertinência da área agregada atinge o valor máximo ($1.0$).
* **Efeito:** Consegue cravar exatamente **$0\%$** no mínimo e **$100\%$** no máximo.
* **Desvantagem:** Ao descartar a geometria da área e focar apenas no topo do pico de pertinência, o sistema perde a continuidade da saída. A resposta do sistema passa a apresentar "degraus" e saltos abruptos à medida que as entradas variam.

---

### 3. Recomendação de Abordagem

**A Abordagem A (Trapézio + Centroide) é a mais recomendada.**

**Justificativa:** A principal vantagem do controle por Lógica Fuzzy em relação a um sistema On/Off convencional é a **suavidade e proporcionalidade na transição dos dados**. A Abordagem A reduz substancialmente a limitação das bordas sem abrir mão da estabilidade contínua na faixa intermediária. A Abordagem B, apesar de atingir exatamente $100\%$, compromete a estabilidade do sistema ao introduzir respostas discretizadas em saltos.

---

### 4. Análise Interpretativa da Superfície de Decisão 3D

1. **Continuidade da Superfície:** A imagem `superficie_decisao.png` gerada confirma uma superfície contínua e suave sem quebras, degraus indesejados ou regiões nulas. Isso demonstra que as 9 regras cobrem $100\%$ do espaço de estados das entradas.
2. **Proporcionalidade da Resposta:** Nota-se a elevação gradativa do eixo Z (Urgência) conforme o aumento conjunto do Impacto (eixo X) e da Explorabilidade (eixo Y), validando a coerência do motor de inferência Mamdani projetado.

## Objetivo
Mapear um conjunto de funções de pertinência e codificar uma matriz completa de 9 regras de inferência fuzzy (3x3) para calcular a porcentagem de Urgência de atendimento de um incidente. O laboratório visa investigar por que o método de defuzzificação por Centroide não atinge os limites exatos ($0\%$ e $100\%$) e comparar abordagens de correção.

**Código:** `lab01_aula10.py`

## Modelagem e Matriz de Regras (3 x 3 = 9 Regras)

### Universos de Discurso e Conjuntos Fuzzy
- **Impacto (Entrada 1):** Universo $[0, 100]\%$. Termos: `Baixo` ($0-40$), `Médio` ($20-80$), `Alto` ($60-100$).
- **Explorabilidade (Entrada 2):** Universo $[0, 10]$. Termos: `Baixa` ($0-4$), `Moderada` ($2-8$), `Alta` ($6-10$).
- **Urgência (Saída):** Universo $[0, 100]\%$. Termos: `Urgência Baixa`, `Urgência Média`, `Urgência Alta`, `Urgência Crítica`.

### Matriz de Decisão Codificada
| Impacto \ Explorabilidade | Baixa (0–4) | Moderada (2–8) | Alta (6–10) |
| :--- | :--- | :--- | :--- |
| **Baixo (0–40)** | Urgência Baixa | Urgência Baixa | Urgência Média |
| **Médio (20–80)** | Urgência Média | Urgência Alta | Urgência Alta |
| **Alto (60–100)** | Urgência Crítica | Urgência Crítica | Urgência Crítica |

### Regras Mapeadas no Algoritmo
1. **SE** (Impacto é Baixo) **E** (Explorabilidade é Baixa) **ENTÃO** (Urgência é Baixa)
2. **SE** (Impacto é Baixo) **E** (Explorabilidade é Moderada) **ENTÃO** (Urgência é Baixa)
3. **SE** (Impacto é Baixo) **E** (Explorabilidade é Alta) **ENTÃO** (Urgência é Média)
4. **SE** (Impacto é Médio) **E** (Explorabilidade é Baixa) **ENTÃO** (Urgência é Média)
5. **SE** (Impacto é Médio) **E** (Explorabilidade é Moderada) **ENTÃO** (Urgência é Alta)
6. **SE** (Impacto é Médio) **E** (Explorabilidade é Alta) **ENTÃO** (Urgência é Alta)
7. **SE** (Impacto é Alto) **E** (Explorabilidade é Baixa) **ENTÃO** (Urgência é Crítica)
8. **SE** (Impacto é Alto) **E** (Explorabilidade é Moderada) **ENTÃO** (Urgência é Crítica)
9. **SE** (Impacto é Alto) **E** (Explorabilidade é Alta) **ENTÃO** (Urgência é Crítica)

---

## Resultado

```text
RESULTADOS DA SIMULAÇÃO - AVALIAÇÃO DE URGÊNCIA DE INCIDENTES
======================================================================
[Caso Mínimo]  Impacto: 0%   | Explorabilidade: 0.0 -> Urgência: 4.33%
[Caso Médio]   Impacto: 50%  | Explorabilidade: 5.0 -> Urgência: 66.80%
[Caso Máximo]  Impacto: 100% | Explorabilidade: 10.0 -> Urgência: 87.50%
----------------------------------------------------------------------
Status de Execução: OK (9 de 9 regras cobertas sem lacunas)
Saída Gráfica: ![Superfície de Decisão 3D](superficie_decisao.png)
```

---

## Análise Técnica

### 1. Resposta ao "Desafio dos Extremos": Por que o Centroide Triangular não atinge 0% e 100%?
* O método de defuzzificação por **Centroide** calcula o centro de massa geométrico (ponto de equilíbrio) da área agregada gerada pelas regras.
* Ao definir a saída com triângulos nas pontas da escala (como a `Urgência Crítica` variando na borda superior), a figura geométrica possui área distribuída à esquerda do limite $100\%$.
* Como a massa da área ativada "puxa" o centro de gravidade para o interior do gráfico, o valor calculated matematicamente nunca atinge a ponta exata. Na entrada máxima `(100%, 10)`, a massa acumulada estabiliza o centroide em **$87.5\%$**. O mesmo ocorre no extremo inferior `(0%, 0)`, onde o ponto de equilíbrio fica em **$4.33\%$**.

---

### 2. Comparação de Soluções: Abordagem A vs. Abordagem B

#### Abordagem A: Uso de Trapézio (`trapmf`) nas bordas superiores/inferiores
* **Mecanismo:** Substitui-se a função de pertinência triangular nas extremidades (`Urgência Baixa` no início e `Urgência Crítica` no topo) por funções trapezoidais que mantêm pertinência $1.0$ contínua até os limites $0\%$ e $100\%$.
* **Efeito:** Adiciona bloco uniforme de massa geométrica rente às bordas do universo de discurso, deslocando o centroide para bem mais próximo de $0\%$ e $100\%$.
* **Vantagem:** Preserva a resposta contínua e a transição suave de acionamento do motor fuzzy no miolo da escala.

#### Abordagem B: Alteração da Defuzzificação para `MOM` (*Mean of Maximum*)
* **Mecanismo:** O método MOM calcula a média dos pontos numéricos onde o grau de pertinência da área agregada atinge o valor máximo ($1.0$).
*0 **Efeito:** Consegue cravar exatamente **$0\%$** no mínimo e **$100\%$** no máximo.
* **Desvantagem:** Ao descartar a geometria da área e focar apenas no topo do pico de pertinência, o sistema perde a continuidade da saída. A resposta do sistema passa a apresentar "degraus" e saltos abruptos à medida que as entradas variam.

---

### 3. Recomendação de Abordagem

**A Abordagem A (Trapézio + Centroide) é a mais recomendada.**

**Justificativa:** A principal vantagem do controle por Lógica Fuzzy em relação a um sistema On/Off convencional é a **suavidade e proporcionalidade na transição dos dados**. A Abordagem A reduz substancialmente a limitação das bordas sem abrir mão da estabilidade contínua na faixa intermediária. A Abordagem B, apesar de atingir exatamente $100\%$, compromete a estabilidade do sistema ao introduzir respostas discretizadas em saltos.

---

### 4. Análise Interpretativa da Superfície de Decisão 3D

1. **Continuidade da Superfície:** A imagem `superficie_decisao.png` confirma uma superfície contínua sem quebras, degraus indesejados ou regiões nulas. Isso demonstra que as 9 regras cobrem $100\%$ do espaço de estados das entradas.
2. **Proporcionalidade da Resposta:** Nota-se a elevação gradativa do eixo $Z$ (Urgência) conforme o aumento conjunto de $X$ (Impacto) e $Y$ (Explorabilidade), validando a coerência do motor de inferência Mamdani projetado.