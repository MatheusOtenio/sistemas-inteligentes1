def geraGrafo(elementos):
    matriz = []
    for i in range(elementos):
        linhas = [0] * elementos
        matriz.append(linhas)
    return matriz

elementos = int(input("Informe a quantidade de nós do grafo: "))
grafo = geraGrafo(elementos)

while True:
    linha = int(input("Digite o nó de origem (0 para sair): "))
    if linha == 0:
        break
    coluna = int(input("Digite o nó que o vetor aponta: "))
    grafo[linha - 1][coluna - 1] = 1

print("Esquema final do grafo:")
for linha in grafo:
    print(linha)

def tsp(grafo, inicio):
    def busca(atual, visitados, caminho):
        n = len(grafo)
        if len(caminho) == n:
            if grafo[atual][inicio] == 1:
                return caminho + [inicio]
            return None
        for prox in range(n):
            if grafo[atual][prox] == 1 and prox not in visitados:
                resultado = busca(prox, visitados | {prox}, caminho + [prox])
                if resultado:
                    return resultado
        return None
    return busca(inicio, {inicio}, [inicio])

inicio = int(input("Digite o nó inicial: ")) - 1
caminho = tsp(grafo, inicio)

if caminho:
    print("Caminho encontrado:")
    print([x + 1 for x in caminho])
else:
    print("Não existe caminho")