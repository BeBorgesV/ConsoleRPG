from itens import criarItem, aplicarItem


def testar_criarItem():
    # CT-T01
    codigo, item = criarItem("Poção", "cura", 20)
    assert codigo == 0
    assert item == {
        "nome": "Poção",
        "tipo": "cura",
        "valor": 20
    }

    # CT-T02
    codigo, item = criarItem("Espada", "ataque", 10)
    assert codigo == 0
    assert item == {
        "nome": "Espada",
        "tipo": "ataque",
        "valor": 10
    }

    # CT-T03
    assert criarItem("", "cura", 20) == (2, None)

    # CT-T04
    assert criarItem("Item estranho", "velocidade", 10) == (2, None)

    # CT-T05
    assert criarItem("Poção", "cura", -10) == (2, None)


def testar_aplicarItem():
    # CT-T07
    jogador = {"nome": "Ana", "vida": 50, "ataque": 10}
    item = {"nome": "Poção", "tipo": "cura", "valor": 20}

    assert aplicarItem(jogador, item) == 0
    assert jogador["vida"] == 70

    # CT-T08
    jogador = {"nome": "Ana", "vida": 50, "ataque": 10}
    item = {"nome": "Espada", "tipo": "ataque", "valor": 5}

    assert aplicarItem(jogador, item) == 0
    assert jogador["ataque"] == 15

    # CT-T09
    item = {"nome": "Poção", "tipo": "cura", "valor": 20}
    assert aplicarItem(None, item) == 2

    # CT-T10
    jogador = {"nome": "Ana", "vida": 50, "ataque": 10}
    assert aplicarItem(jogador, None) == 2

    # CT-T11
    jogador = {"nome": "Ana", "vida": 50, "ataque": 10}
    item = {
        "nome": "Item estranho",
        "tipo": "velocidade",
        "valor": 10
    }

    assert aplicarItem(jogador, item) == 1

    # CT-T12
    jogador = {"nome": "Ana", "vida": 100, "ataque": 10}
    item = {"nome": "Poção", "tipo": "cura", "valor": 20}

    assert aplicarItem(jogador, item) == 1


testar_criarItem()
testar_aplicarItem()

print("Todos os testes do módulo Item passaram.")