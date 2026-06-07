__all__ = [
    "criarJogador",
    "getVida",
    "getXP",
    "getAtaque",
    "getPosicao",
    "getInventario",
    "moverJogador",
    "receberDanoJogador",
    "curarJogador",
    "ganharXP",
    "atualizarAtaque",
    "adicionarItemJogador",
    "usarItemJogador"
]


def _jogadorValido(jogador):
    return jogador is not None and isinstance(jogador, dict)


def criarJogador(nome):
    # CT-J03 - parâmetro inválido
    if nome is None:
        return 2, None

    # CT-J02 - nome vazio ou apenas espaços
    if not isinstance(nome, str) or not nome.strip():
        return 2, None

    # CT-J01 - jogador criado com sucesso
    jogador = {
        "nome": nome.strip(),
        "vida": 100,
        "vida_max": 100,
        "xp": 0,
        "ataque": 10,
        "posicao": (0, 0),
        "vivo": True,
        "inventario": []
    }

    return 0, jogador


def getVida(jogador):
    # CT-J05 - consultar vida de jogador inválido
    if jogador is None:
        return 2, None

    # CT-J06 - consultar vida sem campo vida
    if "vida" not in jogador:
        return 1, None

    # CT-J04 - consultar vida válida
    return 0, jogador["vida"]


def getXP(jogador):
    # CT-J08 - consultar XP com jogador inválido
    if jogador is None:
        return 2, None

    # CT-J09 - consultar XP sem campo xp
    if "xp" not in jogador:
        return 1, None

    # CT-J07 - consultar XP válido
    return 0, jogador["xp"]


def getAtaque(jogador):
    # CT-J11 - consultar ataque com jogador inválido
    if jogador is None:
        return 2, None

    # CT-J12 - consultar ataque sem campo ataque
    if "ataque" not in jogador:
        return 1, None

    # CT-J10 - consultar ataque válido
    return 0, jogador["ataque"]


def getPosicao(jogador):
    # CT-J14 - consultar posição com jogador inválido
    if jogador is None:
        return 2, None

    # CT-J15 - consultar posição sem campo posição
    if "posicao" not in jogador:
        return 1, None

    # CT-J13 - consultar posição válida
    return 0, jogador["posicao"]


def getInventario(jogador):
    # CT-J17 - consultar inventário com jogador inválido
    if jogador is None:
        return 2, None

    # CT-J18 - consultar inventário sem campo inventário
    if "inventario" not in jogador:
        return 1, None

    # CT-J16 - consultar inventário válido
    return 0, jogador["inventario"]


def moverJogador(jogador, dx, dy):
    # CT-J21 - jogador inválido
    if not _jogadorValido(jogador):
        return 2

    # CT-J20 - parâmetros inválidos
    if dx is None or dy is None:
        return 2

    if not isinstance(dx, (int, float)):
        return 2

    if not isinstance(dy, (int, float)):
        return 2

    codigo, posicao = getPosicao(jogador)

    if codigo != 0:
        return 1

    # CT-J19 - mover jogador corretamente
    x, y = posicao
    jogador["posicao"] = (x + dx, y + dy)

    return 0


def receberDanoJogador(jogador, dano):
    # CT-J24 - jogador inválido
    if not _jogadorValido(jogador):
        return 2

    # CT-J23 - dano inválido
    if dano is None:
        return 2

    if not isinstance(dano, (int, float)):
        return 2

    if dano < 0:
        return 2

    codigo, vida = getVida(jogador)

    if codigo != 0:
        return 1

    # CT-J22 - aplicar dano válido
    jogador["vida"] = max(0, vida - dano)

    if jogador["vida"] == 0:
        jogador["vivo"] = False

    return 0


def curarJogador(jogador, valor):
    # parâmetro inválido
    if not _jogadorValido(jogador):
        return 2

    if valor is None:
        return 2

    if not isinstance(valor, (int, float)):
        return 2

    if valor < 0:
        return 2

    codigo, vida = getVida(jogador)

    if codigo != 0:
        return 1

    if "vida_max" not in jogador:
        return 1

    # CT-J26 - vida cheia
    if vida >= jogador["vida_max"]:
        return 1

    # CT-J25 - cura aplicada corretamente
    jogador["vida"] = min(
        vida + valor,
        jogador["vida_max"]
    )

    return 0


def ganharXP(jogador, xp):
    # jogador inválido
    if not _jogadorValido(jogador):
        return 2

    # CT-J29 - ganhar XP inválido
    if xp is None:
        return 2

    if not isinstance(xp, (int, float)):
        return 2

    if xp < 0:
        return 2

    codigo, xpAtual = getXP(jogador)

    if codigo != 0:
        return 1

    # CT-J28 - ganhar XP válido
    jogador["xp"] = xpAtual + xp

    return 0


def atualizarAtaque(jogador):
    # CT-J31 - jogador inválido
    if not _jogadorValido(jogador):
        return 2

    codigo, xp = getXP(jogador)

    if codigo != 0:
        return 1

    # CT-J30 - atualizar ataque corretamente
    jogador["ataque"] = 10 + (xp // 100)

    return 0


def adicionarItemJogador(jogador, item):
    # CT-J34 - parâmetro inválido
    if not _jogadorValido(jogador):
        return 2

    if item is None:
        return 2

    codigo, inventario = getInventario(jogador)

    if codigo != 0:
        return 1

    # CT-J33 - inventário cheio
    if len(inventario) >= 5:
        return 1

    # CT-J32 - adicionar item válido
    inventario.append(item)

    return 0


def usarItemJogador(jogador, item):
    # CT-J37 - parâmetro inválido
    if not _jogadorValido(jogador):
        return 2

    if item is None:
        return 2

    codigo, inventario = getInventario(jogador)

    if codigo != 0:
        return 1

    # CT-J36 - usar item inexistente
    if item not in inventario:
        return 1

    # CT-J35 - usar item válido
    if item["tipo"] == "cura":
        jogador["vida"] += item["valor"]

    elif item["tipo"] == "ataque":
        jogador["ataque"] += item["valor"]

    inventario.remove(item)

    return 0