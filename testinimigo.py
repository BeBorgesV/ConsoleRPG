from inimigos import (
    criarInimigo,
    getVidaInimigo,
    getAtaqueInimigo,
    receberDanoInimigo,
    inimigoVivo,
    verificaIdInimigoValido,
    exportarEstadoInimigos,
    restaurarEstadoInimigos
)


def registrar_ok(caso, descricao):
    print(f"OK - {caso}: {descricao}")


def limpar_inimigos():
    assert restaurarEstadoInimigos([]) == 0


def testar_criarInimigo():
    limpar_inimigos()

    # CT-I01
    codigo, id_inimigo = criarInimigo("Goblin", 50, 10)
    assert codigo == 0
    assert isinstance(id_inimigo, int)
    assert getVidaInimigo(id_inimigo) == (0, 50)
    assert getAtaqueInimigo(id_inimigo) == (0, 10)
    registrar_ok("CT-I01", "criar inimigo com dados válidos")

    # CT-I02
    assert criarInimigo("", 50, 10) == (2, None)
    registrar_ok("CT-I02", "criar inimigo com nome vazio")

    # CT-I03
    assert criarInimigo("Goblin", -10, 10) == (2, None)
    registrar_ok("CT-I03", "criar inimigo com vida inválida")

    # CT-I04
    assert criarInimigo("Goblin", 50, -5) == (2, None)
    registrar_ok("CT-I04", "criar inimigo com ataque inválido")

    # CT-I05
    assert criarInimigo("Goblin", 20, 40) == (1, None)
    registrar_ok("CT-I05", "criar inimigo com vida menor que ataque")

    # CT-I06
    assert criarInimigo("Dragão", 150, 60) == (1, None)
    registrar_ok("CT-I06", "criar inimigo com atributos acima do limite máximo")


def testar_getVidaInimigo():
    limpar_inimigos()

    # CT-I07
    codigo, id_inimigo = criarInimigo("Orc", 60, 20)
    assert codigo == 0
    assert getVidaInimigo(id_inimigo) == (0, 60)
    registrar_ok("CT-I07", "consultar vida de inimigo válido")

    # CT-I08
    assert getVidaInimigo(None) == (2, None)
    assert getVidaInimigo(-1) == (2, None)
    assert getVidaInimigo(9999) == (2, None)
    registrar_ok("CT-I08", "consultar vida de inimigo inválido")


def testar_getAtaqueInimigo():
    limpar_inimigos()

    # CT-I09
    codigo, id_inimigo = criarInimigo("Esqueleto", 40, 15)
    assert codigo == 0
    assert getAtaqueInimigo(id_inimigo) == (0, 15)
    registrar_ok("CT-I09", "consultar ataque de inimigo válido")

    # CT-I10
    assert getAtaqueInimigo(None) == (2, None)
    assert getAtaqueInimigo(-1) == (2, None)
    assert getAtaqueInimigo(9999) == (2, None)
    registrar_ok("CT-I10", "consultar ataque de inimigo inválido")


def testar_receberDanoInimigo():
    limpar_inimigos()

    # CT-I11
    codigo, id_inimigo = criarInimigo("Lobo", 50, 10)
    assert codigo == 0
    assert receberDanoInimigo(id_inimigo, 20) == 0
    assert getVidaInimigo(id_inimigo) == (0, 30)
    registrar_ok("CT-I11", "aplicar dano válido ao inimigo")

    # CT-I12
    codigo, id_inimigo = criarInimigo("Morcego", 50, 10)
    assert codigo == 0
    assert receberDanoInimigo(id_inimigo, 70) == 0
    assert getVidaInimigo(id_inimigo) == (0, 0)
    registrar_ok("CT-I12", "aplicar dano maior que a vida do inimigo")

    # CT-I13
    codigo, id_inimigo = criarInimigo("Aranha", 50, 10)
    assert codigo == 0
    assert receberDanoInimigo(id_inimigo, -10) == 2
    assert getVidaInimigo(id_inimigo) == (0, 50)
    registrar_ok("CT-I13", "aplicar dano inválido")

    # CT-I14
    assert receberDanoInimigo(None, 10) == 2
    assert receberDanoInimigo(-1, 10) == 2
    assert receberDanoInimigo(9999, 10) == 2
    registrar_ok("CT-I14", "aplicar dano em inimigo inválido")

    # CT-I15
    codigo, id_inimigo = criarInimigo("Zumbi", 50, 10)
    assert codigo == 0
    assert receberDanoInimigo(id_inimigo, 50) == 0
    assert receberDanoInimigo(id_inimigo, 10) == 1
    registrar_ok("CT-I15", "aplicar dano em inimigo já derrotado")


