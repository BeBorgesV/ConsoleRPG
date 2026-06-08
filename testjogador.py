from jogador import *

def testar_criarJogador():
    # CT-J01
    assert criarJogador("Ana") == 0

    # CT-J02
    assert criarJogador("") == 1

    # CT-J03
    assert criarJogador(None) == 2

    print("testar_criarJogador: OK")

testar_criarJogador()


def testar_getVida():
    criarJogador("Ana")

    # CT-J04
    assert getVida("Ana") == (0, 100)

    # CT-J05 / CT-J06
    assert getVida("Inexistente") == (2, None)
    assert getVida(None) == (2, None)

    print("testar_getVida: OK")

testar_getVida()


def testar_getXP():
    criarJogador("Ana")

    # CT-J07
    assert getXP("Ana") == (0, 0)

    # CT-J08 / CT-J09
    assert getXP("Inexistente") == (2, None)
    assert getXP(None) == (2, None)

    print("testar_getXP: OK")

testar_getXP()


def testar_getAtaque():
    criarJogador("Ana")

    # CT-J10
    assert getAtaque("Ana") == (0, 10)

    # CT-J11 / CT-J12
    assert getAtaque("Inexistente") == (2, None)

    print("testar_getAtaque: OK")

testar_getAtaque()


def testar_getPosicao():
    criarJogador("Ana")

    # CT-J13
    assert getPosicao("Ana") == (0, (0, 0))

    # CT-J14 / CT-J15
    assert getPosicao("Inexistente") == (2, None)

    print("testar_getPosicao: OK")

testar_getPosicao()


def testar_getInventario():
    criarJogador("Ana")

    # CT-J16
    assert getInventario("Ana") == (0, [])

    # CT-J17 / CT-J18
    assert getInventario("Inexistente") == (2, None)

    print("testar_getInventario: OK")

testar_getInventario()


def testar_moverJogador():
    criarJogador("Ana")

    # CT-J19
    assert moverJogador("Ana", 1, 0) == 0
    assert getPosicao("Ana") == (0, (1, 0))

    # CT-J20
    assert moverJogador("Ana", None, 1) == 2

    # CT-J21
    assert moverJogador("Inexistente", 1, 0) == 2

    print("testar_moverJogador: OK")

testar_moverJogador()


def testar_receberDanoJogador():
    criarJogador("Ana")

    # CT-J22
    assert receberDanoJogador("Ana", 20) == 0
    assert getVida("Ana") == (0, 80)

    # CT-J23
    assert receberDanoJogador("Ana", -10) == 2

    # CT-J24
    assert receberDanoJogador("Inexistente", 10) == 2

    print("testar_receberDanoJogador: OK")

testar_receberDanoJogador()


def testar_curarJogador():
    criarJogador("Ana")
    receberDanoJogador("Ana", 50)

    # CT-J25
    assert curarJogador("Ana", 20) == 0
    assert getVida("Ana") == (0, 70)

    # Completa a vida
    curarJogador("Ana", 100)

    # CT-J26
    assert curarJogador("Ana", 20) == 1

    # CT-J27 (Cura inválida)
    assert curarJogador("Ana", -10) == 2

    print("testar_curarJogador: OK")

testar_curarJogador()


def testar_ganharXP():
    criarJogador("Ana")

    # CT-J28
    assert ganharXP("Ana", 20) == 0
    assert getXP("Ana") == (0, 20)

    # CT-J29
    assert ganharXP("Ana", -5) == 2

    print("testar_ganharXP: OK")

testar_ganharXP()


def testar_atualizarAtaque():
    criarJogador("Ana")
    ganharXP("Ana", 100)

    # CT-J30
    assert atualizarAtaque("Ana") == 0
    assert getAtaque("Ana") == (0, 11)

    # CT-J31
    assert atualizarAtaque("Inexistente") == 2

    print("testar_atualizarAtaque: OK")

testar_atualizarAtaque()


def testar_adicionarItemJogador():
    criarJogador("Ana")

    item = {
        "nome": "Poção",
        "tipo": "cura",
        "valor": 20
    }

    # CT-J32
    assert adicionarItemJogador("Ana", item) == 0

    codigo, inventario = getInventario("Ana")
    assert item in inventario

    # Preenche inventário até o limite (já tem 1 item, adiciona mais 4)
    for i in range(4):
        adicionarItemJogador("Ana", {"nome": f"item{i}"})

    # CT-J33 - Limite excedido (5 itens)
    assert adicionarItemJogador("Ana", {"nome": "extra"}) == 1

    # CT-J34
    assert adicionarItemJogador("Inexistente", item) == 2

    print("testar_adicionarItemJogador: OK")

testar_adicionarItemJogador()


def testar_usarItemJogador():
    criarJogador("Ana")
    receberDanoJogador("Ana", 50)

    item = {
        "nome": "Poção",
        "tipo": "cura",
        "valor": 20
    }

    adicionarItemJogador("Ana", item)

    # CT-J35
    assert usarItemJogador("Ana", item) == 0
    assert getVida("Ana") == (0, 70)

    # CT-J36
    assert usarItemJogador("Ana", item) == 1

    # CT-J37
    assert usarItemJogador("Inexistente", item) == 2

    print("testar_usarItemJogador: OK")

testar_usarItemJogador()

print("Todos os testes do módulo Jogador passaram.")