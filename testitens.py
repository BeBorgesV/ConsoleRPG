from itens import (
    criarItem,
    getTipoItem,
    getValorItem,
    exportarEstadoItens,
    restaurarEstadoItens
)

total_testes = 0
testes_passaram = 0


def resultado(caso, descricao, condicao):
    global total_testes
    global testes_passaram

    total_testes += 1

    if condicao:
        testes_passaram += 1
        print(f"[OK] {caso}: {descricao}")
    else:
        print(f"[ERRO] {caso}: {descricao}")


def limpar_itens():
    restaurarEstadoItens([])


print("========================================")
print("      Testes do módulo Item")
print("========================================")


# ========================================
# criarItem
# ========================================

print("\n[ criarItem ]")

limpar_itens()

codigo, id_item = criarItem("Poção", "cura", 20)
resultado(
    "CT-T01",
    "criar item de cura com dados válidos",
    codigo == 0 and getTipoItem(id_item) == (0, "cura")
)

codigo, id_item = criarItem("Espada", "ataque", 10)
resultado(
    "CT-T02",
    "criar item de ataque com dados válidos",
    codigo == 0 and getTipoItem(id_item) == (0, "ataque")
)

resultado(
    "CT-T03",
    "criar item com nome vazio",
    criarItem("", "cura", 20) == (2, None)
)

resultado(
    "CT-T04",
    "criar item com tipo inválido",
    criarItem("Item estranho", "velocidade", 10) == (2, None)
)

resultado(
    "CT-T05",
    "criar item com valor inválido",
    criarItem("Poção", "cura", -10) == (2, None)
)


# ========================================
# getTipoItem
# ========================================

print("\n[ getTipoItem ]")

limpar_itens()

_, id_item = criarItem("Poção", "cura", 20)

resultado(
    "CT-T06",
    "consultar tipo de item válido",
    getTipoItem(id_item) == (0, "cura")
)

resultado(
    "CT-T07",
    "consultar tipo de item inválido",
    getTipoItem(None) == (2, None)
    and getTipoItem(-1) == (2, None)
    and getTipoItem(9999) == (2, None)
)


# ========================================
# getValorItem
# ========================================

print("\n[ getValorItem ]")

limpar_itens()

_, id_item = criarItem("Espada", "ataque", 10)

resultado(
    "CT-T08",
    "consultar valor de item válido",
    getValorItem(id_item) == (0, 10)
)

resultado(
    "CT-T09",
    "consultar valor de item inválido",
    getValorItem(None) == (2, None)
    and getValorItem(-1) == (2, None)
    and getValorItem(9999) == (2, None)
)


# ========================================
# exportarEstadoItens
# ========================================

print("\n[ exportarEstadoItens ]")

limpar_itens()

criarItem("Poção", "cura", 20)
criarItem("Espada", "ataque", 10)

estado = exportarEstadoItens()

resultado(
    "CT-T10",
    "exportar estado dos itens",
    len(estado) == 2
)

estado[0]["valor"] = 999

novo_estado = exportarEstadoItens()

resultado(
    "CT-T11",
    "exportar cópia sem alterar lista interna",
    novo_estado[0]["valor"] == 20
)


# ========================================
# restaurarEstadoItens
# ========================================

print("\n[ restaurarEstadoItens ]")

limpar_itens()

estado = [
    {"nome": "Poção", "tipo": "cura", "valor": 20},
    {"nome": "Espada", "tipo": "ataque", "valor": 10}
]

resultado(
    "CT-T12",
    "restaurar estado válido dos itens",
    restaurarEstadoItens(estado) == 0
    and getTipoItem(0) == (0, "cura")
    and getValorItem(0) == (0, 20)
    and getTipoItem(1) == (0, "ataque")
    and getValorItem(1) == (0, 10)
)

resultado(
    "CT-T13",
    "recusar estado inválido dos itens",
    restaurarEstadoItens(None) == 2
    and restaurarEstadoItens("estado inválido") == 2
    and restaurarEstadoItens([{"nome": "Poção", "tipo": "cura"}]) == 2
)

print("\n========================================")
print(f"Resultado: {testes_passaram}/{total_testes} testes passaram")
print("========================================")