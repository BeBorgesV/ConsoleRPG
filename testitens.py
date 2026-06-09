from itens import (
    criarItem,
    getTipoItem,
    getValorItem,
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
    assert getTipoItem(id_item) == (0, "cura")
    assert getValorItem(id_item) == (0, 20)
    registrar_ok("CT-T01", "criar item de cura com dados válidos")

    # CT-T02
    codigo, id_item = criarItem("Espada", "ataque", 10)
    assert codigo == 0
    assert isinstance(id_item, int)
    assert getTipoItem(id_item) == (0, "ataque")
    assert getValorItem(id_item) == (0, 10)
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


def testar_getTipoItem():
    limpar_itens()

    # CT-T06
    codigo, id_item = criarItem("Poção", "cura", 20)
    assert codigo == 0
    assert getTipoItem(id_item) == (0, "cura")
    registrar_ok("CT-T06", "consultar tipo de item válido")

    # CT-T07
    assert getTipoItem(None) == (2, None)
    assert getTipoItem(-1) == (2, None)
    assert getTipoItem(9999) == (2, None)
    registrar_ok("CT-T07", "consultar tipo de item inválido")


def testar_getValorItem():
    limpar_itens()

    # CT-T08
    codigo, id_item = criarItem("Espada", "ataque", 10)
    assert codigo == 0
    assert getValorItem(id_item) == (0, 10)
    registrar_ok("CT-T08", "consultar valor de item válido")

    # CT-T09
    assert getValorItem(None) == (2, None)
    assert getValorItem(-1) == (2, None)
    assert getValorItem(9999) == (2, None)
    registrar_ok("CT-T09", "consultar valor de item inválido")


def testar_exportarEstadoItens():
    limpar_itens()

    # CT-T10
    criarItem("Poção", "cura", 20)
    criarItem("Espada", "ataque", 10)

    estado = exportarEstadoItens()

    assert isinstance(estado, list)
    assert len(estado) == 2
    assert estado[0] == {"nome": "Poção", "tipo": "cura", "valor": 20}
    assert estado[1] == {"nome": "Espada", "tipo": "ataque", "valor": 10}
    registrar_ok("CT-T10", "exportar estado dos itens")

    # CT-T11
    estado[0]["valor"] = 999
    novo_estado = exportarEstadoItens()
    assert novo_estado[0]["valor"] == 20
    registrar_ok("CT-T11", "exportar cópia sem alterar lista interna")


def testar_restaurarEstadoItens():
    limpar_itens()

    # CT-T12
    estado = [
        {"nome": "Poção", "tipo": "cura", "valor": 20},
        {"nome": "Espada", "tipo": "ataque", "valor": 10}
    ]

    assert restaurarEstadoItens(estado) == 0
    assert getTipoItem(0) == (0, "cura")
    assert getTipoItem(1) == (0, "ataque")
    assert getTipoItem(2) == (2, None)
    assert getTipoItem(0) == (0, "cura")
    assert getValorItem(0) == (0, 20)
    assert getTipoItem(1) == (0, "ataque")
    assert getValorItem(1) == (0, 10)
    registrar_ok("CT-T12", "restaurar estado válido dos itens")

    # CT-T13
    assert restaurarEstadoItens(None) == 2
    assert restaurarEstadoItens("estado inválido") == 2
    assert restaurarEstadoItens([{"nome": "Poção", "tipo": "cura"}]) == 2
    assert restaurarEstadoItens([{"nome": "Poção", "tipo": "velocidade", "valor": 10}]) == 2
    registrar_ok("CT-T13", "recusar estado inválido dos itens")


testar_criarItem()
testar_getTipoItem()
testar_getValorItem()
testar_exportarEstadoItens()
testar_restaurarEstadoItens()

print("Relatório final: todos os testes do módulo Item passaram.")
