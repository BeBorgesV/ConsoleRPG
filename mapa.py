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
    """
    Objetivo:
        Criar o TAD mapa a partir de uma estrutura de dados ou usar o mapa padrão.

    Requisitos funcionais:
        - Se nenhuma estrutura for fornecida, o mapa padrão deve ser criado.
        - A estrutura fornecida deve ser validada antes da criação.
        - O mapa criado deve conter regiões, tamanho, posição inicial, obstáculos e eventos.

    Acoplamento:
        Entrada:
            estrutura: dicionário descrevendo o mapa, ou omitido para usar o padrão.
        Saída:
            mapa: dicionário TAD representando o mapa criado.
        Retornos:
            (0, mapa): mapa criado com sucesso.
            (1, None): estrutura inválida por regra do jogo.
            (2, None): parâmetro inválido (None explícito).

    Condições de acoplamento:
        Assertivas de entrada:
            - estrutura deve ser um dicionário com os campos obrigatórios, ou omitida.
            - tamanho deve ser uma tupla de dois inteiros positivos.
            - posicao_inicial deve estar dentro dos limites do mapa.
        Assertivas de saída:
            - se retornar (0, mapa), o mapa contém os campos regioes, tamanho, posicao_inicial, obstaculos, eventos, itens, inimigos, chefes, descricoes e portao_castelo.
            - se retornar (1, None) ou (2, None), nenhum mapa é criado.

    Hipóteses e restrições:
        - O mapa padrão representa o Bosque do Castelo com grid 15x15.
        - Itens e inimigos são alocados separadamente após a criação do mapa.
    """
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
    """
    Objetivo:
        Verificar se uma posição pode ser ocupada no mapa.

    Requisitos funcionais:
        - A posição deve estar dentro dos limites do mapa.
        - A posição não deve ser um obstáculo.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            x: coordenada horizontal da posição.
            y: coordenada vertical da posição.
        Saída:
            código indicando a validade da posição.
        Retornos:
            0: posição válida e acessível.
            1: posição bloqueada (fora dos limites ou obstáculo).
            2: parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - x e y devem ser inteiros.
        Assertivas de saída:
            - se retornar 0, a posição (x, y) pode ser ocupada pelo jogador.
            - se retornar 1, a posição é inacessível.
            - se retornar 2, os parâmetros recebidos são inválidos.

    Hipóteses e restrições:
        - Obstáculos são definidos na criação do mapa e não se alteram.
    """
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
    """
    Objetivo:
        Alocar um item em uma posição do mapa pelo seu identificador.

    Requisitos funcionais:
        - A posição deve ser válida e estar vazia.
        - O identificador do item deve ser um inteiro não negativo.
        - A posição deve ser marcada com o evento item após a alocação.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            x: coordenada horizontal da posição.
            y: coordenada vertical da posição.
            id_item: identificador do item a ser alocado.
        Saída:
            mapa atualizado com o item na posição informada.
        Retornos:
            0: item alocado com sucesso.
            1: posição inválida ou já ocupada.
            2: parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - x e y devem ser inteiros.
            - id_item deve ser um inteiro maior ou igual a zero.
            - a posição não deve conter outro evento.
        Assertivas de saída:
            - se retornar 0, mapa["eventos"][(x, y)] é EVENTO_ITEM e mapa["itens"][(x, y)] é id_item.
            - se retornar 1 ou 2, o mapa não é alterado.

    Hipóteses e restrições:
        - O módulo mapa não valida se id_item corresponde a um item existente no módulo itens.
        - O módulo mapa armazena apenas o identificador do item, não sua estrutura interna.
    """
    status = _alocarEvento(mapa, x, y, id_item, EVENTO_ITEM)

    if status == 0:
        mapa["itens"][(x, y)] = id_item

    return status


