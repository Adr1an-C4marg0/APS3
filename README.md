# Resolução do Problema das N-Rainhas por Buscas

---

## Nomes: Adrian Aparecido da Silva Camargo e Rafael Santos Pereira

---

Este projeto implementa a solução para o clássico **Problema das $N$-Rainhas** utilizando a biblioteca `aigyminsper`. 

A abordagem utilizada é a de **Espaço de Estados**, na qual o tabuleiro inicia com todas as $N$ rainhas posicionadas (uma por linha, em colunas sorteadas) e os sucessores realizam movimentos locais (alterando a coluna de uma rainha por vez) até zerar todos os conflitos de ataque em linhas, colunas e diagonais.

---

## 📊 Tabela Comparativa dos Resultados ($N = 4, 5, 6, 7, 8$)

Os testes a seguir consideraram execuções com o mesmo tabuleiro inicial aleatório (para gerar um padrão na análise).

| $N$ | Conflitos Iniciais | Busca em Largura (BFS) | Busca em Profundidade (DFS, $m=10$) | Profundidade Iterativa (IDDFS) |
|:---:|:------------------:|:----------------------:|:----------------------------------:|:------------------------------:|
| **4** | 3 | 🟢 **Sucesso** (~0.003s) | 🟢 **Sucesso** (~0.005s) | 🟢 **Sucesso** (~0.001s) |
| **5** | 4 | 🟢 **Sucesso** (~0.018s) | 🟢 **Sucesso** (~0.005s) | 🟢 **Sucesso** (~0.002s) |
| **6** | 4 | 🟢 **Sucesso** (~2.68s) | 🟢 **Sucesso** (~1.55s)* | 🟢 **Sucesso** (~0.15s) |
| **7** | 5 | 🔴 **Timeout / Memória** | 🔴 **Timeout / Ramo Infinitamente Profundo** | 🟢 **Sucesso** (~2.20s) |
| **8** | 6 | 🔴 **Timeout / Memória** | 🔴 **Timeout / Ramo Infinitamente Profundo** | 🟢 **Sucesso** (~41.67s) |

*\*Para o DFS com $N=6$, utilizou-se limite de profundidade $m=15$.*

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
