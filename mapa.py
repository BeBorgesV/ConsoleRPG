__all__ = [
    "criarMapa",
    "posicaoValida",
    "getItemMapa",
    "getInimigoMapa",
    "alocarItemMapa",
    "alocarInimigoMapa",
    "limparEventoMapa",
    "registrarInimigoDerrotadoMapa",
    "inimigoFinalMapa",
    "moverJogadorMapa",
    "getPosicaoInicialMapa",
    "descreverPosicaoMapa",
    "renderizarMapa"
]

EVENTO_VAZIO = "vazio"
EVENTO_ITEM = "item"
EVENTO_INIMIGO = "inimigo"
EVENTO_CHEFE = "chefe"

_EVENTOS_VALIDOS = [EVENTO_VAZIO, EVENTO_ITEM, EVENTO_INIMIGO, EVENTO_CHEFE]
_DIRECOES = {
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0),
    "cima": (0, -1),
    "baixo": (0, 1),
    "esquerda": (-1, 0),
    "direita": (1, 0)
}
_SIMBOLOS = {
    EVENTO_ITEM: "!",
    EVENTO_INIMIGO: "M",
    EVENTO_CHEFE: "Ω"
}
_SEM_ESTRUTURA = object()


def _ehPosicao(posicao):
    return (
        isinstance(posicao, tuple) and
        len(posicao) == 2 and
        isinstance(posicao[0], int) and
        isinstance(posicao[1], int)
    )


def _dentroDoMapa(tamanho, posicao):
    return _ehPosicao(posicao) and 0 <= posicao[0] < tamanho[0] and 0 <= posicao[1] < tamanho[1]


def _estruturaValida(estrutura):
    if not isinstance(estrutura, dict):
        return False

    for campo in ["regioes", "tamanho", "posicao_inicial"]:
        if campo not in estrutura:
            return False

    if not isinstance(estrutura["regioes"], list) or not _ehPosicao(estrutura["tamanho"]):
        return False

    largura, altura = estrutura["tamanho"]
    if largura <= 0 or altura <= 0:
        return False

    if not _dentroDoMapa(estrutura["tamanho"], estrutura["posicao_inicial"]):
        return False

    tipos_opcionais = {
        "obstaculos": list,
        "eventos": dict,
        "descricoes": dict,
        "portao_castelo": tuple
    }

    for campo, tipo in tipos_opcionais.items():
        if campo in estrutura and not isinstance(estrutura[campo], tipo):
            if campo == "portao_castelo" and estrutura[campo] is None:
                continue

            return False

    return True


def _mapaValido(mapa):
    campos = ["regioes", "tamanho", "posicao_inicial", "obstaculos", "eventos"]
    return isinstance(mapa, dict) and all(campo in mapa for campo in campos) and _estruturaValida(mapa)


def _posicoesValidas(posicoes, tamanho, proibidas):
    validas = []

    for posicao in posicoes:
        if _dentroDoMapa(tamanho, posicao) and posicao not in proibidas and posicao not in validas:
            validas.append(posicao)

    return validas


def _caminhoPadrao():
    return [
        (1, 13), (2, 13), (3, 13),
        (3, 12), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11),
        (7, 10), (7, 9), (8, 9), (9, 9), (10, 9),
        (10, 8), (10, 7), (11, 7), (12, 7), (13, 7),
        (13, 6), (13, 5), (13, 4), (13, 3), (13, 2),
        (2, 12), (2, 11), (2, 10), (1, 10),
        (4, 13), (5, 13),
        (9, 7), (8, 7), (8, 6), (8, 5),
        (11, 6)
    ]


