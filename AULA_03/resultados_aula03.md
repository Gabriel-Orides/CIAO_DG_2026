# Laboratórios de Algoritmos Genéticos

Este repositório reúne três atividades práticas focadas no funcionamento, ajuste de hiperparâmetros e aplicação de **Algoritmos Genéticos (AG)** em diferentes tipos de problemas.

## Conteúdo

- [Lab 01 — Impacto dos Parâmetros no Espaço de Busca](#lab-01--impacto-dos-parâmetros-no-espaço-de-busca)
- [Lab 02 — Problema OneMax e Comportamento da População](#lab-02--problema-onemax-e-comportamento-da-população)
- [Lab 03 — Otimização Contínua de Função Matemática](#lab-03--otimização-contínua-de-função-matemática)

---

## Lab 01 — Impacto dos Parâmetros no Espaço de Busca

### Objetivo

Analisar como a alteração na quantidade de bits (tamanho do cromossomo) e na taxa de mutação afeta o desempenho e a convergência do algoritmo ao tentar maximizar uma função simples.

### Resultados e Análise

Ao comparar a versão original do código com a modificada, observamos impactos diretos no comportamento da população:

* **Espaço de busca:** A redução de 5 para 3 bits limitou drasticamente o espaço de busca, restringindo o valor máximo a 7. Isso acabou gerando um "falso erro" no relatório final, já que o algoritmo alcançou o limite do seu espaço, mas a referência estava configurada para o ambiente anterior.
* **Estabilidade e Mutação:** O maior contraste ocorreu na taxa de mutação. O uso de 60% no código modificado causou forte instabilidade e impediu a população de estabilizar.
* **Convergência ideal:** O código original obteve sucesso ao usar 5 bits e uma mutação equilibrada de 10%. Isso permitiu uma evolução saudável, onde todos os indivíduos convergiram perfeitamente para o ótimo global (31).

---

## Lab 02 — Problema OneMax e Comportamento da População

### Objetivo

Resolver o problema OneMax (que consiste em maximizar a quantidade de bits `1` no cromossomo) e testar como as mudanças drásticas nos hiperparâmetros afetam a busca do AG pela solução.

### Observações dos Cenários Testados

#### 1. Aumentar a taxa de mutação para 0.1
O gráfico de fitness passa a oscilar muito mais, dificultando que o algoritmo mantenha o resultado ótimo. Uma mutação de 10% é considerada altíssima para esse escopo. O excesso de aleatoriedade acaba transformando a evolução em uma busca cega, destruindo bons genes.

#### 2. Diminuir a população para 10
O algoritmo converge muito rápido, mas corre um grande risco de estacionar em um ótimo local. Isso acontece porque uma população pequena tem pouca diversidade genética. Nesses casos, dar um tempo extra (mais gerações) pode ser a salvação para o algoritmo tentar encontrar a convergência.

#### 3. Aumentar as gerações para 100
A linha do gráfico simplesmente se estende mais para a direita. Se o algoritmo já estava alcançando a pontuação máxima (20/20) na geração 30 ou 40, o restante das gerações será apenas uma reta plana, indicando tempo de processamento excedente.

#### 4. Mudar a taxa de elite para 0
Ao remover o elitismo, a curva de melhor resultado no gráfico deixa de ser uma subida constante e segura. Ela passa a apresentar quedas (vales) de uma geração para a outra, já que os melhores indivíduos não têm mais passagem garantida e podem ser arruinados pelo cruzamento ou mutação.

---

## Lab 03 — Otimização Contínua de Função Matemática

### Objetivo

Completar as funções vitais de um Algoritmo Genético para encontrar o valor de $x$ no intervalo de 0 a 10 que maximiza a função $f(x) = x \cdot \sin(3x)$. O desafio extra é lidar com mapeamento de variáveis reais e ajustes em funções que geram valores negativos.

### Código Completo das Funções Adaptadas

```python
import random

# TODO 1: Converter bits para x real
def bits_para_x(bits):
    """
    Converte lista de 8 bits para valor real no intervalo [X_MIN, X_MAX].
    """
    # 1. Transformamos a lista de bits em uma string e depois em um inteiro decimal
    # Ex: [1, 1, 1, 1, 1, 1, 1, 1] vira 255
    string_bits = "".join(str(b) for b in bits)
    decimal = int(string_bits, 2)
    
    # 2. Normalizamos para o intervalo [X_MIN, X_MAX]
    # O valor máximo para 8 bits é 255 (2^8 - 1)
    max_decimal = (2 ** BITS) - 1
    
    x = X_MIN + (decimal / max_decimal) * (X_MAX - X_MIN)
    return x

# TODO 2: Calcular fitness (nota) de um indivíduo
def fitness(individuo):
    """
    Calcula o fitness de um indivíduo.
    """
    x = bits_para_x(individuo)
    valor_fx = funcao_objetivo(x)
    
    # TRUQUE IMPORTANTE:
    # A função x * sin(3x) pode retornar valores negativos.
    # O método da roleta falha se houver fitness negativo, pois as probabilidades 
    # não fariam sentido. O menor valor possível de f(x) nesse intervalo é aprox -9.
    # Portanto, somamos 15 para garantir que o fitness seja sempre positivo!
    return valor_fx + 15

# TODO 3: Mutação bit-flip
def mutacao(individuo):
    """
    Aplica mutação bit-flip.
    """
    for i in range(len(individuo)):
        # Gera um número entre 0 e 1. Se for menor que a taxa, inverte o bit.
        if random.random() < TAXA_MUT:
            individuo[i] = 1 - individuo[i]
            
    return individuo