def alocarInimigoMapa(mapa, x, y, id_inimigo, final=False):
    """
    Objetivo:
        Alocar um inimigo em uma posição do mapa pelo seu identificador.

    Requisitos funcionais:
        - A posição deve ser válida e estar vazia.
        - O identificador do inimigo deve ser um inteiro não negativo.
        - Quando final=True, o inimigo deve ser marcado como chefe.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            x: coordenada horizontal da posição.
            y: coordenada vertical da posição.
            id_inimigo: identificador do inimigo a ser alocado.
            final: indica se o inimigo é o chefe (padrão False).
        Saída:
            mapa atualizado com o inimigo na posição informada.
        Retornos:
            0: inimigo alocado com sucesso.
            1: posição inválida ou já ocupada.
            2: parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - x e y devem ser inteiros.
            - id_inimigo deve ser um inteiro maior ou igual a zero.
            - a posição não deve conter outro evento.
        Assertivas de saída:
            - se retornar 0, mapa["inimigos"][(x, y)] é id_inimigo.
            - se retornar 0 e final=True, a posição é registrada em mapa["chefes"].
            - se retornar 1 ou 2, o mapa não é alterado.

    Hipóteses e restrições:
        - O módulo mapa não valida se id_inimigo corresponde a um inimigo existente no módulo inimigos.
        - O módulo mapa armazena apenas o identificador do inimigo, não sua estrutura interna.
    """
    evento = EVENTO_CHEFE if final else EVENTO_INIMIGO
    status = _alocarEvento(mapa, x, y, id_inimigo, evento)

    if status == 0:
        mapa["inimigos"][(x, y)] = id_inimigo

        if final:
            mapa["chefes"].append((x, y))

    return status


def getItemMapa(mapa, x, y):
    """
    Objetivo:
        Retornar o identificador do item alocado em uma posição do mapa.

    Requisitos funcionais:
        - A posição deve ser válida e conter um evento do tipo item.
        - O identificador retornado deve referenciar o item alocado na posição.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            x: coordenada horizontal da posição.
            y: coordenada vertical da posição.
        Saída:
            id_item: identificador do item na posição informada.
        Retornos:
            (0, id_item): item encontrado na posição.
            (1, None): posição válida mas sem item.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - x e y devem ser inteiros.
            - a posição deve ser acessível no mapa.
        Assertivas de saída:
            - se retornar (0, id_item), id_item é o identificador do item na posição.
            - se retornar (1, None), não há item na posição informada.
            - o módulo mapa não conhece os dados internos do item, apenas seu identificador.

    Hipóteses e restrições:
        - O módulo mapa armazena apenas o identificador do item, não sua estrutura interna.
    """
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2, None

    if posicaoValida(mapa, x, y) != 0:
        return 1, None

    if mapa["eventos"].get((x, y), EVENTO_VAZIO) != EVENTO_ITEM:
        return 1, None

    return (0, mapa["itens"][(x, y)]) if (x, y) in mapa["itens"] else (1, None)


def getInimigoMapa(mapa, x, y):
    """
    Objetivo:
        Retornar o identificador do inimigo alocado em uma posição do mapa.

    Requisitos funcionais:
        - A posição deve ser válida e conter um evento do tipo inimigo ou chefe.
        - O identificador retornado deve referenciar o inimigo alocado na posição.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            x: coordenada horizontal da posição.
            y: coordenada vertical da posição.
        Saída:
            id_inimigo: identificador do inimigo na posição informada.
        Retornos:
            (0, id_inimigo): inimigo encontrado na posição.
            (1, None): posição válida mas sem inimigo.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - x e y devem ser inteiros.
            - a posição deve ser acessível no mapa.
        Assertivas de saída:
            - se retornar (0, id_inimigo), id_inimigo é o identificador do inimigo na posição.
            - se retornar (1, None), não há inimigo na posição informada.
            - o módulo mapa não conhece os dados internos do inimigo, apenas seu identificador.

    Hipóteses e restrições:
        - O módulo mapa armazena apenas o identificador do inimigo, não sua estrutura interna.
        - Eventos do tipo inimigo e chefe são tratados da mesma forma por esta função.
    """
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2, None

    if posicaoValida(mapa, x, y) != 0:
        return 1, None

    if mapa["eventos"].get((x, y), EVENTO_VAZIO) not in [EVENTO_INIMIGO, EVENTO_CHEFE]:
        return 1, None

    return (0, mapa["inimigos"][(x, y)]) if (x, y) in mapa["inimigos"] else (1, None)


