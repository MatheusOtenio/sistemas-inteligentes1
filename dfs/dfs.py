# DFS - Quebra-Cabeça de 8 Peças

# O numero 0 representa o espaco vazio no tabuleiro
# Para testar outros estados, altere apenas os valores abaixo
INICIAL  = [[2, 8, 3],
            [1, 6, 4],
            [7, 0, 5]]

OBJETIVO = [[1, 2, 3],
            [8, 0, 4],
            [7, 6, 5]]

# O DFS sem limite de profundidade pode se perder infinitamente,
# pois ele desce cada vez mais fundo sem garantia de encontrar solucao.
# define o limite em 5 niveis de profundidade.
LIMITE_PROFUNDIDADE = 5

# Limite de seguranca para nao travar em estados muito distantes
LIMITE_ITERACOES = 10000


# -------------------------------------------------------
# FUNCAO 1: contar_inversoes
# -------------------------------------------------------
# Uma "inversao" acontece quando um numero maior aparece
# antes de um numero menor na leitura do tabuleiro.
# Usamos isso para saber se o problema tem solucao ou nao.
def contar_inversoes(estado):
    # Transforma o tabuleiro 3x3 em uma lista simples,
    # ignorando o espaco vazio (0)
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
def is_solvable(inicial, objetivo):
    return contar_inversoes(inicial) % 2 == contar_inversoes(objetivo) % 2


# -------------------------------------------------------
# FUNCAO 3: gerar_filhos
# -------------------------------------------------------
# Gera todos os estados possiveis a partir do estado atual,
# movendo o espaco vazio (0) para cada direcao valida.
def gerar_filhos(estado):
    filhos = []

    # Encontra em qual posicao esta o espaco vazio (0)
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                linha_vazio, col_vazio = i, j

    # Define as 4 direcoes possiveis de movimento:
    # esquerda, cima, direita, baixo
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
# FUNCAO 4: dfs
# -------------------------------------------------------
# Implementacao do DFS conforme o pseudocodigo.
#
# DFS -> filhos entram no INICIO de ABERTOS  (Pilha - LIFO)
#
# Isso faz o DFS sempre processar o filho mais recente primeiro,
# descendo o mais fundo possivel antes de tentar outros caminhos.
#
# Cada estado em ABERTOS guarda tambem sua profundidade,
# para sabermos quando parar de descer.
def dfs(inicial, objetivo):

    # Antes de comecar, verifica se o problema tem solucao
    if not is_solvable(inicial, objetivo):
        print("=" * 45)
        print("           *** FRACASSO ***")
        print("  Este estado inicial nao tem solucao.")
        print("=" * 45)
        return None, 0

    # --- Inicializacao ---
    # Cada elemento de ABERTOS e uma tupla (estado, profundidade).
    # O estado inicial esta no nivel 0 (raiz da arvore).
    # ABERTOS e uma Pilha (LIFO)
    abertos  = [(inicial, 0)]
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
        # pop(0) retira o primeiro elemento — que no DFS e sempre
        # o filho mais recente (topo da pilha)
        x, profundidade = abertos.pop(0)

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

        # So gera filhos se ainda nao atingiu o limite de profundidade.
        # Sem esse limite, o DFS desceria infinitamente pelo mesmo caminho.
        if profundidade < LIMITE_PROFUNDIDADE:

            # Gera todos os estados filhos de X
            filhos = gerar_filhos(x)

            # --- descarta filhos ja visitados ---
            # Evita ciclos: ignora filhos que ja estao em ABERTOS ou FECHADOS
            estados_em_abertos = [estado for estado, _ in abertos]
            filhos_validos = [(f, profundidade + 1) for f in filhos
                              if f not in estados_em_abertos
                              and f not in fechados]

            # --- coloca filhos no INICIO a esquerda de ABERTOS ---
            # DFS: abertos = filhos + abertos    -> filhos vao para o INICIO
            # Isso faz o DFS processar os filhos antes dos estados anteriores,
            # mergulhando fundo em um caminho antes de tentar outro.
            abertos = filhos_validos + abertos

    # --- retorna FALHA se ABERTOS ficou vazio ---
    print("=" * 45)
    print("           *** FRACASSO ***")
    print("  Nenhuma solucao encontrada.")
    print("=" * 45)
    return None, iteracoes


# -------------------------------------------------------
# EXECUCAO
# -------------------------------------------------------
solucao, total_iteracoes = dfs(INICIAL, OBJETIVO)