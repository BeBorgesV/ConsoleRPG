import batalha
import inimigos
import itens
from jogador import (
    adicionarItemJogador,
    atualizarAtaque,
    criarJogador as _criarJogador,
    ganharXP,
    getAtaque,
    getInventario,
    getVida,
    getXP,
    usarItemJogador
)
from mapa import (
    alocarInimigoMapa,
    alocarItemMapa,
    criarMapa,
    descreverPosicaoMapa,
    getInimigoMapa,
    getItemMapa,
    getPosicaoInicialMapa,
    inimigoFinalMapa,
    limparEventoMapa,
    moverJogadorMapa,
    registrarInimigoDerrotadoMapa,
    renderizarMapa
)


ITENS_INICIAIS = [
    ((2, 12), "Pocao simples", "cura", 25),
    ((5, 13), "Amuleto de ataque", "ataque", 5),
    ((1, 10), "Chave da clareira", "chave", 1),
    ((8, 5), "Chave da ponte", "chave", 1),
    ((11, 6), "Pocao forte", "cura", 35)
]

INIMIGOS_INICIAIS = [
    ((5, 11), "Lobo da trilha", 35, 7, False),
    ((9, 9), "Bandido do bosque", 45, 9, False),
    ((12, 7), "Guarda do castelo", 55, 11, False),
    ((13, 2), "Chefe do castelo", 75, 13, True)
]

DIRECOES = ["cima", "baixo", "esquerda", "direita"]
COMANDOS_SAIDA = ["salvar e sair", "5"]
ATALHOS = {
    "w": "cima",
    "s": "baixo",
    "a": "esquerda",
    "d": "direita",
    "1": "inventario",
    "2": "mapa",
    "5": "salvar e sair"
}


def criarJogador(nome):
    resultado = _criarJogador(nome)

    if isinstance(resultado, dict):
        return 0, resultado

    return resultado, None


def _nomeJogador(jogador):
    if isinstance(jogador, dict):
        return jogador.get("nome")

    return jogador


def _posicaoJogador(jogador):
    if not isinstance(jogador, dict):
        return 2, None

    if "posicao" not in jogador:
        return 1, None

    return 0, jogador["posicao"]


def _obterDadosItem(id_item):
    if not itens.verificaIdItemValido(id_item):
        return None
    estado = itens.exportarEstadoItens()
    if id_item >= len(estado):
        return None
    return estado[id_item].copy()


def _contarChaves(jogador):
    codigo, inventario = getInventario(_nomeJogador(jogador))

    if codigo != 0:
        return 0

    total = 0

    for item in inventario:
        if itens.itemEhChave(item):
            total += 1

    return total


def _garantirPosicaoJogador(jogador, mapa):
    if not isinstance(jogador, dict) or mapa is None:
        return 2

    if "posicao" in jogador:
        return 0

    status, posicao = getPosicaoInicialMapa(mapa)

    if status == 0:
        jogador["posicao"] = posicao

    return status


def _prepararEntidades(mapa):
    if itens.restaurarEstadoItens([]) != 0:
        return 1

    for posicao, nome, tipo, valor in ITENS_INICIAIS:
        status, id_item = itens.criarItem(nome, tipo, valor)

        if status != 0 or not itens.verificaIdItemValido(id_item):
            return 1

        if alocarItemMapa(mapa, posicao[0], posicao[1], id_item) != 0:
            return 1

    if inimigos.restaurarEstadoInimigos([]) != 0:
        return 1

    for posicao, nome, vida, ataque, final in INIMIGOS_INICIAIS:
        status, id_inimigo = inimigos.criarInimigo(nome, vida, ataque)

        if status != 0 or not inimigos.verificaIdInimigoValido(id_inimigo):
            return 1

        if alocarInimigoMapa(mapa, posicao[0], posicao[1], id_inimigo, final) != 0:
            return 1

    return 0