def _mapaPadrao():
    tamanho = (15, 15)
    caminho = _caminhoPadrao()
    obstaculos = []

    for y in range(tamanho[1]):
        for x in range(tamanho[0]):
            if (x, y) not in caminho:
                obstaculos.append((x, y))

    return {
        "nome": "Bosque do Castelo",
        "regioes": ["entrada do bosque", "trilha fechada", "castelo antigo"],
        "tamanho": tamanho,
        "posicao_inicial": (1, 13),
        "obstaculos": obstaculos,
        "eventos": {},
        "portao_castelo": (13, 4),
        "descricoes": {
            (1, 13): "Entrada do bosque. O caminho segue para leste.",
            (2, 12): "Uma pocao simples foi deixada perto da trilha.",
            (3, 11): "Bifurcacao: o desvio oeste parece levar a uma chave.",
            (1, 10): "Uma chave antiga esta presa em um galho baixo.",
            (5, 11): "Um lobo bloqueia a primeira passagem.",
            (5, 13): "Um amuleto de ataque brilha no fim do desvio.",
            (7, 9): "A trilha estreita força voce a seguir pela curva.",
            (10, 7): "Bifurcacao: a oeste ha pedras suspeitas; a leste fica o castelo.",
            (8, 5): "A segunda chave esta escondida perto das pedras.",
            (9, 9): "Um bandido guarda a curva do bosque.",
            (11, 6): "Uma pocao forte esta escondida antes do portao.",
            (12, 7): "Um guarda protege a entrada do castelo.",
            (13, 5): "O portao do castelo esta logo ao norte.",
            (13, 4): "Portao do castelo. Ele exige duas chaves.",
            (13, 2): "Sala do chefe. A batalha final começa aqui."
        }
    }


def _normalizarEventos(eventos, tamanho, bloqueadas):
    eventos_validos = {}

    for posicao, evento in eventos.items():
        if _dentroDoMapa(tamanho, posicao) and posicao not in bloqueadas and evento in _EVENTOS_VALIDOS:
            eventos_validos[posicao] = evento

    return eventos_validos


def criarMapa(estrutura=_SEM_ESTRUTURA):
    """Cria o TAD mapa e retorna (0, mapa), (1, None) ou (2, None)."""
    if estrutura is _SEM_ESTRUTURA:
        estrutura = _mapaPadrao()
    elif estrutura is None:
        return 2, None

    if not _estruturaValida(estrutura):
        return 1, None

    tamanho = estrutura["tamanho"]
    inicial = estrutura["posicao_inicial"]
    obstaculos = _posicoesValidas(estrutura.get("obstaculos", []), tamanho, [inicial])

    mapa = {
        "nome": estrutura.get("nome", "Mapa"),
        "regioes": list(estrutura["regioes"]),
        "tamanho": tamanho,
        "posicao_inicial": inicial,
        "obstaculos": obstaculos,
        "eventos": _normalizarEventos(estrutura.get("eventos", {}), tamanho, obstaculos + [inicial]),
        "itens": {},
        "inimigos": {},
        "chefes": [],
        "descricoes": dict(estrutura.get("descricoes", {})),
        "portao_castelo": estrutura.get("portao_castelo")
    }
    return 0, mapa


def posicaoValida(mapa, x, y):
    """Verifica se uma posicao pode ser ocupada: 0 valida, 1 bloqueada, 2 invalida."""
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2

    if not _dentroDoMapa(mapa["tamanho"], (x, y)) or (x, y) in mapa["obstaculos"]:
        return 1

    return 0


def _alocarEvento(mapa, x, y, id_entidade, evento):
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2

    if not isinstance(id_entidade, int) or id_entidade < 0:
        return 2

    if posicaoValida(mapa, x, y) != 0 or mapa["eventos"].get((x, y), EVENTO_VAZIO) != EVENTO_VAZIO:
        return 1

    mapa["eventos"][(x, y)] = evento
    return 0


def alocarItemMapa(mapa, x, y, id_item):
    """Aloca um id de item no mapa sem armazenar os dados internos do item."""
    status = _alocarEvento(mapa, x, y, id_item, EVENTO_ITEM)

    if status == 0:
        mapa["itens"][(x, y)] = id_item

    return status


def alocarInimigoMapa(mapa, x, y, id_inimigo, final=False):
    """Aloca um id de inimigo no mapa, marcando como chefe quando final=True."""
    evento = EVENTO_CHEFE if final else EVENTO_INIMIGO
    status = _alocarEvento(mapa, x, y, id_inimigo, evento)

    if status == 0:
        mapa["inimigos"][(x, y)] = id_inimigo

        if final:
            mapa["chefes"].append((x, y))

    return status


def getItemMapa(mapa, x, y):
    """Retorna o id do item alocado em uma posicao."""
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2, None

    if posicaoValida(mapa, x, y) != 0:
        return 1, None

    if mapa["eventos"].get((x, y), EVENTO_VAZIO) != EVENTO_ITEM:
        return 1, None

    return (0, mapa["itens"][(x, y)]) if (x, y) in mapa["itens"] else (1, None)


