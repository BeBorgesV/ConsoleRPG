import batalha
import inimigos
import itens
from jogador import (
    adicionarItemJogador,
    atualizarAtaque,
    criarJogador,
    curarJogador,
    ganharXP,
    getAtaque,
    getInventario,
    getPosicao,
    getVida,
    getXP
)
from mapa import (
    EVENTO_DESCANSO,
    EVENTO_INIMIGO,
    EVENTO_ITEM,
    EVENTO_SAIDA,
    EVENTO_VAZIO,
    criarMapa,
    descreverPosicaoMapa,
    getEventoMapa,
    limparEventoMapa,
    moverJogadorMapa,
    renderizarMapa
)


def _resolverEventoAtual(jogador, mapa):
    codigo_posicao, posicao = getPosicao(jogador)

    if codigo_posicao != 0:
        return codigo_posicao

    x, y = posicao
    codigo_evento, evento = getEventoMapa(mapa, x, y)

    if codigo_evento != 0:
        return codigo_evento

    if evento == EVENTO_VAZIO:
        return 0

    if evento == EVENTO_ITEM:
        codigo_item, item = itens.criarItem("Pocao simples", "cura", 20)

        if codigo_item != 0:
            return codigo_item

        codigo_adicionar = adicionarItemJogador(jogador, item)

        if codigo_adicionar == 0:
            print("  Achado  : Pocao simples adicionada ao inventario.")
            limparEventoMapa(mapa, x, y)
            return 0

        if codigo_adicionar == 1:
            print("  Achado  : ha um item aqui, mas o inventario esta cheio.")
            return 0

        return codigo_adicionar

    if evento == EVENTO_DESCANSO:
        codigo_cura = curarJogador(jogador, 20)

        if codigo_cura == 0:
            print("  Descanso: voce recuperou 20 pontos de vida.")
            limparEventoMapa(mapa, x, y)
            return 0

        if codigo_cura == 1:
            print("  Descanso: sua vida ja esta cheia.")
            return 0

        return codigo_cura

    if evento == EVENTO_INIMIGO:
        codigo_inimigo, inimigo_atual = inimigos.criarInimigo(
            "Sentinela da dungeon",
            35,
            8
        )

        if codigo_inimigo != 0:
            return codigo_inimigo

        codigo_batalha, vencedor = batalha.executarBatalha(jogador, inimigo_atual)

        if codigo_batalha != 0:
            return codigo_batalha

        if vencedor == "jogador":
            ganharXP(jogador, 50)
            atualizarAtaque(jogador)
            limparEventoMapa(mapa, x, y)
            print("  XP      : voce ganhou 50 pontos de experiencia.")

        return 0

    if evento == EVENTO_SAIDA:
        print("  Objetivo: voce entrou na dungeon.")
        print("\nFim de jogo: objetivo concluido!")
        return 3

    return 1

def iniciarJogo(nome):
    if nome is None:
        return 2, None, None

    status, jogador = criarJogador(nome)
    if status != 0:
        return 1, None, None

    status, mapa = criarMapa()
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

COMANDOS_VALIDOS = {
    "cima",
    "baixo",
    "esquerda",
    "direita",
    "w",
    "a",
    "s",
    "d",
    "mover",
    "sair",
    "salvar",
    "salvar e sair",
    "inventario",
    "mapa",
    "1",
    "7"
}

COMANDOS_SAIDA = ["sair", "salvar", "salvar e sair", "7"]

DIRECOES_ATALHO = {
    "w": "cima",
    "s": "baixo",
    "a": "esquerda",
    "d": "direita"
}


def _normalizarDirecao(entrada):
    if entrada is None or not isinstance(entrada, str):
        return None

    entrada = entrada.strip().lower()

    if entrada in DIRECOES_ATALHO:
        return DIRECOES_ATALHO[entrada]

    if entrada in ["cima", "baixo", "esquerda", "direita"]:
        return entrada

    return None


def _normalizarComando(entrada):
    if entrada == "1":
        return "inventario"

    if entrada == "7":
        return "salvar e sair"

    return entrada


def _exibirMiniMapa(jogador, mapa):
    _, posicao = getPosicao(jogador)
    status_mapa, desenho = renderizarMapa(mapa, posicao)

    if status_mapa != 0:
        return status_mapa

    print(desenho)
    return 0


def _processarMovimento(jogador, mapa, direcao):
    status = moverJogadorMapa(mapa, jogador, direcao)

    if status != 0:
        print("Movimento inválido. Tente outra direção.")
        return _exibirMiniMapa(jogador, mapa)

    _, posicao = getPosicao(jogador)
    print(f"  Posição : {posicao}")

    status_descricao, descricao = descreverPosicaoMapa(mapa, posicao[0], posicao[1])
    if status_descricao == 0:
        print(f"  Local   : {descricao['texto']}")

    status_evento = _resolverEventoAtual(jogador, mapa)

    if status_evento != 0:
        return status_evento

    return _exibirMiniMapa(jogador, mapa)

def processarComando(jogador, mapa, comando):
    # CT-P05: parâmetros inválidos
    if jogador is None or mapa is None or comando is None:
        return 2
    if not isinstance(comando, str) or not comando.strip():
        return 2

    # CT-P04: comando inválido
    comando = _normalizarComando(comando.strip().lower())

    direcao = _normalizarDirecao(comando)

    if comando not in COMANDOS_VALIDOS and direcao is None:
        return 1

    # CT-P03: comando válido
    if direcao is not None:
        return _processarMovimento(jogador, mapa, direcao)

    if comando == "mover":
        print("Para onde deseja mover?")
        print("W - Cima")
        print("S - Baixo")
        print("A - Esquerda")
        print("D - Direita")
        direcao = _normalizarDirecao(input("Escolha: "))

        if direcao is None:
            print("Direção inválida.")
            return 0

        return _processarMovimento(jogador, mapa, direcao)

    if comando == "inventario":
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

    elif comando == "mapa":
        return _exibirMiniMapa(jogador, mapa)
    return 0

def loopJogo(jogador, mapa):
    if jogador is None or mapa is None:
        return 2

    # exibe status só no início
    exibirStatus(jogador, mapa)
    _, vida_inicial = getVida(jogador)

    if vida_inicial > 0:
        _exibirMiniMapa(jogador, mapa)

    while True:
        _, vida = getVida(jogador)
        if vida <= 0:
            print("\nVocê morreu. Fim de jogo.")
            return 0

        print("\n" + "-" * 46)
        print("Movimento: W-Cima | S-Baixo | A-Esquerda | D-Direita")
        print("Ações    : 1-Inventário | 7-Sair")

        try:
            comando = _normalizarComando(input("\n> Escolha: ").strip().lower())
        except (EOFError, KeyboardInterrupt):
            print("\nJogo interrompido.")
            return 0

        if comando in COMANDOS_SAIDA:
            print("Encerrando o jogo...")
            return 0

        status = processarComando(jogador, mapa, comando)

        if status == 1:
            print(f"Comando '{comando}' inválido. Tente outro.")
        elif status == 2:
            print("Erro interno ao processar comando.")
            return 1
        elif status == 3:
            return 0

if __name__ == "__main__":
    print("=== ConsoleRPG ===")
    nome = input("Digite seu nome: ")
    status, jogador, mapa = iniciarJogo(nome)
    if status != 0:
        print("Erro ao iniciar jogo!")
    else:
        loopJogo(jogador, mapa)