def _resolverEventoAtual(jogador, mapa):
    nome = _nomeJogador(jogador)
    status, posicao = _posicaoJogador(jogador)

    if status != 0:
        return status

    x, y = posicao
    status_item, id_item = getItemMapa(mapa, x, y)

    if status_item == 0:
        item = _obterDadosItem(id_item)

        if item is None:
            return 1

        status_adicionar = adicionarItemJogador(nome, item)

        if status_adicionar == 0:
            if itens.itemEhChave(item):
                print(f"  Chave   : {item['nome']} obtida ({_contarChaves(jogador)}/2).")
            else:
                print(f"  Achado  : {item['nome']} adicionado ao inventario.")

            limparEventoMapa(mapa, x, y)
            return 0

        if status_adicionar == 1:
            print("  Achado  : ha um item aqui, mas o inventario esta cheio.")
            return 0

        return status_adicionar

    status_inimigo, id_inimigo = getInimigoMapa(mapa, x, y)

    if status_inimigo != 0:
        return 2 if status_item == 2 or status_inimigo == 2 else 0

    if not inimigos.verificaIdInimigoValido(id_inimigo):
        return 1

    status_final, chefe = inimigoFinalMapa(mapa, x, y)

    if status_final != 0:
        return status_final

    if chefe:
        print("  Alerta  : voce encontrou o chefe da torre.")

    status_batalha, vencedor = batalha.executarBatalha(jogador, id_inimigo)

    if status_batalha != 0:
        return status_batalha

    if vencedor != "jogador":
        return 0

    xp = 120 if chefe else 50
    registrarInimigoDerrotadoMapa(mapa, x, y)
    ganharXP(nome, xp)
    atualizarAtaque(nome)
    print(f"  XP      : voce ganhou {xp} pontos de experiencia.")

    if chefe:
        print("  Objetivo: chefe derrotado.")
        print("\nFim de jogo: voce atravessou o bosque e venceu o chefe do castelo!")
        return 3

    return 0


def iniciarJogo(nome):
    if nome is None:
        return 2, None, None

    status, jogador = criarJogador(nome)

    if status != 0 or jogador is None:
        return 1, None, None

    status, mapa = criarMapa()

    if status != 0 or _prepararEntidades(mapa) != 0:
        return 1, None, None

    status, posicao = getPosicaoInicialMapa(mapa)

    if status != 0:
        return 1, None, None

    jogador["posicao"] = posicao
    return 0, jogador, mapa


def exibirStatus(jogador, mapa):
    if jogador is None or mapa is None:
        return 1

    status = _garantirPosicaoJogador(jogador, mapa)

    if status != 0:
        return status

    nome = _nomeJogador(jogador)
    _, vida = getVida(nome)
    _, ataque = getAtaque(nome)
    _, xp = getXP(nome)
    _, posicao = _posicaoJogador(jogador)
    chaves = _contarChaves(jogador)
    vida_maxima = jogador.get("vida_max", 100)
    barras = int((vida / vida_maxima) * 10)
    barra_vida = "█" * barras + "░" * (10 - barras)

    print("=" * 30)
    print(f"  Jogador : {nome}")
    print(f"  Vida    : [{barra_vida}] {vida}/{vida_maxima}")
    print(f"  Ataque  : {ataque}")
    print(f"  XP      : {xp}")
    print(f"  Chaves  : {chaves}/2")
    print(f"  Posição : {posicao}")
    print("=" * 30)
    return 0


def _normalizarComando(comando):
    if not isinstance(comando, str):
        return None

    comando = comando.strip().lower()
    return ATALHOS.get(comando, comando)


def _exibirMapa(jogador, mapa):
    _, posicao = _posicaoJogador(jogador)
    status, desenho = renderizarMapa(mapa, posicao)

    if status == 0:
        print(desenho)

    return status


def _exibirInventario(jogador):
    nome = _nomeJogador(jogador)
    _, vida = getVida(nome)
    _, ataque = getAtaque(nome)
    _, xp = getXP(nome)
    _, posicao = _posicaoJogador(jogador)
    _, inventario = getInventario(nome)
    chaves = _contarChaves(jogador)
    nomes = []

    for item in inventario:
        if isinstance(item, dict):
            nomes.append(item.get("nome", "Item"))
        else:
            nomes.append(str(item))

    texto_inventario = ", ".join(nomes) if nomes else "vazio"

    print("=" * 30)
    print(f"  Jogador : {nome}")
    print(f"  Vida    : {vida}/{jogador.get('vida_max', 100)}")
    print(f"  Ataque  : {ataque}")
    print(f"  XP      : {xp}")
    print(f"  Chaves  : {chaves}/2")
    print(f"  Posição : {posicao}")
    print(f"  Inventário: {texto_inventario}")
    print("=" * 30)
    return 0


