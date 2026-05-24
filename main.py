from jogador import *
from mapa import *

def iniciarJogo(nome):
    if nome is None:
        return 2, None, None

    status, jogador = criarJogador(nome)
    if status != 0:
        return 1, None, None

    estrutura = {
        "regioes": ["floresta", "cidade", "dungeon"],
        "tamanho": (10, 10),
        "posicao_inicial": (0, 0)
    }

    status, mapa = criarMapa(estrutura)
    if status != 0:
        return 1, None, None

    jogador["posicao"] = mapa["posicao_inicial"]

    return 0, jogador, mapa

def exibirStatus(jogador, mapa):
    if jogador is None or mapa is None:
        return 1

    # O "_" é usado quando não precisamos do código de status retornado pela função.
    # As funções get retornam uma tupla (status, valor). Exemplo: getVida(jogador) retorna (0, 100)
    # Ao escrever:  _, vida = getVida(jogador)
    # "_" recebe o status (0) e é ignorado, "vida" recebe o valor (100) e é usado
    _, vida = getVida(jogador)
    _, xp = getXP(jogador)
    _, ataque = getAtaque(jogador)
    _, posicao = getPosicao(jogador)
    _, inventario = getInventario(jogador)

    barras = int((vida / jogador["vida_max"]) * 10)
    barra_vida = "█" * barras + "░" * (10 - barras)

    print("=" * 30)
    print(f"  Jogador : {jogador['nome']}")
    print(f"  Vida    : [{barra_vida}] {vida}/{jogador['vida_max']}")
    print(f"  Ataque  : {ataque}")
    print(f"  XP      : {xp}")
    print(f"  Posição : {posicao}")
    print(f"  Inventário: {inventario}")
    print("=" * 30)
    return 0

if __name__ == "__main__":
    print("=== ConsoleRPG ===")
    nome = input("Digite seu nome: ")
    status,jogador,mapa = iniciarJogo(nome)
    print(f"Bem-vindo, {jogador['nome']}!")