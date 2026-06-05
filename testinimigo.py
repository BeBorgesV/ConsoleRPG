from inimigos import (
    criarInimigo,
    getVidaInimigo,
    getAtaqueInimigo,
    receberDanoInimigo,
    inimigoVivo
)


def testar_criarInimigo():
    # CT-I01
    codigo, inimigo = criarInimigo("Goblin", 50, 10)
    assert codigo == 0
    assert inimigo == {"nome": "Goblin", "vida": 50, "ataque": 10}

    # CT-I02
    assert criarInimigo("", 50, 10) == (2, None)

    # CT-I03
    assert criarInimigo("Goblin", -10, 10) == (2, None)

    # CT-I04
    assert criarInimigo("Goblin", 50, -5) == (2, None)

    # CT-I05
    assert criarInimigo("Goblin", 20, 40) == (1, None)

    # CT-I06
    assert criarInimigo("Dragão", 150, 60) == (1, None)


def testar_getVidaInimigo():
    # CT-I07
    inimigo = {"nome": "Goblin", "vida": 50, "ataque": 10}
    assert getVidaInimigo(inimigo) == (0, 50)

    # CT-I08
    assert getVidaInimigo(None) == (2, None)

    # CT-I09
    assert getVidaInimigo({"nome": "Goblin", "ataque": 10}) == (1, None)


def testar_getAtaqueInimigo():
    # CT-I10
    inimigo = {"nome": "Goblin", "vida": 50, "ataque": 10}
    assert getAtaqueInimigo(inimigo) == (0, 10)

    # CT-I11
    assert getAtaqueInimigo(None) == (2, None)

    # CT-I12
    assert getAtaqueInimigo({"nome": "Goblin", "vida": 50}) == (1, None)


def testar_receberDanoInimigo():
    # CT-I13
    inimigo = {"nome": "Goblin", "vida": 50, "ataque": 10}
    assert receberDanoInimigo(inimigo, 20) == 0
    assert inimigo["vida"] == 30

    # CT-I14
    inimigo = {"nome": "Goblin", "vida": 50, "ataque": 10}
    assert receberDanoInimigo(inimigo, 70) == 0
    assert inimigo["vida"] == 0

    # CT-I15
    inimigo = {"nome": "Goblin", "vida": 50, "ataque": 10}
    assert receberDanoInimigo(inimigo, -10) == 2
    assert inimigo["vida"] == 50

    # CT-I16
    assert receberDanoInimigo(None, 10) == 2

    # CT-I17
    inimigo = {"nome": "Goblin", "vida": 0, "ataque": 10}
    assert receberDanoInimigo(inimigo, 10) == 1


def testar_inimigoVivo():
    # CT-I18
    assert inimigoVivo(
        {"nome": "Goblin", "vida": 30, "ataque": 10}
    ) == (0, True)

    # CT-I19
    assert inimigoVivo(
        {"nome": "Goblin", "vida": 0, "ataque": 10}
    ) == (0, False)

    # CT-I20
    assert inimigoVivo(None) == (2, None)

    # CT-I21
    assert inimigoVivo(
        {"nome": "Goblin", "ataque": 10}
    ) == (1, None)


testar_criarInimigo()
testar_getVidaInimigo()
testar_getAtaqueInimigo()
testar_receberDanoInimigo()
testar_inimigoVivo()

print("Todos os testes do módulo Inimigo passaram.")