# BFS - Quebra-Cabeça de 8 Peças

# O numero 0 representa o espaco vazio no tabuleiro
# Para testar outros estados, altere apenas os valores abaixo
INICIAL  = [[2, 8, 3],
            [1, 6, 4],
            [7, 0, 5]]

OBJETIVO = [[1, 2, 3],
            [8, 0, 4],
            [7, 6, 5]]

# Limite de seguranca para nao travar em estados muito distantes
LIMITE_ITERACOES = 10000


# -------------------------------------------------------
# FUNCAO 1: contar_inversoes
# -------------------------------------------------------
# Uma "inversao" acontece quando um numero maior aparece
# antes de um numero menor na leitura do tabuleiro.
# Ex: na sequencia [2, 8, 3], o 8 antes do 3 e uma inversao.
# Usamos isso para saber se o problema tem solucao ou nao.
def contar_inversoes(estado):
    # Transforma o tabuleiro 3x3 em uma lista simples,
    # ignorando o espaco vazio (0)
    # Ex: [[2,8,3],[1,6,4],[7,0,5]] -> [2,8,3,1,6,4,7,5]
    flat = [n for linha in estado for n in linha if n != 0]

    inversoes = 0

    # Compara cada par de numeros: se o da esquerda for maior,
    # e uma inversao
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversoes += 1

    return inversoes


# -------------------------------------------------------
# FUNCAO 2: is_solvable
# -------------------------------------------------------
# Verifica se o estado inicial consegue chegar ao objetivo.
# A regra e: os dois estados precisam ter a mesma paridade
# de inversoes (ambos pares OU ambos impares).
# Se forem diferentes, e matematicamente impossivel resolver.
# Isso evita que o BFS fique rodando infinitamente.
def is_solvable(inicial, objetivo):
    return contar_inversoes(inicial) % 2 == contar_inversoes(objetivo) % 2


# -------------------------------------------------------
# FUNCAO 3: gerar_filhos
# -------------------------------------------------------
# Gera todos os estados possiveis a partir do estado atual,
# movendo o espaco vazio (0) para cada direcao valida.
# Cada movimento e um "filho" do estado atual.
def gerar_filhos(estado):
    filhos = []

    # Encontra em qual posicao esta o espaco vazio (0)
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                linha_vazio, col_vazio = i, j

    # Define as 4 direcoes possiveis de movimento:
    # esquerda, cima, direita, baixo
    # Cada tupla representa (variacao_linha, variacao_coluna)
    movimentos = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    for dl, dc in movimentos:
        nova_linha = linha_vazio + dl
        nova_col   = col_vazio  + dc

        # Verifica se o movimento nao sai fora do tabuleiro 3x3
        if 0 <= nova_linha < 3 and 0 <= nova_col < 3:

            # Cria uma copia do estado atual para nao modificar o original
            novo_estado = [linha[:] for linha in estado]

            # Troca o espaco vazio com a peca vizinha
            novo_estado[linha_vazio][col_vazio] = novo_estado[nova_linha][nova_col]
            novo_estado[nova_linha][nova_col]   = 0

            filhos.append(novo_estado)

    return filhos


# -------------------------------------------------------
# FUNCAO 4: bfs
# -------------------------------------------------------
# Implementacao do BFS conforme o pseudocodigo.
# ABERTOS e uma Fila (FIFO): novos estados entram no final
# e sao processados do inicio -> explora nivel por nivel.
def bfs(inicial, objetivo):

    # Antes de comecar, verifica se o problema tem solucao
    if not is_solvable(inicial, objetivo):
        print("=" * 45)
        print("           *** FRACASSO ***")
        print("  Este estado inicial nao tem solucao.")
        print("=" * 45)
        return None, 0

    # --- Inicializacao ---
    # ABERTOS comeca com o estado inicial (e uma Fila)
    abertos  = [inicial]
    # FECHADOS comeca vazio
    fechados = []

    iteracoes = 0

    # --- Loop principal ---
    # Continua enquanto ainda houver estados para explorar
    while abertos:
        iteracoes += 1

        # Seguranca: para se atingir o limite de iteracoes
        if iteracoes > LIMITE_ITERACOES:
            print("=" * 45)
            print("           *** FRACASSO ***")
            print(f"  Limite de {LIMITE_ITERACOES} iteracoes atingido.")
            print("=" * 45)
            return None, iteracoes

        # --- remove o estado mais a esquerda de ABERTOS ---
        # pop(0) retira o primeiro elemento da lista (comportamento de Fila)
        x = abertos.pop(0)

        # --- verifica se X e o objetivo ---
        if x == objetivo:
            print("=" * 45)
            print("            *** SUCESSO ***")
            print(f"  Solucao encontrada em {iteracoes} iteracoes.")
            print("=" * 45)
            return x, iteracoes

        # --- senao, processa X ---

        # Coloca X em FECHADOS (ja foi examinado)
        fechados.append(x)

        # Gera todos os estados filhos de X
        filhos = gerar_filhos(x)

        # --- descarta filhos ja visitados ---
        # Evita ciclos: se o filho ja esta em ABERTOS ou FECHADOS,
        # ele ja foi ou sera processado, entao ignoramos
        filhos_validos = [f for f in filhos if f not in abertos and f not in fechados]

        # --- coloca filhos no final a direita de ABERTOS ---
        # Isso e o que faz o BFS ser uma Fila (FIFO):
        # os filhos entram no final e serao processados por ultimo,
        # garantindo que exploramos todo o nivel atual antes de descer
        abertos.extend(filhos_validos)

    # --- retorna FALHA se ABERTOS ficou vazio ---
    print("=" * 45)
    print("           *** FRACASSO ***")
    print("  Nenhuma solucao encontrada.")
    print("=" * 45)
    return None, iteracoes


# -------------------------------------------------------
# EXECUCAO
# -------------------------------------------------------
solucao, total_iteracoes = bfs(INICIAL, OBJETIVO)