__all__ = [
    "EVENTO_VAZIO",
    "EVENTO_INIMIGO",
    "EVENTO_ITEM",
    "EVENTO_DESCANSO",
    "EVENTO_SAIDA",
    "criarMapa",
    "posicaoValida",
    "temObstaculo",
    "getEventoMapa",
    "limparEventoMapa",
    "desativarEventoMapa",
    "moverJogadorMapa",
    "getPosicaoInicialMapa",
    "getTamanhoMapa",
    "descreverPosicaoMapa",
    "renderizarMapa"
]

EVENTO_VAZIO = "vazio"
EVENTO_INIMIGO = "inimigo"
EVENTO_ITEM = "item"
EVENTO_DESCANSO = "descanso"
EVENTO_SAIDA = "saida"

EVENTOS_VALIDOS = [
    EVENTO_VAZIO,
    EVENTO_INIMIGO,
    EVENTO_ITEM,
    EVENTO_DESCANSO,
    EVENTO_SAIDA
]

DIRECOES = {
    "cima": (0, -1),
    "baixo": (0, 1),
    "esquerda": (-1, 0),
    "direita": (1, 0),
    "frente": (1, 0),
    "tras": (-1, 0)
}

_SEM_ESTRUTURA = object()


def _mapaPadrao():
    # Pequena historia para o trabalho: atravessar salas externas ate a dungeon.
    return {
        "nome": "Ruinas antes da Dungeon",
        "regioes": ["bosque", "ruinas", "sala da fonte", "entrada da dungeon"],
        "tamanho": (8, 7),
        "posicao_inicial": (0, 3),
        "obstaculos": [
            (3, 0),
            (1, 1), (3, 1), (5, 1),
            (1, 2), (5, 2), (7, 2),
            (3, 3),
            (1, 4), (3, 4), (5, 4), (7, 4),
            (1, 5), (5, 5),
            (3, 6)
        ],
        "eventos": {
            (2, 0): EVENTO_ITEM,
            (6, 0): EVENTO_INIMIGO,
            (2, 5): EVENTO_DESCANSO,
            (6, 5): EVENTO_ITEM,
            (5, 6): EVENTO_INIMIGO,
            (7, 0): EVENTO_SAIDA,
            (7, 6): EVENTO_SAIDA
        },
        "descricoes": {
            (0, 3): "Clareira inicial. As ruinas estao logo a frente.",
            (2, 0): "Uma sala lateral guarda uma mochila esquecida.",
            (6, 0): "Um guarda bloqueia a entrada norte da dungeon.",
            (2, 5): "A sala da fonte permite recuperar o folego.",
            (6, 5): "Um bau simples esta perto da passagem inferior.",
            (5, 6): "Um inimigo patrulha o corredor sul.",
            (7, 0): "Entrada norte da dungeon.",
            (7, 6): "Entrada sul da dungeon."
        },
        "salas": {
            1: {"frente": 2},
            2: {"tras": 1, "frente": 3},
            3: {"tras": 2}
        },
        "eventos_salas": {
            3: EVENTO_ITEM
        },
        "obstaculos_salas": [3]
    }


def _coordenadaValida(coordenada):
    if not isinstance(coordenada, tuple):
        return False

    if len(coordenada) != 2:
        return False

    x, y = coordenada
    return isinstance(x, int) and isinstance(y, int)


def _estruturaValida(estrutura):
    if not isinstance(estrutura, dict) or len(estrutura) == 0:
        return False

    if "regioes" not in estrutura:
        return False

    if "tamanho" not in estrutura:
        return False

    if "posicao_inicial" not in estrutura:
        return False

    if not isinstance(estrutura["regioes"], list):
        return False

    if not _coordenadaValida(estrutura["tamanho"]):
        return False

    if not _coordenadaValida(estrutura["posicao_inicial"]):
        return False

    largura, altura = estrutura["tamanho"]

    if largura <= 0 or altura <= 0:
        return False

    x_inicial, y_inicial = estrutura["posicao_inicial"]

    if x_inicial < 0 or y_inicial < 0:
        return False

    if x_inicial >= largura or y_inicial >= altura:
        return False

    if "obstaculos" in estrutura and not isinstance(estrutura["obstaculos"], list):
        return False

    if "eventos" in estrutura and not isinstance(estrutura["eventos"], dict):
        return False

    return True


