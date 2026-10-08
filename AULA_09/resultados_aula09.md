# RELATÓRIO TÉCNICO — AULA DE SISTEMAS INTELIGENTES
## CONTROLE FUZZY DE TEMPERATURA E ROTATIVIDADE DE VENTILADOR

**Data de execução:** 07/10/2026
**Alunos:** Gabriel Orides - 106541 | Davi Kazussuke - 90613

---

## 1. Objetivo

Registrar as análises técnicas, saídas do console e validação do algoritmo de inferência fuzzy desenvolvido em Python. O objetivo do sistema é controlar dinamicamente a velocidade de rotação de um ventilador em resposta a variações na temperatura ambiente.

---

# LABORATÓRIO 01 — CONTROLE NEBULOSO (FUZZY) PARA VELOCIDADE DE VENTILADOR

## Objetivo
Mapear um conjunto de funções de pertinência e regras de inferência fuzzy para calcular proporcionalmente o percentual de acionamento de um ventilador com base na temperatura em graus Celsius (°C).

**Código:** `lab1_aula09.py`

## Resultado

```text
RESULTADOS DA SIMULAÇÃO - CONTROLE FUZZY DE VENTILADOR
==================================================
10°C -> ventilador a 17%
20°C -> ventilador a 44%
25°C -> ventilador a 50%
30°C -> ventilador a 56%
38°C -> ventilador a 83%
--------------------------------------------------
Status de Execução: OK (sem exceções ou erros)
Saída Gráfica:![alt text](image.png)![alt text](image-1.png)
```

## Análise técnica

1. **Comportamento do sistema e suavidade na transição de acionamento:**
   * O algoritmo executou com sucesso o processo de fuzificação, inferência e desfuzificação, garantindo um acionamento contínuo e proporcional.
   * Em temperaturas baixas (10°C), o sistema mantém a rotação em um nível mínimo de 17%.
   * No ponto médio da escala de temperatura (25°C), o ventilador opera exatamente na metade da sua capacidade total (50%).
   * Em cenários de alta temperatura (38°C), a rotação responde de forma adequada elevando a potência para 83%.
   * **Conclusão de desempenho:** Diferente do controle liga/desliga (On/Off) tradicional, a abordagem fuzzy previne picos abruptos de corrente e melhora o conforto térmico ao ajustar a velocidade suavemente.

# LABORATÓRIO 02 — CONTROLE NEBULOSO (FUZZY) PARA CÁLCULO DE GORJETA

## Objetivo
Mapear um conjunto de funções de pertinência triangulares e regras de inferência fuzzy para calcular proporcionalmente o percentual de gorjeta (0% a 25%) em resposta às notas de serviço e comida em uma escala de 0 a 10.

**Código:** `lab2_aula09.py`

## Resultado

```text
RESULTADOS DA SIMULAÇÃO - CONTROLE FUZZY DE GORJETA
==================================================
Nota do serviço (0-10) [7]: 8
Nota da comida (0-10) [3]: 9

=> Gorjeta sugerida: 15.3%
--------------------------------------------------
Status de Execução: OK (sem exceções ou erros)
Saída Gráfica: Visualização dos conjuntos fuzzy e área de defuzzificação gerada
```

## Análise técnica

1. **Mapeamento de Fuzificação e Inferência:**
   * **Serviço (8/10):** Apresenta grau de pertinência de 0.6 no conjunto `"bom"` e 0.4 no conjunto `"medio"`.
   * **Comida (9/10):** Apresenta grau de pertinência de 0.8 no conjunto `"bom"` e 0.2 no conjunto `"medio"`.
   * **Ativação das Regras:**
     * **Regra 2 (`servico["medio"]`):** Ativada com intensidade 0.4, truncando o conjunto de gorjeta `"media"`.
     * **Regra 3 (`servico["bom"] | comida["bom"]`):** Ativada com intensidade $\max(0.6, 0.8) = 0.8$, truncando o conjunto de gorjeta `"alta"`.

2. **Desfuzificação pelo Método do Centroide:**
   * A saída agregada combina a área da gorjeta `"media"` (altura 0.4) com a área da gorjeta `"alta"` (altura 0.8).
   * O resultado obtido de **15.3%** reflete o centro de gravidade dessa superfície agregada. A presença de pertinência (0.4) no termo `"medio"` puxa o resultado para a região central da escala, impedindo que a gorjeta atinja o limite máximo (25%).

