import copy

__all__ = [
    "criarJogador",
    "getVida",
    "getXP",
    "getAtaque",
    "getInventario",
    "receberDanoJogador",
    "curarJogador",
    "ganharXP",
    "atualizarAtaque",
    "adicionarItemJogador",
    "usarItemJogador"
]

# Dicionário interno que armazena todos os TADs de jogadores indexados pelo nome
_jogadores = dict()

def _jogadorExiste(nome):
    """Valida se o nome corresponde a um jogador cadastrado e válido."""
    return nome in _jogadores and isinstance(_jogadores[nome], dict)

def criarJogador(nome):
    # CT-J03 - parâmetro inválido
    if nome is None:
        return 2

    # CT-J02 - nome vazio ou apenas espaços
    if not isinstance(nome, str) or not nome.strip():
        return 1

    nome_limpo = nome.strip()
    
    jogador = {
        "nome": nome_limpo,
        "vida": 100,
        "vida_max": 100,
        "xp": 0,
        "ataque": 10,
        "vivo": True,
        "inventario": []
    }
    _jogadores[nome_limpo] = jogador
    
    # Retorna uma cópia para que o jogo não quebre, mas proteja o dict original
    retorno_seguro = copy.deepcopy(jogador)
    return retorno_seguro


def getVida(nome):
    # CT-J05 - consultar vida de jogador inválido (não cadastrado)
    if not _jogadorExiste(nome):
        return 2, None

    jogador = _jogadores[nome]
    # CT-J06 - consultar vida sem campo vida
    if "vida" not in jogador:
        return 1, None

    # CT-J04 - consultar vida válida
    return 0, jogador["vida"]


def getXP(nome):
    # CT-J08 - consultar XP com jogador inválido
    if not _jogadorExiste(nome):
        return 2, None

    jogador = _jogadores[nome]
    # CT-J09 - consultar XP sem campo xp
    if "xp" not in jogador:
        return 1, None

    # CT-J07 - consultar XP válido
    return 0, jogador["xp"]


def getAtaque(nome):
    # CT-J11 - consultar ataque com jogador inválido
    if not _jogadorExiste(nome):
        return 2, None

    jogador = _jogadores[nome]
    # CT-J12 - consultar ataque sem campo ataque
    if "ataque" not in jogador:
        return 1, None

    # CT-J10 - consultar ataque válido
    return 0, jogador["ataque"]


def getInventario(nome):
    # CT-J17 - consultar inventário com jogador inválido
    if not _jogadorExiste(nome):
        return 2, None

    jogador = _jogadores[nome]
    # CT-J18 - consultar inventário sem campo inventário
    if "inventario" not in jogador:
        return 1, None

    # CT-J16 - consultar inventário válido (retorna cópia profunda)
    return 0, copy.deepcopy(jogador["inventario"])


def receberDanoJogador(nome, dano):
    # CT-J24 - jogador inválido
    if not _jogadorExiste(nome):
        return 2

    # CT-J23 - dano inválido
    if dano is None or not isinstance(dano, (int, float)) or dano < 0:
        return 2

    codigo, vida = getVida(nome)
    if codigo != 0:
        return 1

    # CT-J22 - aplicar dano válido
    jogador = _jogadores[nome]
    jogador["vida"] = max(0, vida - dano)

    if jogador["vida"] == 0:
        jogador["vivo"] = False

    return 0


def curarJogador(nome, valor):
    # parâmetro inválido
    if not _jogadorExiste(nome):
        return 2

    if valor is None or not isinstance(valor, (int, float)) or valor < 0:
        return 2

    codigo, vida = getVida(nome)
    if codigo != 0:
        return 1

    jogador = _jogadores[nome]
    if "vida_max" not in jogador:
        return 1

    # CT-J26 - vida cheia
    if vida >= jogador["vida_max"]:
        return 1

    # CT-J25 - cura aplicada corretamente
    jogador["vida"] = min(vida + valor, jogador["vida_max"])
    return 0


def ganharXP(nome, xp):
    # jogador inválido
    if not _jogadorExiste(nome):
        return 2

    # CT-J29 - ganhar XP inválido
    if xp is None or not isinstance(xp, (int, float)) or xp < 0:
        return 2

    codigo, xpAtual = getXP(nome)
    if codigo != 0:
        return 1

    # CT-J28 - ganhar XP válido
    _jogadores[nome]["xp"] = xpAtual + xp
    return 0


def atualizarAtaque(nome):
    # CT-J31 - jogador inválido
    if not _jogadorExiste(nome):
        return 2

    codigo, xp = getXP(nome)
    if codigo != 0:
        return 1

    # CT-J30 - atualizar ataque corretamente
    _jogadores[nome]["ataque"] = 10 + (xp // 100)
    return 0


def adicionarItemJogador(nome, item):
    # CT-J34 - parâmetro inválido
    if not _jogadorExiste(nome):
        return 2

    if item is None:
        return 2

    codigo, inventario = getInventario(nome)
    if codigo != 0:
        return 1

    # CT-J33 - inventário cheio
    if len(inventario) >= 5:
        return 1

    # CT-J32 - adicionar item válido
    _jogadores[nome]["inventario"].append(item)
    return 0


def usarItemJogador(nome, item):
    # CT-J37 - parâmetro inválido
    if not _jogadorExiste(nome):
        return 2

    if item is None:
        return 2

    codigo, inventario = getInventario(nome)
    if codigo != 0:
        return 1

    # CT-J36 - usar item inexistente
    if item not in inventario:
        return 1

    # CT-J35 - usar item válido
    jogador = _jogadores[nome]
    if item.get("tipo") == "cura":
        jogador["vida"] += item["valor"]
    elif item.get("tipo") == "ataque":
        jogador["ataque"] += item["valor"]

    jogador["inventario"].remove(item)
    return 0