def _mapaValido(mapa):
    if not isinstance(mapa, dict):
        return False

    campos = ["regioes", "tamanho", "posicao_inicial", "obstaculos", "eventos"]

    for campo in campos:
        if campo not in mapa:
            return False

    return _estruturaValida(mapa)


def _dentroDoMapa(mapa, x, y):
    largura, altura = mapa["tamanho"]
    return x >= 0 and y >= 0 and x < largura and y < altura


def _copiarLista(lista):
    copia = []

    for item in lista:
        copia.append(item)

    return copia


def _normalizarObstaculos(estrutura):
    obstaculos = []
    largura, altura = estrutura["tamanho"]
    posicao_inicial = estrutura["posicao_inicial"]

    for obstaculo in estrutura.get("obstaculos", []):
        if not _coordenadaValida(obstaculo):
            continue

        x, y = obstaculo

        if x < 0 or y < 0 or x >= largura or y >= altura:
            continue

        if obstaculo == posicao_inicial:
            continue

        if obstaculo not in obstaculos:
            obstaculos.append(obstaculo)

    return obstaculos


def _normalizarEventos(estrutura, obstaculos):
    eventos = {}
    largura, altura = estrutura["tamanho"]
    posicao_inicial = estrutura["posicao_inicial"]

    for posicao in estrutura.get("eventos", {}):
        if not _coordenadaValida(posicao):
            continue

        x, y = posicao
        evento = estrutura["eventos"][posicao]

        if x < 0 or y < 0 or x >= largura or y >= altura:
            continue

        if posicao == posicao_inicial or posicao in obstaculos:
            continue

        if evento not in EVENTOS_VALIDOS:
            continue

        eventos[posicao] = evento

    return eventos


def criarMapa(estrutura=_SEM_ESTRUTURA):
    if estrutura is _SEM_ESTRUTURA:
        estrutura = _mapaPadrao()
    elif estrutura is None:
        return 2, None

    if not _estruturaValida(estrutura):
        return 1, None

    obstaculos = _normalizarObstaculos(estrutura)
    eventos = _normalizarEventos(estrutura, obstaculos)

    mapa = {
        "nome": estrutura.get("nome", "Mapa"),
        "regioes": _copiarLista(estrutura["regioes"]),
        "tamanho": estrutura["tamanho"],
        "posicao_inicial": estrutura["posicao_inicial"],
        "obstaculos": obstaculos,
        "eventos": eventos,
        "descricoes": estrutura.get("descricoes", {}),
        "salas": estrutura.get("salas", {}),
        "eventos_salas": estrutura.get("eventos_salas", {}),
        "obstaculos_salas": estrutura.get("obstaculos_salas", [])
    }

    return 0, mapa


def posicaoValida(mapa, x, y):
    if not _mapaValido(mapa):
        return 2

    if isinstance(y, str):
        salas = mapa.get("salas", {})

        if x not in salas:
            return 1

        if y not in salas[x]:
            return 1

        return 0

    if not isinstance(x, int) or not isinstance(y, int):
        return 2

    if not _dentroDoMapa(mapa, x, y):
        return 1

    if (x, y) in mapa["obstaculos"]:
        return 1

    return 0


def temObstaculo(mapa, x, y):
    if not _mapaValido(mapa):
        return 2

    if y == "sala":
        # Compatibilidade com testes antigos baseados em salas.
        if x in mapa.get("obstaculos_salas", []):
            return 0

        return 1

    if isinstance(y, str):
        if posicaoValida(mapa, x, y) != 0:
            return 1

        destino = mapa["salas"][x][y]
        return temObstaculo(mapa, destino, "sala")

    if not isinstance(x, int) or not isinstance(y, int):
        return 2

    if not _dentroDoMapa(mapa, x, y):
        return 1

    if (x, y) in mapa["obstaculos"]:
        return 0

    return 1


def getEventoMapa(mapa, x, y=None):
    if not _mapaValido(mapa):
        return 2, None

    if y is None:
        if not isinstance(x, int):
            return 2, None

        evento = mapa.get("eventos_salas", {}).get(x, EVENTO_VAZIO)

        if evento != EVENTO_VAZIO:
            return 0, evento

        return 1, None

    if not isinstance(x, int) or not isinstance(y, int):
        return 2, None

    if posicaoValida(mapa, x, y) != 0:
        return 1, None

    return 0, mapa["eventos"].get((x, y), EVENTO_VAZIO)


