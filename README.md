# README: Resolução do Problema das N-Rainhas via Busca em Espaço de Estados Completos

Este projeto implementa a solução para o clássico **Problema das $N$-Rainhas** utilizando a biblioteca `aigyminsper`. 

A abordagem utilizada é a de **Espaço de Estados Completos**, na qual o tabuleiro inicia com todas as $N$ rainhas posicionadas (uma por linha, em colunas sorteadas) e os sucessores realizam movimentos locais (alterando a coluna de uma rainha por vez) até zerar todos os conflitos de ataque em linhas, colunas e diagonais.

---

## 🛠️ Modelagem (`QueenStateCompleto`)

- **Representação do Estado:** Matriz $N \times N$ com exatamente 1 rainha (`'R'`) por linha.
- **Fator de Ramificação ($b$):** Cada estado possui $N \times (N - 1)$ sucessores (para cada uma das $N$ linhas, a rainha pode se mover para $N - 1$ colunas restantes).
- **Função de Conflitos (`_contar_conflitos`):** Conta quantos pares de rainhas compartilham a mesma linha, coluna ou diagonal ($|r_1 - r_2| == |c_1 - c_2|$).
- **Condição de Meta (`is_goal`):** Retorna `True` quando `_contar_conflitos() == 0`.
- **Identificação Única (`env`):** Retorna `str(self.mtx)` para catalogação de nós abertos/fechados no grafo de busca.

---

## 📊 Tabela Comparativa dos Resultados ($N = 4, 5, 6, 7, 8$)

Os testes a seguir consideraram execuções com o mesmo tabuleiro inicial aleatório (para fins de padronização dos benchmarks).

| $N$ | Conflitos Iniciais | Busca em Largura (BFS) | Busca em Profundidade (DFS, $m=10$) | Profundidade Iterativa (IDDFS) | Algoritmo Vencedor |
|:---:|:------------------:|:----------------------:|:----------------------------------:|:------------------------------:|:------------------:|
| **4** | 3 | 🟢 **Sucesso** (~0.003s) | 🟢 **Sucesso** (~0.005s) | 🟢 **Sucesso** (~0.001s) | **IDDFS / BFS** |
| **5** | 4 | 🟢 **Sucesso** (~0.018s) | 🟢 **Sucesso** (~0.005s) | 🟢 **Sucesso** (~0.002s) | **IDDFS** |
| **6** | 4 | 🟢 **Sucesso** (~2.68s) | 🟢 **Sucesso** (~1.55s)* | 🟢 **Sucesso** (~0.15s) | **IDDFS** |
| **7** | 5 | 🔴 **Timeout / Memória** | 🔴 **Timeout / Ramo Infinitamente Profundo** | 🟢 **Sucesso** (~2.20s) | **IDDFS** |
| **8** | 6 | 🔴 **Timeout / Memória** | 🔴 **Timeout / Ramo Infinitamente Profundo** | 🟢 **Sucesso** (~41.67s) | **IDDFS** |

*\*Para o DFS com $N=6$, utilizou-se limite de profundidade $m=15$.*

---

## 🔍 Análise Detalhada por Tamanho de Tabuleiro ($N$)

### 🔹 $N = 4$ e $N = 5$ (Instâncias Pequenas)
- **Fator de ramificação:** $b = 12$ ($N=4$) e $b = 20$ ($N=5$).
- **Desempenho:** Todos os três algoritmos encontram a solução quase instantaneamente (menos de 0.02 segundos).
- **Motivo:** A árvore de busca é rasa e o número total de estados possíveis é pequeno ($4^4 = 256$ estados para $N=4$ e $5^5 = 3.125$ estados para $N=5$).

### 🔹 $N = 6$ (Instância Intermediária)
- **Fator de ramificação:** $b = 30$ ($6 \times 5$).
- **BFS (Largura):** Encontra a solução em ~2.68s, mas precisa armazenar milhares de nós na memória.
- **DFS (Profundidade):** Depende muito do valor do limite de profundidade $m$. Com $m=15$, encontrou a solução em ~1.55s.
- **IDDFS:** **Destaque da execução!** Encontra a solução mais rasa em apenas **0.15s**, pois combina o baixo consumo de memória com a busca em nível por nível.

### 🔹 $N = 7$ e $N = 8$ (Instâncias Grandes)
- **Fator de ramificação:** $b = 42$ ($N=7$) e $b = 56$ ($N=8$).
- **BFS (Largura):** **Estoura memória / Timeout.** Com $b=56$, a busca em largura no nível 3 gera mais de $56^3 \approx 175.000$ nós. O consumo de memória RAM cresce exponencialmente ($O(b^d)$).
- **DFS (Profundidade):** **Entra em caminhos profundos não-ótimos (Timeout).** Sem uma heurística para guiar, a busca em profundidade perde tempo explorando caminhos longos com muitos conflitos antes de fazer o *backtracking*.
- **IDDFS (Profundidade Iterativa):** **Consegue resolver!** Resolve $N=7$ em **~2.20s** e $N=8$ em **~41.67s**. Como incrementa o limite de profundidade de 1 em 1 ($0, 1, 2, 3...$), garante encontrar o caminho mais curto até a solução sem o custo de memória da BFS.

---

## 💡 Conclusões Teóricas e Práticas

1. **Por que a busca em espaço de estados completos sofre com $N \ge 7$?**
   - Como estamos usando algoritmos de **busca não informada** (cega), a busca explora os movimentos sem saber qual movimento reduz mais o número de conflitos.
   - O fator de ramificação $b = N(N-1)$ causa uma **explosão combinatória** acelerada à medida que $N$ aumenta.

2. **Comparativo entre as buscas:**
   - **Busca em Largura (BFS):** Garante o caminho mais curto, mas inviabilizada pelo consumo de memória $O(b^d)$.
   - **Busca em Profundidade (DFS):** Consumo de memória baixo $O(b \cdot m)$, porém ineficiente quando a árvore é profunda e sem informação visual de proximidade da meta.
   - **Busca em Profundidade Iterativa (IDDFS):** **A melhor escolha entre as buscas cegas.** Combina a garantia de otimidade em profundidade da BFS com o consumo eficiente de memória da DFS ($O(b \cdot d)$).

---

## 🚀 Como Executar

1. Certifique-se de ter o Python 3 instalado e a biblioteca `aigyminsper`:
   ```bash
   pip install aigyminsper
   ```

2. Execute o arquivo do projeto:
   ```bash
   python main.py
   ```

3. Responda aos prompts interativos no terminal:
   - Escolha o algoritmo de busca (1 - Largura, 2 - Profundidade, 3 - Profundidade Iterativa).
   - Digite o valor de $N$ (ex: 4, 5, 6, 7 ou 8).