def _usarItemMapa(jogador):
    nome = _nomeJogador(jogador)
    _, inventario = getInventario(nome)
    usaveis = [item for item in inventario if isinstance(item, dict) and item.get("tipo") in ["cura", "ataque"]]

    if not usaveis:
        print("  Nenhum item utilizável no inventário.")
        return 0

    for i, item in enumerate(usaveis):
        print(f"  {i + 1} - {item.get('nome', 'Item')} ({item.get('tipo')}: +{item.get('valor', 0)})")
    print("  0 - Cancelar")

    try:
        escolha = input("  Usar item: ").strip()
    except (EOFError, KeyboardInterrupt):
        return 0

    if not escolha.isdigit() or int(escolha) == 0:
        return 0

    num = int(escolha)
    if num < 1 or num > len(usaveis):
        print("  Opção inválida.")
        return 0

    item = usaveis[num - 1]
    codigo = usarItemJogador(nome, item)

    if codigo == 0:
        print(f"  {item.get('nome', 'Item')} utilizado.")
    else:
        print("  Não foi possível usar o item.")

    return 0


def processarComando(jogador, mapa, comando):
    if jogador is None or mapa is None or comando is None:
        return 2

    comando = _normalizarComando(comando)

    if comando is None:
        return 2

    if not comando:
        return 1

    status = _garantirPosicaoJogador(jogador, mapa)

    if status != 0:
        return status

    if comando in DIRECOES:
        status_movimento = moverJogadorMapa(mapa, jogador, comando, _contarChaves(jogador) >= 2)

        if status_movimento == 3:
            print(f"  Portão trancado. Você tem {_contarChaves(jogador)}/2 chaves.")
            return _exibirMapa(jogador, mapa)

        if status_movimento != 0:
            print("Movimento inválido. Tente outra direção.")
            return _exibirMapa(jogador, mapa)

        _, posicao = _posicaoJogador(jogador)
        print(f"  Posição : {posicao}")

        status_descricao, descricao = descreverPosicaoMapa(mapa, posicao[0], posicao[1])

        if status_descricao == 0:
            print(f"  Local   : {descricao}")

        status_evento = _resolverEventoAtual(jogador, mapa)

        if status_evento != 0:
            return status_evento

        return _exibirMapa(jogador, mapa)

    if comando == "inventario":
        _exibirInventario(jogador)
        return _usarItemMapa(jogador)

    if comando == "mapa":
        return _exibirMapa(jogador, mapa)

    if comando == "salvar e sair":
        return 0

    return 1


def loopJogo(jogador, mapa):
    if jogador is None or mapa is None:
        return 2

    if _garantirPosicaoJogador(jogador, mapa) != 0:
        return 2

    exibirStatus(jogador, mapa)
    print("Objetivo : pegue 2 chaves, entre no castelo e derrote o chefe.")

    nome = _nomeJogador(jogador)

    if getVida(nome)[1] > 0:
        _exibirMapa(jogador, mapa)

    while True:
        _, vida = getVida(nome)

        if vida <= 0:
            print("\nVocê morreu. Fim de jogo.")
            return 0

        print("\n" + "-" * 46)
        print("Movimento: W-Cima | S-Baixo | A-Esquerda | D-Direita")
        print("Ações    : 1-Inventário | 2-Mapa | 5-Salvar e sair")

        try:
            comando = input("\n> Escolha: ")
        except (EOFError, KeyboardInterrupt):
            print("\nJogo interrompido.")
            return 0

        comando_normalizado = _normalizarComando(comando)

        if not comando_normalizado:
            print("Escolha uma opção.")
            continue

        if comando_normalizado in COMANDOS_SAIDA:
            print("Encerrando o jogo...")
            return 0

        status = processarComando(jogador, mapa, comando_normalizado)

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