def inimigoFinalMapa(mapa, x, y):
    """
    Objetivo:
        Verificar se o inimigo presente em uma posição é o chefe do mapa.

    Requisitos funcionais:
        - O mapa deve ser válido.
        - A verificação deve retornar True apenas para posições registradas como chefes.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            x: coordenada horizontal da posição.
            y: coordenada vertical da posição.
        Saída:
            booleano indicando se o inimigo na posição é o chefe.
        Retornos:
            (0, True): inimigo na posição é o chefe.
            (0, False): inimigo na posição não é o chefe.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - x e y devem ser inteiros.
        Assertivas de saída:
            - se retornar (0, True), a posição está registrada em mapa["chefes"].
            - se retornar (0, False), a posição não está em mapa["chefes"].

    Hipóteses e restrições:
        - Um inimigo é marcado como chefe na alocação via alocarInimigoMapa com final=True.
    """
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2, None

    return 0, (x, y) in mapa["chefes"]


def limparEventoMapa(mapa, x, y):
    """
    Objetivo:
        Remover o evento de uma posição do mapa após sua resolução.

    Requisitos funcionais:
        - A posição deve ser válida e conter um evento ativo.
        - Após a limpeza, o evento da posição deve ser EVENTO_VAZIO.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            x: coordenada horizontal da posição.
            y: coordenada vertical da posição.
        Saída:
            mapa atualizado com o evento da posição removido.
        Retornos:
            0: evento removido com sucesso.
            1: posição inválida ou sem evento ativo.
            2: parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - x e y devem ser inteiros.
            - a posição deve conter um evento diferente de EVENTO_VAZIO.
        Assertivas de saída:
            - se retornar 0, mapa["eventos"][(x, y)] é EVENTO_VAZIO.
            - se retornar 1 ou 2, o mapa não é alterado.

    Hipóteses e restrições:
        - Esta função não remove registros de mapa["inimigos"] nem mapa["itens"].
        - Deve ser chamada após a resolução do evento (coleta de item ou vitória em batalha).
    """
    if not _mapaValido(mapa) or not isinstance(x, int) or not isinstance(y, int):
        return 2

    if posicaoValida(mapa, x, y) != 0 or mapa["eventos"].get((x, y), EVENTO_VAZIO) == EVENTO_VAZIO:
        return 1

    mapa["eventos"][(x, y)] = EVENTO_VAZIO
    return 0


def registrarInimigoDerrotadoMapa(mapa, x, y):
    """
    Objetivo:
        Registrar a derrota de um inimigo, limpando seu evento no mapa.

    Requisitos funcionais:
        - Deve haver um inimigo válido na posição informada.
        - O evento da posição deve ser alterado para EVENTO_VAZIO.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            x: coordenada horizontal da posição.
            y: coordenada vertical da posição.
        Saída:
            mapa atualizado com o evento de combate removido.
        Retornos:
            0: inimigo registrado como derrotado com sucesso.
            1: não há inimigo na posição ou mapa inválido.
            2: parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - x e y devem ser inteiros.
            - a posição deve conter um evento do tipo inimigo ou chefe.
        Assertivas de saída:
            - se retornar 0, mapa["eventos"][(x, y)] é EVENTO_VAZIO.
            - se retornar 1 ou 2, o mapa não é alterado.

    Hipóteses e restrições:
        - Deve ser chamada após vitória do jogador em batalha.
        - Não altera os dados internos do inimigo no módulo inimigos.
    """
    if getInimigoMapa(mapa, x, y)[0] != 0:
        return 1 if _mapaValido(mapa) else 2

    mapa["eventos"][(x, y)] = EVENTO_VAZIO
    return 0


