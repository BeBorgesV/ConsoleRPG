from jogador import *

def testar_criarJogador():
    codigo, jogador = criarJogador("Ana")
    assert codigo == 0
    assert jogador["nome"] == "Ana"
    assert criarJogador("") == (2, None)
    assert criarJogador(None) == (2, None)
    print("testar_criarJogador : OK")

testar_criarJogador()

def testar_getVida():
    _, jogador = criarJogador("Ana")
    assert getVida(jogador) == (0, 100)        # CT-J04
    assert getVida(None) == (2, None)           # CT-J05
    assert getVida({}) == (1, None)             # CT-J06
    print("testar_getVida: OK")

testar_getVida()

def testar_getXP():
    _, jogador = criarJogador("Ana")
    assert getXP(jogador) == (0, 0)            # CT-J07
    assert getXP(None) == (2, None)            # CT-J08
    assert getXP({}) == (1, None)              # CT-J09
    print("testar_getXP: OK")

testar_getXP()

def testar_getAtaque():
    _, jogador = criarJogador("Ana")
    assert getAtaque(jogador) == (0, 10)       # CT-J10
    assert getAtaque(None) == (2, None)        # CT-J11
    assert getAtaque({}) == (1, None)          # CT-J12
    print("testar_getAtaque: OK")

testar_getAtaque()

def testar_getPosicao():
    _, jogador = criarJogador("Ana")
    assert getPosicao(jogador) == (0, (0, 0))  # CT-J13
    assert getPosicao(None) == (2, None)       # CT-J14
    assert getPosicao({}) == (1, None)         # CT-J15
    print("testar_getPosicao: OK")

testar_getPosicao()

def testar_getInventario():
    _, jogador = criarJogador("Ana")
    assert getInventario(jogador) == (0, [])   # CT-J16
    assert getInventario(None) == (2, None)    # CT-J17
    assert getInventario({}) == (1, None)      # CT-J18
    print("testar_getInventario: OK")

testar_getInventario()

def testar_moverJogador():
    _, jogador = criarJogador("Ana")

    assert moverJogador(jogador, 1, 0) == 0               # CT-J19
    assert jogador["posicao"] == (1, 0)                   # posição atualizada
    assert moverJogador(jogador, None, 1) == 2            # CT-J20
    assert moverJogador(None, 1, 0) == 2                  # CT-J21
    print("testar_moverJogador: OK")

testar_moverJogador()