def testar_inimigoVivo():
    limpar_inimigos()

    # CT-I16
    codigo, id_inimigo = criarInimigo("Slime", 30, 10)
    assert codigo == 0
    assert inimigoVivo(id_inimigo) == (0, True)
    registrar_ok("CT-I16", "verificar inimigo vivo")

    # CT-I17
    codigo, id_inimigo = criarInimigo("Fantasma", 50, 10)
    assert codigo == 0
    assert receberDanoInimigo(id_inimigo, 50) == 0
    assert inimigoVivo(id_inimigo) == (0, False)
    registrar_ok("CT-I17", "verificar inimigo derrotado")

    # CT-I18
    assert inimigoVivo(None) == (2, None)
    assert inimigoVivo(-1) == (2, None)
    assert inimigoVivo(9999) == (2, None)
    registrar_ok("CT-I18", "verificar inimigo inválido")


def testar_verificaIdInimigoValido():
    limpar_inimigos()

    # CT-I19
    codigo, id_inimigo = criarInimigo("Goblin", 50, 10)
    assert codigo == 0
    assert verificaIdInimigoValido(id_inimigo) is True
    registrar_ok("CT-I19", "verificar id de inimigo válido")

    # CT-I20
    assert verificaIdInimigoValido(None) is False
    assert verificaIdInimigoValido(-1) is False
    assert verificaIdInimigoValido(9999) is False
    registrar_ok("CT-I20", "verificar id de inimigo inválido")


def testar_exportarEstadoInimigos():
    limpar_inimigos()

    # CT-I21
    criarInimigo("Goblin", 50, 10)
    criarInimigo("Orc", 60, 20)

    estado = exportarEstadoInimigos()

    assert isinstance(estado, list)
    assert len(estado) == 2
    assert estado[0] == {"nome": "Goblin", "vida": 50, "ataque": 10}
    assert estado[1] == {"nome": "Orc", "vida": 60, "ataque": 20}
    registrar_ok("CT-I21", "exportar estado dos inimigos")

    # CT-I22
    estado[0]["vida"] = 999
    novo_estado = exportarEstadoInimigos()
    assert novo_estado[0]["vida"] == 50
    registrar_ok("CT-I22", "exportar cópia sem alterar lista interna")


def testar_restaurarEstadoInimigos():
    limpar_inimigos()

    # CT-I23
    estado = [
        {"nome": "Goblin", "vida": 50, "ataque": 10},
        {"nome": "Orc", "vida": 0, "ataque": 20}
    ]

    assert restaurarEstadoInimigos(estado) == 0
    assert verificaIdInimigoValido(0) is True
    assert verificaIdInimigoValido(1) is True
    assert verificaIdInimigoValido(2) is False
    assert getVidaInimigo(0) == (0, 50)
    assert getVidaInimigo(1) == (0, 0)
    registrar_ok("CT-I23", "restaurar estado válido dos inimigos")

    # CT-I24
    assert restaurarEstadoInimigos(None) == 2
    assert restaurarEstadoInimigos("estado inválido") == 2
    assert restaurarEstadoInimigos([{"nome": "Goblin", "vida": 50}]) == 2
    assert restaurarEstadoInimigos([{"nome": "Goblin", "vida": -1, "ataque": 10}]) == 2
    registrar_ok("CT-I24", "recusar estado inválido dos inimigos")


testar_criarInimigo()
testar_getVidaInimigo()
testar_getAtaqueInimigo()
testar_receberDanoInimigo()
testar_inimigoVivo()
testar_verificaIdInimigoValido()
testar_exportarEstadoInimigos()
testar_restaurarEstadoInimigos()

print("Relatório final: todos os testes do módulo Inimigo passaram.")