3. **Validação dos Experimentos Propostos:**
   * **Alteração da Regra 2 (`servico["medio"] & comida["medio"]`):** Ao substituir a regra por um operador lógico **E**, exige-se que ambos os critérios sejam médios simultaneamente. Para entradas como `(7, 3)`, a regra média passa a ser ativada por $\min(0.6, 0.6) = 0.6$, ajustando o equilíbrio da superfície agregada.
   * **Funções de Pertinência Gaussianas (`fuzz.gaussmf`):** Substituir as funções triangulares por gaussianas elimina a descontinuidade nos vértices e gera transições de resposta mais suaves ao longo de todo o universo de discurso.
   * **Métodos de Defuzzificação:**
     * `centroid`: Garante continuidade e estabilidade na saída.
     * `mom`: Produz saltos discretos na gorjeta ao considerar apenas os pontos de pertinência máxima, desconsiderando a ponderação das áreas.
     * `bisector`: Divide a área agregada em duas regiões de superfície idênticas.
   * **Adição do Termo `"excelente"`:** Permite isolar avaliações no topo da escala (9–10), permitindo que cenários de alta satisfação alcancem valores de gorjeta próximos do teto de 25%.
   * **Análise dos Casos Limite:**
     * **`(0, 0)`:** Ativação exclusiva da gorjeta baixa, resultando na gorjeta mínima (~4.3%).
     * **`(5, 5)`:** Ponto neutro com pico de pertinência no termo médio, resultando em gorjeta central (~12.5%).
     * **`(10, 10)`:** Ativação máxima da gorjeta alta (~20.6%).

# LABORATÓRIO 03 — CONTROLE NEBULOSO (FUZZY) PARA INTENSIDADE DE TREINO

## Objetivo (Etapa 1: Definição do Problema)
O problema consiste em determinar a intensidade ideal de um treino físico diário. Hoje, essa decisão costuma ser tomada de forma empírica ou intuitiva pelo próprio atleta ou treinador. As entradas são numéricas: horas de sono na noite anterior (0 a 12 horas) e Frequência Cardíaca (FC) de repouso ao acordar (40 a 100 bpm). A saída é a intensidade sugerida para o treino, variando de 0% a 100%. A lógica fuzzy é adequada porque conceitos como "dormir pouco" ou "frequência alta" são vagos e não possuem limites exatos. O modelo proporciona uma transição suave na decisão, permitindo ajustar o treino em dias de fadiga moderada e evitando categorizações extremas do tipo "tudo ou nada".

**Código:** `lab03_aula09.py`

## Modelagem e Regras (Etapa 2)

**Universo de Discurso e Funções de Pertinência:**
* **Sono (Entrada 1):** Unidade em horas (0 a 12). Termos linguísticos: `ruim`, `medio`, `bom` (forma geométrica: triângulos).
* **FC de Repouso (Entrada 2):** Unidade em bpm (40 a 100). Termos linguísticos: `baixa`, `media`, `alta` (forma geométrica: triângulos).
* **Intensidade (Saída):** Unidade em percentual (0 a 100). Termos linguísticos: `leve`, `moderado`, `intenso` (forma geométrica: triângulos).

<img width="599" height="415" alt="image" src="https://github.com/user-attachments/assets/7ae05bb5-17da-4032-beb4-e1601ff61211" />
<img width="597" height="445" alt="image" src="https://github.com/user-attachments/assets/f40aa97d-5f45-4092-8668-dafef420e187" />
<img width="599" height="440" alt="image" src="https://github.com/user-attachments/assets/38e347c4-8610-4227-bcd6-531575759c88" />



**Base de Regras:**[cite: 3]
1. **SE** (Sono é Ruim) **OU** (FC é Alta) **ENTÃO** (Intensidade é Leve)
2. **SE** (Sono é Ruim) **E** (FC é Baixa) **ENTÃO** (Intensidade é Moderado)
3. **SE** (Sono é Médio) **E** (FC é Média) **ENTÃO** (Intensidade é Moderado)
4. **SE** (Sono é Médio) **E** (FC é Baixa) **ENTÃO** (Intensidade é Intenso)
5. **SE** (Sono é Bom) **E** (FC é Baixa **OU** FC é Média) **ENTÃO** (Intensidade é Intenso)
6. **SE** (Sono é Bom) **E** (FC é Alta) **ENTÃO** (Intensidade é Moderado)

## Resultado (Etapa 4: Testes)

```text
=== RESULTADOS DA AVALIAÇÃO FUZZY ===
Teste 1: Sono = 3h | FC = 90 bpm
 -> Saída do sistema: 18.6% (Esperado: Leve)

Teste 2: Sono = 7h | FC = 65 bpm
 -> Saída do sistema: 60.0% (Esperado: Moderado)

Teste 3: Sono = 9h | FC = 45 bpm
 -> Saída do sistema: 87.7% (Esperado: Intenso)

Teste 4: Sono = 8h | FC = 80 bpm
 -> Saída do sistema: 52.3% (Esperado: Moderado)
--------------------------------------------------
Status de Execução: OK (sem exceções ou erros)
Saída Gráfica: Visualização dos conjuntos fuzzy e área de defuzzificação gerada.
