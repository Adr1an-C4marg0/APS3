
#################################################################################################################################################
#CASO GERAL


from aigyminsper.search.search_algorithms import BuscaLargura,  BuscaProfundidade, BuscaProfundidadeIterativa
from aigyminsper.search.graph import State
import copy
import random


class QueenStateCompleto(State):
    def __init__(self, op, mtx):
        super().__init__(op)
        self.mtx = mtx
        self.tamanho = len(mtx)

    def _contar_conflitos(self):
        #Conta quantos pares de rainhas estão se atacando no tabuleiro 
        conflitos = 0

        # Encontra as posições (linha, coluna) de todas as rainhas
        posicoes = []
        for linha in range(self.tamanho):
            for valor in range(self.tamanho):
                if self.mtx[linha][valor] == 'R':
                    posicoes.append((linha, valor))

        # Compara todos as  rainhas em pares e analisa para ver se estão se atacando (mesma coluna, linha ou diagonal)
        for i in range(len(posicoes)):
            for j in range(i + 1, len(posicoes)):
                linha1, coluna1 = posicoes[i]
                linha2, coluna2 = posicoes[j]

                # Mesma linha ou mesma coluna
                if linha1 == linha2 or coluna1 == coluna2:
                    conflitos += 1
                # diagonal: se |r1 - r2| == |c1 - c2| , pois se a distância entre as linhas for igual a distânica das colunas está na diagonal
                elif abs(linha1 - linha2) == abs(coluna1 - coluna2):
                    conflitos += 1

        return conflitos

    def successors(self):
        """
        para cada linha, tenta mover a rainha para todas as outras colunas possíveis daquela mesma linha.
        """
        successors = []

        for linha in range(self.tamanho):
            # Acha onde a rainha está na linha
            coluna_atual = -1
            for col in range(self.tamanho):
                if self.mtx[linha][col] == 'R':
                    coluna_atual = col
                    break

            # Tenta mover a rainha dessa linha para qualquer outra coluna
            for nova_col in range(self.tamanho):
                if nova_col != coluna_atual:
                    nova_mtx = copy.deepcopy(self.mtx)
                    # Remove da coluna antiga e coloca na nova
                    nova_mtx[linha][coluna_atual] = 0
                    nova_mtx[linha][nova_col] = 'R'

                    desc = f"Mover rainha da linha {linha} para coluna {nova_col}"
                    successors.append(QueenStateCompleto(desc, nova_mtx))

        return successors

    def is_goal(self):
        # A meta é alcançada quando NÃO houver nenhum par de rainhas se atacando
        return self._contar_conflitos() == 0

    def description(self):
        return "N-Rainhas movendo rainhas até zerar os conflitos."

    def cost(self):
        return 1

    def env(self):
        # String única do tabuleiro para evitar repetções na busca
        return str(self.mtx)


def gerar_tabuleiro_inicial_aleatorio(N):
    #Gera um tabuleiro N x N com 1 rainha por linha de forma aleatoria.
    tabuleiro = [[0] * N for _ in range(N)]
    for linha in range(N):
        coluna_aleatoria = random.randint(0, N - 1)
        tabuleiro[linha][coluna_aleatoria] = 'R'
    return tabuleiro


def main():
    
    
    # Para ficar mais facil de utilizar o terminal coloquei essas opções
    
    print("Escolha a busca:")
    print("1 - Largura")
    print("2 - Profundidade")
    print("3 - Profundidade Iterativa")

    while True:
        try:
            escolha = int(input("Digite o número da busca: "))
            if escolha in {1, 2, 3}:
                break
            print("Opção inválida. Digite 1, 2 ou 3.")
        except ValueError:
            print("Valor inválido. Digite apenas números.")

    while True:
        try:
            N = int(input("Digite o valor de N (tamanho do tabuleiro): "))
            if N > 0:
                break
            print("N deve ser maior que 0.")
        except ValueError:
            print("Valor inválido. Digite apenas números inteiros positivos.")

    m = None
    if escolha == 2:
        while True:
            try:
                m = int(input("Digite o valor de m para a busca em profundidade: "))
                if m > 0:
                    break
                print("m deve ser maior que 0.")
            except ValueError:
                print("Valor inválido. Digite apenas números inteiros positivos.")

    if escolha == 1:
        busca = 'largura'
    elif escolha == 2:
        busca = 'profundidade'
    else:
        busca = 'profundidade_iterativa'

    print(f'\nBusca QueenProblem Estado Completo ({N}-Rainhas) usando {busca}')

    tabuleiro_inicial = gerar_tabuleiro_inicial_aleatorio(N)

    print("\nTabuleiro Inicial Aleatório:")
    for linha in tabuleiro_inicial:
        print(linha)

    state = QueenStateCompleto('Estado Inicial Aleatório', tabuleiro_inicial)

    if escolha == 1:
        algorithm = BuscaLargura()
        result = algorithm.search(state, trace=False)
    elif escolha == 2:
        algorithm = BuscaProfundidade()
        result = algorithm.search(state, m=m, trace=False)
    else:
        algorithm = BuscaProfundidadeIterativa()
        result = algorithm.search(state, trace=False)

    if result is not None:
        print('\nAchou solução!')
        print(result.show_path())

        estado_final = result.get_state()
        print("\nTabuleiro Final:")
        for linha in estado_final.mtx:
            print(linha)
    else:
        print('\nNão achou solução')


if __name__ == '__main__':
    main()