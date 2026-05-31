def criarJogador(nome):
    # CT-J03: parâmetro inválido
    if nome is None:
        return 2, None

    # CT-J02: nome vazio ou só espaços
    if not isinstance(nome, str) or not nome.strip():
        return 2, None

    # CT-J01: jogador criado com sucesso
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
    #CT-J05: consultar vida de jogador inválido
    if jogador is None:
        return 2, None
    #CT-J06: consultar vida de jogador sem campo de vida
    if "vida" not in jogador:
        return 1, None
    #CT-J04: consultar vida de jogador válido
    return 0, jogador["vida"]

def getXP(jogador):
    #CT-J08: Consultar XP com jogador inválido
    if jogador is None:
        return 2, None
    #CT-J09: Consultar XP sem campo XP
    if "xp" not in jogador:
        return 1, None
    #CT-J07: Consultar XP válido
    return 0, jogador["xp"]

def getAtaque(jogador):
    #CT-J11: Consultar ataque com jogador inválido
    if jogador is None:
        return 2, None
    #CT-J12: Consultar ataque sem campo de ataque
    if "ataque" not in jogador:
        return 1, None
    #CT-J10: Consultar ataque válido
    return 0, jogador["ataque"]

def getPosicao(jogador):
    #CT-J13: Consultar posição com jogador inválido
    if jogador is None:
        return 2, None
    #CT-J14: Consultar posição sem campo de posição
    if "posicao" not in jogador:
        return 1, None
    #CT-J15: Consultar posição válida
    return 0, jogador["posicao"]

def getInventario(jogador):
    #CT-J16: Consultar inventário com jogador inválido
    if jogador is None:
        return 2, None
    #CT-J17: Consultar inventário sem campo de inventário
    if "inventario" not in jogador:
        return 1, None
    #CT-J18: Consultar inventário válido
    return 0, jogador["inventario"]

def moverJogador(jogador, dx, dy):
    # CT-J21: jogador inválido
    if jogador is None:
        return 2

    # CT-J20: parâmetros inválidos
    if dx is None or dy is None:
        return 2
    if not isinstance(dx, (int, float)) or not isinstance(dy, (int, float)):
        return 2

    if "posicao" not in jogador:
        return 1

    x, y = jogador["posicao"]
    jogador["posicao"] = (x + dx, y + dy)
    return 0

    