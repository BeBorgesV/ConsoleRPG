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

    barras = int((vida / jogador["vida_max"]) * 10)
    barra_vida = "█" * barras + "░" * (10 - barras)

    print("=" * 30)
    print(f"  Jogador : {jogador['nome']}")
    print(f"  Vida    : [{barra_vida}] {vida}/{jogador['vida_max']}")
    print(f"  Ataque  : {ataque}")
    print(f"  XP      : {xp}")
    print(f"  Posição : {posicao}")
    print("=" * 30)
    return 0

COMANDOS_VALIDOS = {"mover", "atacar", "defender", "sair", "inventario"}

def processarComando(jogador, mapa, comando):
    # CT-P05: parâmetros inválidos
    if jogador is None or mapa is None or comando is None:
        return 2
    if not isinstance(comando, str) or not comando.strip():
        return 2

    # CT-P04: comando inválido
    if comando.strip().lower() not in COMANDOS_VALIDOS:
        return 1

    # CT-P03: comando válido
    if comando == "mover":
        print("Para onde deseja mover?")
        print("1 - Cima")
        print("2 - Baixo")
        print("3 - Esquerda")
        print("4 - Direita")
        direcao = input("Escolha: ").strip()

        if direcao == "1":
            status = moverJogador(jogador, 0, -1)
        elif direcao == "2":
            status = moverJogador(jogador, 0, 1)
        elif direcao == "3":
            status = moverJogador(jogador, -1, 0)
        elif direcao == "4":
            status = moverJogador(jogador, 1, 0)
        else:
            print("Direção inválida.")
            return 1

        if status != 0:
            return 1

        _, posicao = getPosicao(jogador)
        print(f"  Posição : {posicao}")

    elif comando == "atacar":
        print("Você atacou!")
        _, ataque = getAtaque(jogador)
        _, vida = getVida(jogador)
        print(f"  Ataque : {ataque}")
        print(f"  Vida   : {vida}/{jogador['vida_max']}")

    elif comando == "defender":
        print("Você se defendeu!")
        _, vida = getVida(jogador)
        _, xp = getXP(jogador)
        print(f"  Vida : {vida}/{jogador['vida_max']}")
        print(f"  XP   : {xp}")

    elif comando == "inventario":
        _, vida = getVida(jogador)
        _, xp = getXP(jogador)
        _, ataque = getAtaque(jogador)
        _, posicao = getPosicao(jogador)
        _, inventario = getInventario(jogador)
        print("=" * 30)
        print(f"  Jogador : {jogador['nome']}")
        print(f"  Vida    : {vida}/{jogador['vida_max']}")
        print(f"  Ataque  : {ataque}")
        print(f"  XP      : {xp}")
        print(f"  Posição : {posicao}")
        print(f"  Inventário: {inventario if inventario else 'vazio'}")
        print("=" * 30)
    return 0

def loopJogo(jogador, mapa):
    if jogador is None or mapa is None:
        return 2

    # exibe status só no início
    exibirStatus(jogador, mapa)

    while True:
        _, vida = getVida(jogador)
        if vida <= 0:
            print("\nVocê morreu. Fim de jogo.")
            return 0

        print("\nComandos: mover, atacar, defender, inventario, sair")

        try:
            comando = input("\n> Digite um comando: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nJogo interrompido.")
            return 0

        if comando == "sair":
            print("Encerrando o jogo...")
            return 0

        status = processarComando(jogador, mapa, comando)

        if status == 1:
            print(f"Comando '{comando}' inválido. Tente outro.")
        elif status == 2:
            print("Erro interno ao processar comando.")
            return 1

if __name__ == "__main__":
    print("=== ConsoleRPG ===")
    nome = input("Digite seu nome: ")
    status, jogador, mapa = iniciarJogo(nome)
    if status != 0:
        print("Erro ao iniciar jogo!")
    else:
        loopJogo(jogador, mapa)