def getInimigoMapa(mapa, x, y):
    """Retorna o id do inimigo alocado em uma posicao."""
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2, None

    if posicaoValida(mapa, x, y) != 0:
        return 1, None

    if mapa["eventos"].get((x, y), EVENTO_VAZIO) not in [EVENTO_INIMIGO, EVENTO_CHEFE]:
        return 1, None

    return (0, mapa["inimigos"][(x, y)]) if (x, y) in mapa["inimigos"] else (1, None)


def inimigoFinalMapa(mapa, x, y):
    """Informa se o inimigo da posicao e o chefe."""
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2, None

    return 0, (x, y) in mapa["chefes"]


def limparEventoMapa(mapa, x, y):
    """Remove o evento de uma posicao depois que ele foi resolvido."""
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2

    if posicaoValida(mapa, x, y) != 0 or mapa["eventos"].get((x, y), EVENTO_VAZIO) == EVENTO_VAZIO:
        return 1

    mapa["eventos"][(x, y)] = EVENTO_VAZIO
    return 0


def registrarInimigoDerrotadoMapa(mapa, x, y):
    """Remove o combate de uma posicao depois da vitoria."""
    if getInimigoMapa(mapa, x, y)[0] != 0:
        return 1 if _mapaValido(mapa) else 2

    mapa["eventos"][(x, y)] = EVENTO_VAZIO
    return 0


def moverJogadorMapa(mapa, jogador, direcao, castelo_liberado=True):
    """Move o jogador no mapa quando o destino e valido."""
    if not _mapaValido(mapa) or not isinstance(jogador, dict) or not isinstance(direcao, str):
        return 2

    if "posicao" not in jogador or not _ehPosicao(jogador["posicao"]):
        return 1

    direcao = direcao.strip().lower()
    if direcao not in _DIRECOES:
        return 1

    dx, dy = _DIRECOES[direcao]
    x, y = jogador["posicao"]
    destino = (x + dx, y + dy)

    if posicaoValida(mapa, destino[0], destino[1]) != 0:
        return 1

    if destino == mapa.get("portao_castelo") and not castelo_liberado:
        return 3

    jogador["posicao"] = destino
    return 0


def getPosicaoInicialMapa(mapa):
    """Retorna a posicao inicial do mapa."""
    return (0, mapa["posicao_inicial"]) if _mapaValido(mapa) else (2, None)


def descreverPosicaoMapa(mapa, x, y):
    """Retorna uma descricao simples da posicao atual."""
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2, None

    if posicaoValida(mapa, x, y) != 0:
        return 1, None

    return 0, mapa["descricoes"].get((x, y), "Corredor do bosque. Siga pelo caminho aberto.")


def _janelaVisao(coordenada, limite):
    inicio = max(0, coordenada - 2)
    fim = min(limite - 1, inicio + 4)
    return max(0, fim - 4), fim


def _simbolo(mapa, posicao, jogador):
    if posicao == jogador:
        return "@"
    if posicao == mapa["posicao_inicial"]:
        return "I"
    if posicao == mapa.get("portao_castelo"):
        return "C"
    if posicao in mapa["obstaculos"]:
        return "#"
    return _SIMBOLOS.get(mapa["eventos"].get(posicao), ".")


def renderizarMapa(mapa, posicao_jogador=None):
    """Monta o texto do mapa completo ou da visao local 5x5."""
    if not _mapaValido(mapa) or (posicao_jogador is not None and not _ehPosicao(posicao_jogador)):
        return 2, None

    largura, altura = mapa["tamanho"]

    if posicao_jogador is None:
        x1, x2, y1, y2 = 0, largura - 1, 0, altura - 1
        titulo = "Mapa: " + mapa["nome"]
    else:
        x1, x2 = _janelaVisao(posicao_jogador[0], largura)
        y1, y2 = _janelaVisao(posicao_jogador[1], altura)
        titulo = "Visao local: " + mapa["nome"] + " | Posicao: " + str(posicao_jogador)

    linhas = []
    for y in range(y1, y2 + 1):
        linha = [_simbolo(mapa, (x, y), posicao_jogador) for x in range(x1, x2 + 1)]
        linhas.append(" ".join(linha))

    largura_visual = (x2 - x1 + 1) * 2 + 1
    borda = "+" + "-" * largura_visual + "+"
    desenho = [titulo, borda]
    desenho += ["| " + linha + " |" for linha in linhas]
    desenho.append(borda)
    desenho.append("@=voce I=inicio C=castelo #=parede !=item M=inimigo Ω=chefe")
    return 0, "\n".join(desenho)