def moverJogadorMapa(mapa, jogador, direcao, castelo_liberado=True):
    """
    Objetivo:
        Mover o jogador para uma posição adjacente no mapa conforme a direção informada.

    Requisitos funcionais:
        - A direção deve ser válida.
        - O destino deve ser uma posição acessível no mapa.
        - Se o destino for o portão do castelo e ele não estiver liberado, o movimento deve ser bloqueado.
        - A posição do jogador deve ser atualizada após movimento bem-sucedido.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            jogador: dicionário do jogador com campo "posicao".
            direcao: string indicando a direção do movimento.
            castelo_liberado: indica se o portão do castelo pode ser atravessado (padrão True).
        Saída:
            jogador com campo "posicao" atualizado.
        Retornos:
            0: movimento realizado com sucesso.
            1: movimento inválido (direção inválida, posição bloqueada ou inexistente).
            2: parâmetro inválido.
            3: portão do castelo bloqueado.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - jogador deve ser um dicionário com o campo "posicao" definido.
            - direcao deve ser uma string pertencente ao conjunto de direções aceitas.
        Assertivas de saída:
            - se retornar 0, jogador["posicao"] foi atualizado para o destino.
            - se retornar 1, 2 ou 3, jogador["posicao"] permanece inalterado.
            - se retornar 3, o destino é o portão do castelo e castelo_liberado é False.

    Hipóteses e restrições:
        - Direções aceitas: "cima", "baixo", "esquerda", "direita", "w", "s", "a", "d".
        - O portão do castelo é desbloqueado quando o jogador possui as chaves necessárias.
    """
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
    """
    Objetivo:
        Retornar a posição inicial definida no mapa.

    Requisitos funcionais:
        - O mapa deve ser válido.
        - A posição retornada deve corresponder ao ponto de entrada do mapa.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
        Saída:
            posicao: tupla (x, y) representando a posição inicial do mapa.
        Retornos:
            (0, posicao): posição inicial retornada com sucesso.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
        Assertivas de saída:
            - se retornar (0, posicao), posicao é uma tupla (x, y) válida dentro dos limites do mapa.
            - se retornar (2, None), o mapa recebido é inválido.

    Hipóteses e restrições:
        - A posição inicial é definida na criação do mapa e não se altera durante o jogo.
    """
    return (0, mapa["posicao_inicial"]) if _mapaValido(mapa) else (2, None)


def descreverPosicaoMapa(mapa, x, y):
    """
    Objetivo:
        Retornar a descrição textual de uma posição do mapa.

    Requisitos funcionais:
        - A posição deve ser válida no mapa.
        - Se não houver descrição específica, retornar uma descrição padrão.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            x: coordenada horizontal da posição.
            y: coordenada vertical da posição.
        Saída:
            descricao: string descrevendo a posição informada.
        Retornos:
            (0, descricao): descrição retornada com sucesso.
            (1, None): posição fora dos limites ou obstáculo.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - x e y devem ser inteiros.
            - a posição deve ser acessível no mapa.
        Assertivas de saída:
            - se retornar (0, descricao), descricao é uma string não vazia.
            - posições sem descrição específica retornam uma mensagem padrão.

    Hipóteses e restrições:
        - As descrições são definidas na criação do mapa dentro do campo "descricoes".
    """
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
    """
    Objetivo:
        Gerar a representação visual do mapa completo ou de uma janela 5x5 centrada no jogador.

    Requisitos funcionais:
        - Se posicao_jogador for fornecida, exibir uma visão local 5x5 centrada nessa posição.
        - Se posicao_jogador for None, exibir o mapa completo.
        - Obstáculos, itens, inimigos, chefe, posição do jogador e portão devem ter símbolos distintos.

    Acoplamento:
        Entrada:
            mapa: dicionário TAD do mapa.
            posicao_jogador: tupla (x, y) com a posição atual do jogador, ou None para visão total.
        Saída:
            desenho: string com a representação visual do mapa.
        Retornos:
            (0, desenho): mapa renderizado com sucesso.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um TAD válido criado por criarMapa.
            - posicao_jogador, se fornecida, deve ser uma tupla de dois inteiros.
        Assertivas de saída:
            - se retornar (0, desenho), desenho é uma string multilinha com bordas e legenda.
            - a visão local cobre no máximo 5x5 células centradas na posição do jogador.

    Hipóteses e restrições:
        - Símbolos: @ jogador, I início, C castelo, # parede, ! item, M inimigo, Ω chefe, . caminho livre.
        - A janela de visão é ajustada nos limites do mapa quando o jogador está nas bordas.
    """
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