def limparEventoMapa(mapa, x, y=None):
    if not _mapaValido(mapa):
        return 2

    if y is None:
        if not isinstance(x, int):
            return 2

        if x not in mapa.get("eventos_salas", {}):
            return 1

        if mapa["eventos_salas"][x] == EVENTO_VAZIO:
            return 1

        mapa["eventos_salas"][x] = EVENTO_VAZIO
        return 0

    if not isinstance(x, int) or not isinstance(y, int):
        return 2

    if posicaoValida(mapa, x, y) != 0:
        return 1

    if (x, y) not in mapa["eventos"]:
        return 1

    if mapa["eventos"][(x, y)] == EVENTO_VAZIO:
        return 1

    mapa["eventos"][(x, y)] = EVENTO_VAZIO
    return 0


def desativarEventoMapa(mapa, x, y=None):
    return limparEventoMapa(mapa, x, y)


def moverJogadorMapa(mapa, jogador, direcao):
    if not _mapaValido(mapa) or not isinstance(jogador, dict):
        return 2

    if not isinstance(direcao, str):
        return 2

    direcao = direcao.strip().lower()

    if "salaAtual" in jogador:
        sala_atual = jogador["salaAtual"]

        if posicaoValida(mapa, sala_atual, direcao) != 0:
            return 1

        if temObstaculo(mapa, sala_atual, direcao) == 0:
            return 1

        jogador["salaAtual"] = mapa["salas"][sala_atual][direcao]
        return 0

    if "posicao" not in jogador:
        return 1

    if not _coordenadaValida(jogador["posicao"]):
        return 1

    if direcao not in DIRECOES:
        return 1

    dx, dy = DIRECOES[direcao]
    x, y = jogador["posicao"]
    novo_x = x + dx
    novo_y = y + dy

    if posicaoValida(mapa, novo_x, novo_y) != 0:
        return 1

    jogador["posicao"] = (novo_x, novo_y)
    return 0


def getPosicaoInicialMapa(mapa):
    if not _mapaValido(mapa):
        return 2, None

    return 0, mapa["posicao_inicial"]


def getTamanhoMapa(mapa):
    if not _mapaValido(mapa):
        return 2, None

    return 0, mapa["tamanho"]


def descreverPosicaoMapa(mapa, x, y):
    if not _mapaValido(mapa):
        return 2, None

    if not isinstance(x, int) or not isinstance(y, int):
        return 2, None

    if posicaoValida(mapa, x, y) != 0:
        return 1, None

    _, evento = getEventoMapa(mapa, x, y)

    descricao = {
        "posicao": (x, y),
        "evento": evento,
        "obstaculo": False,
        "texto": mapa.get("descricoes", {}).get((x, y), "Caminho livre.")
    }

    return 0, descricao


def renderizarMapa(mapa, posicao_jogador=None):
    if not _mapaValido(mapa):
        return 2, None

    if posicao_jogador is not None and not _coordenadaValida(posicao_jogador):
        return 2, None

    largura, altura = mapa["tamanho"]
    linhas_mapa = []

    for y in range(altura):
        linha = []

        for x in range(largura):
            posicao = (x, y)

            if posicao == posicao_jogador:
                linha.append("J")
            elif posicao == mapa["posicao_inicial"]:
                linha.append("I")
            elif posicao in mapa["obstaculos"]:
                linha.append("#")
            elif mapa["eventos"].get(posicao) == EVENTO_INIMIGO:
                linha.append("M")
            elif mapa["eventos"].get(posicao) == EVENTO_ITEM:
                linha.append("T")
            elif mapa["eventos"].get(posicao) == EVENTO_DESCANSO:
                linha.append("+")
            elif mapa["eventos"].get(posicao) == EVENTO_SAIDA:
                linha.append("E")
            else:
                linha.append(".")

        linhas_mapa.append(" ".join(linha))

    largura_texto = largura * 2 - 1
    borda = "+" + "-" * (largura_texto + 2) + "+"
    titulo = "Mapa: " + mapa.get("nome", "Mapa")

    if posicao_jogador is not None:
        titulo += " | Posicao: " + str(posicao_jogador)

    linhas = [
        titulo,
        borda
    ]

    for linha in linhas_mapa:
        linhas.append("| " + linha + " |")

    linhas.append(borda)

    if posicao_jogador is not None:
        linhas.append("J=voce I=inicio #=bloqueio T=item M=inimigo +=descanso E=entrada")
    else:
        linhas.append("I=inicio #=bloqueio T=item M=inimigo +=descanso E=entrada")

    return 0, "\n".join(linhas)
