from mapa import *

def testar_criarMapa():
    estrutura_valida = {
        "regioes": ["floresta", "cidade", "dungeon"],
        "tamanho": (10, 10),
        "posicao_inicial": (0, 0)
    }
    codigo, mapa = criarMapa(estrutura_valida)
    assert codigo == 0
    assert mapa is not None
    assert criarMapa({}) == (1, None)
    assert criarMapa(None) == (2, None)
    print("testar_criarMapa: OK")

testar_criarMapa()

def testar_posicaoValida():

    codigo, mapa = criarMapa()

    assert posicaoValida(mapa, 1, "frente") == 0
    assert posicaoValida(mapa, 1, "esquerda") == 1
    assert posicaoValida(None, 1, "frente") == 2


def testar_temObstaculo():

    codigo, mapa = criarMapa()

    assert temObstaculo(mapa, 2, "frente") == 0
    assert temObstaculo(mapa, 2, "direita") == 1
    assert temObstaculo(None, 2, "frente") == 2


def testar_getEventoMapa():

    codigo, mapa = criarMapa()

    assert getEventoMapa(mapa, 3)[0] == 0
    assert getEventoMapa(mapa, 4)[0] == 1
    assert getEventoMapa(None, 3)[0] == 2


def testar_desativarEventoMapa():

    codigo, mapa = criarMapa()

    assert desativarEventoMapa(mapa, 3) == 0
    assert desativarEventoMapa(mapa, 4) == 1
    assert desativarEventoMapa(None, 3) == 2


def testar_moverJogadorMapa():

    codigo, mapa = criarMapa()

    jogador = {
        "nome": "Ana",
        "salaAtual": 1
    }

    assert moverJogadorMapa(mapa, jogador, "frente") == 0
    assert jogador["salaAtual"] == 2

    assert moverJogadorMapa(mapa, jogador, "esquerda") == 1
    assert moverJogadorMapa(None, jogador, "frente") == 2