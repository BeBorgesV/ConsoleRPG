from itens import (
    criarItem,
    aplicarItem,
    verificaIdItemValido,
    exportarEstadoItens,
    restaurarEstadoItens
)


def registrar_ok(caso, descricao):
    print(f"OK - {caso}: {descricao}")


def limpar_itens():
    assert restaurarEstadoItens([]) == 0


def testar_criarItem():
    limpar_itens()

    # CT-T01
    codigo, id_item = criarItem("Poção", "cura", 20)
    assert codigo == 0
    assert isinstance(id_item, int)
    assert verificaIdItemValido(id_item) is True
    registrar_ok("CT-T01", "criar item de cura com dados válidos")

    # CT-T02
    codigo, id_item = criarItem("Espada", "ataque", 10)
    assert codigo == 0
    assert isinstance(id_item, int)
    assert verificaIdItemValido(id_item) is True
    registrar_ok("CT-T02", "criar item de ataque com dados válidos")

    # CT-T03
    assert criarItem("", "cura", 20) == (2, None)
    registrar_ok("CT-T03", "criar item com nome vazio")

    # CT-T04
    assert criarItem("Item estranho", "velocidade", 10) == (2, None)
    registrar_ok("CT-T04", "criar item com tipo inválido")

    # CT-T05
    assert criarItem("Poção", "cura", -10) == (2, None)
    registrar_ok("CT-T05", "criar item com valor inválido")


def testar_aplicarItem():
    limpar_itens()

    # CT-T07
    jogador = {"nome": "Ana", "vida": 50, "ataque": 10}
    codigo, id_item = criarItem("Poção", "cura", 20)
    assert codigo == 0
    assert aplicarItem(jogador, id_item) == 0
    assert jogador["vida"] == 70
    registrar_ok("CT-T07", "aplicar item de cura em jogador válido")

    # CT-T08
    jogador = {"nome": "Ana", "vida": 50, "ataque": 10}
    codigo, id_item = criarItem("Espada", "ataque", 5)
    assert codigo == 0
    assert aplicarItem(jogador, id_item) == 0
    assert jogador["ataque"] == 15
    registrar_ok("CT-T08", "aplicar item de ataque em jogador válido")

    # CT-T09
    codigo, id_item = criarItem("Poção", "cura", 20)
    assert codigo == 0
    assert aplicarItem(None, id_item) == 2
    registrar_ok("CT-T09", "aplicar item com jogador inválido")

    # CT-T10
    jogador = {"nome": "Ana", "vida": 50, "ataque": 10}
    assert aplicarItem(jogador, None) == 2
    assert aplicarItem(jogador, -1) == 2
    assert aplicarItem(jogador, 9999) == 2
    registrar_ok("CT-T10", "aplicar item inválido")

    # CT-T11
    estado_invalido = [
        {"nome": "Item estranho", "tipo": "velocidade", "valor": 10}
    ]
    assert restaurarEstadoItens(estado_invalido) == 2
    registrar_ok("CT-T11", "impedir restauração de item com tipo desconhecido")

    # CT-T12
    jogador = {"nome": "Ana", "vida": 100, "ataque": 10}
    codigo, id_item = criarItem("Poção", "cura", 20)
    assert codigo == 0
    assert aplicarItem(jogador, id_item) == 1
    assert jogador["vida"] == 100
    registrar_ok("CT-T12", "aplicar item de cura em jogador com vida cheia")


def testar_verificaIdItemValido():
    limpar_itens()

    # CT-T13
    codigo, id_item = criarItem("Poção", "cura", 20)
    assert codigo == 0
    assert verificaIdItemValido(id_item) is True
    registrar_ok("CT-T13", "verificar id de item válido")

    # CT-T14
    assert verificaIdItemValido(None) is False
    assert verificaIdItemValido(-1) is False
    assert verificaIdItemValido(9999) is False
    registrar_ok("CT-T14", "verificar id de item inválido")


def testar_exportarEstadoItens():
    limpar_itens()

    # CT-T15
    criarItem("Poção", "cura", 20)
    criarItem("Espada", "ataque", 10)

    estado = exportarEstadoItens()

    assert isinstance(estado, list)
    assert len(estado) == 2
    assert estado[0] == {"nome": "Poção", "tipo": "cura", "valor": 20}
    assert estado[1] == {"nome": "Espada", "tipo": "ataque", "valor": 10}
    registrar_ok("CT-T15", "exportar estado dos itens")

    # CT-T16
    estado[0]["valor"] = 999
    novo_estado = exportarEstadoItens()
    assert novo_estado[0]["valor"] == 20
    registrar_ok("CT-T16", "exportar cópia sem alterar lista interna")


def testar_restaurarEstadoItens():
    limpar_itens()

    # CT-T17
    estado = [
        {"nome": "Poção", "tipo": "cura", "valor": 20},
        {"nome": "Espada", "tipo": "ataque", "valor": 10}
    ]

    assert restaurarEstadoItens(estado) == 0
    assert verificaIdItemValido(0) is True
    assert verificaIdItemValido(1) is True
    assert verificaIdItemValido(2) is False
    registrar_ok("CT-T17", "restaurar estado válido dos itens")

    # CT-T18
    assert restaurarEstadoItens(None) == 2
    assert restaurarEstadoItens("estado inválido") == 2
    assert restaurarEstadoItens([{"nome": "Poção", "tipo": "cura"}]) == 2
    assert restaurarEstadoItens([{"nome": "Poção", "tipo": "velocidade", "valor": 10}]) == 2
    registrar_ok("CT-T18", "recusar estado inválido dos itens")


testar_criarItem()
testar_aplicarItem()
testar_verificaIdItemValido()
testar_exportarEstadoItens()
testar_restaurarEstadoItens()

print("Relatório final: todos os testes do módulo Item passaram.")