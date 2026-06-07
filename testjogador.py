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

def testar_receberDanoJogador():
    jogador = {"nome": "Ana", "vida": 100}

    assert receberDanoJogador(jogador, 20) == 0      # CT-J22
    assert jogador["vida"] == 80

    jogador = {"nome": "Ana", "vida": 100}
    assert receberDanoJogador(jogador, -10) == 2     # CT-J23
    assert jogador["vida"] == 100

    assert receberDanoJogador(None, 10) == 2         # CT-J24
    print("testar_receberDanoJogador: OK")

testar_receberDanoJogador()


def testar_curarJogador():
    jogador = {"nome": "Ana", "vida": 50, "vida_max": 100}

    assert curarJogador(jogador, 20) == 0            # CT-J25
    assert jogador["vida"] == 70

    jogador = {"nome": "Ana", "vida": 100, "vida_max": 100}
    assert curarJogador(jogador, 20) == 1            # CT-J26

    assert curarJogador(jogador, -10) == 2           # CT-J27
    print("testar_curarJogador: OK")

testar_curarJogador()


def testar_ganharXP():
    jogador = {"nome": "Ana", "xp": 10}

    assert ganharXP(jogador, 20) == 0                # CT-J28
    assert jogador["xp"] == 30

    assert ganharXP(jogador, -5) == 2               # CT-J29
    print("testar_ganharXP: OK")

testar_ganharXP()


def testar_atualizarAtaque():
    jogador = {"nome": "Ana", "xp": 100, "ataque": 10}

    assert atualizarAtaque(jogador) == 0            # CT-J30
    assert jogador["ataque"] == 11

    assert atualizarAtaque(None) == 2               # CT-J31
    print("testar_atualizarAtaque: OK")

testar_atualizarAtaque()


def testar_adicionarItemJogador():
    jogador = {"nome": "Ana", "inventario": []}
    item = {"nome": "Poção", "tipo": "cura", "valor": 20}

    assert adicionarItemJogador(jogador, item) == 0     # CT-J32
    assert item in jogador["inventario"]

    jogador = {
        "nome": "Ana",
        "inventario": ["i1", "i2", "i3", "i4", "i5"]
    }

    assert adicionarItemJogador(jogador, item) == 1     # CT-J33
    assert adicionarItemJogador(None, item) == 2        # CT-J34

    print("testar_adicionarItemJogador: OK")

testar_adicionarItemJogador()


def testar_usarItemJogador():
    item = {"nome": "Poção", "tipo": "cura", "valor": 20}

    jogador = {
        "nome": "Ana",
        "vida": 50,
        "inventario": [item]
    }

    assert usarItemJogador(jogador, item) == 0          # CT-J35

    jogador = {
        "nome": "Ana",
        "inventario": []
    }

    assert usarItemJogador(jogador, item) == 1          # CT-J36
    assert usarItemJogador(None, item) == 2             # CT-J37

    print("testar_usarItemJogador: OK")

testar_usarItemJogador()

print("Todos os testes do módulo Jogador passaram.")