from batalha import *

def testar_calcularDano():

    assert calcularDano(10)[0] == 0

    codigo, dano = calcularDano(10)
    assert dano > 0

    assert calcularDano(-5) == (2, None)

    assert calcularDano(None) == (2, None)


def testar_iniciarBatalha():

    jogador = {
        "nome": "Jogador",
        "vida": 100,
        "ataque": 10
    }

    inimigo = {
        "nome": "Goblin",
        "vida": 50,
        "ataque": 5
    }

    codigo, batalha = iniciarBatalha(jogador, inimigo)

    assert codigo == 0

    # 0 = turno do jogador
    assert batalha["turno"] == 0

    assert iniciarBatalha(None, inimigo) == (2, None)

    assert iniciarBatalha(jogador, None) == (2, None)

    inimigoMorto = {
        "nome": "Goblin",
        "vida": 0,
        "ataque": 5
    }

    assert iniciarBatalha(jogador, inimigoMorto) == (1, None)


def testar_turnoJogador():

    jogador = {
        "nome": "Jogador",
        "vida": 100,
        "ataque": 10
    }

    inimigo = {
        "nome": "Goblin",
        "vida": 50,
        "ataque": 5
    }

    batalha = {
        "turno": 0
    }

    codigo = turnoJogador(jogador, inimigo, batalha)

    assert codigo == 0
    assert inimigo["vida"] < 50

    # 1 = turno do inimigo
    batalha["turno"] = 1

    assert turnoJogador(jogador, inimigo, batalha) == 1

    assert turnoJogador(None, inimigo, batalha) == 2


def testar_turnoInimigo():

    jogador = {
        "nome": "Jogador",
        "vida": 100,
        "ataque": 10
    }

    inimigo = {
        "nome": "Goblin",
        "vida": 50,
        "ataque": 5
    }

    batalha = {
        "turno": 1
    }

    codigo = turnoInimigo(jogador, inimigo, batalha)

    assert codigo == 0
    assert jogador["vida"] < 100

    batalha["turno"] = 0

    assert turnoInimigo(jogador, inimigo, batalha) == 1

    assert turnoInimigo(jogador, None, batalha) == 2