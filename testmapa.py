from mapa import *


def testar_criarMapa():
    estrutura = {
        "regioes": ["inicio"],
        "tamanho": (5, 5),
        "posicao_inicial": (0, 0)
    }

    codigo, mapa = criarMapa(estrutura)

    assert codigo == 0
    assert mapa is not None
    assert criarMapa({}) == (1, None)
    assert criarMapa(None) == (2, None)
    assert criarMapa()[0] == 0
    print("testar_criarMapa: OK")


def testar_posicao_e_obstaculo():
    codigo, mapa = criarMapa()

    assert codigo == 0
    assert posicaoValida(mapa, 1, 13) == 0
    assert posicaoValida(mapa, 4, 3) == 1
    assert posicaoValida(mapa, -1, 0) == 1
    assert posicaoValida(mapa, 1, "x") == 2
    print("testar_posicao_e_obstaculo: OK")


def testar_eventos():
    codigo, mapa = criarMapa()

    assert codigo == 0
    assert alocarItemMapa(mapa, 2, 12, 0) == 0
    assert getItemMapa(mapa, 2, 12) == (0, 0)

    assert limparEventoMapa(mapa, 2, 12) == 0
    assert getItemMapa(mapa, 2, 12) == (1, None)
    print("testar_eventos: OK")


def testar_inimigos():
    codigo, mapa = criarMapa()

    assert codigo == 0
    assert alocarInimigoMapa(mapa, 5, 11, 0) == 0
    assert alocarInimigoMapa(mapa, 13, 2, 1, True) == 0
    assert getInimigoMapa(mapa, 5, 11) == (0, 0)
    assert inimigoFinalMapa(mapa, 13, 2) == (0, True)
    assert registrarInimigoDerrotadoMapa(mapa, 5, 11) == 0
    assert getInimigoMapa(mapa, 5, 11) == (1, None)
    print("testar_inimigos: OK")


def testar_movimento():
    codigo, mapa = criarMapa()
    jogador = {"nome": "Ana", "posicao": (1, 13)}

    assert codigo == 0
    assert moverJogadorMapa(mapa, jogador, "d") == 0
    assert jogador["posicao"] == (2, 13)
    assert moverJogadorMapa(mapa, jogador, "w") == 0
    assert jogador["posicao"] == (2, 12)

    jogador["posicao"] = (4, 2)
    assert moverJogadorMapa(mapa, jogador, "s") == 1
    assert jogador["posicao"] == (4, 2)

    jogador["posicao"] = (13, 5)
    assert moverJogadorMapa(mapa, jogador, "w", False) == 3
    assert jogador["posicao"] == (13, 5)
    assert moverJogadorMapa(mapa, jogador, "w", True) == 0
    assert jogador["posicao"] == (13, 4)
    print("testar_movimento: OK")


def testar_renderizarMapa():
    codigo, mapa = criarMapa()
    codigo_render, desenho = renderizarMapa(mapa, (1, 13))

    assert codigo == 0
    assert codigo_render == 0
    assert "Visao local" in desenho
    assert "@" in desenho
    assert len(desenho.splitlines()[2:7]) == 5
    print("testar_renderizarMapa: OK")


if __name__ == "__main__":
    testar_criarMapa()
    testar_posicao_e_obstaculo()
    testar_eventos()
    testar_inimigos()
    testar_movimento()
    testar_renderizarMapa()
    print("Todos os testes do modulo mapa passaram.")
