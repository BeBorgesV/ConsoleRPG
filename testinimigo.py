from inimigos import (
    criarInimigo,
    getNomeInimigo,
    getVidaInimigo,
    getAtaqueInimigo,
    receberDanoInimigo,
    inimigoVivo,
    exportarEstadoInimigos,
    restaurarEstadoInimigos
)


total_testes = 0
testes_passaram = 0


def _resultado(caso, descricao, condicao):
    global total_testes
    global testes_passaram

    total_testes += 1

    if condicao:
        testes_passaram += 1
        print(f"    [OK] {caso}: {descricao}")
    else:
        print(f"    [ERRO] {caso}: {descricao}")


def limpar_inimigos():
    restaurarEstadoInimigos([])


def testar_criarInimigo():
    print("\n[ criarInimigo ]")
    limpar_inimigos()

    # CT-I01
    codigo, id_inimigo = criarInimigo("Goblin", 50, 10)
    _resultado(
        "CT-I01",
        "criar inimigo com dados válidos",
        codigo == 0
        and isinstance(id_inimigo, int)
        and getNomeInimigo(id_inimigo) == (0, "Goblin")
        and getVidaInimigo(id_inimigo) == (0, 50)
        and getAtaqueInimigo(id_inimigo) == (0, 10)
    )

    # CT-I02
    _resultado(
        "CT-I02",
        "criar inimigo com nome vazio",
        criarInimigo("", 50, 10) == (2, None)
    )

    # CT-I03
    _resultado(
        "CT-I03",
        "criar inimigo com vida inválida",
        criarInimigo("Goblin", -10, 10) == (2, None)
    )

    # CT-I04
    _resultado(
        "CT-I04",
        "criar inimigo com ataque inválido",
        criarInimigo("Goblin", 50, -5) == (2, None)
    )

    # CT-I05
    _resultado(
        "CT-I05",
        "criar inimigo com vida menor que ataque",
        criarInimigo("Goblin", 20, 40) == (1, None)
    )

    # CT-I06
    _resultado(
        "CT-I06",
        "criar inimigo com atributos acima do limite máximo",
        criarInimigo("Dragão", 150, 60) == (1, None)
    )


def testar_getNomeInimigo():
    print("\n[ getNomeInimigo ]")
    limpar_inimigos()

    # CT-I07
    codigo, id_inimigo = criarInimigo("Orc", 60, 20)
    _resultado(
        "CT-I07",
        "consultar nome de inimigo válido",
        codigo == 0 and getNomeInimigo(id_inimigo) == (0, "Orc")
    )

    # CT-I08
    _resultado(
        "CT-I08",
        "consultar nome de inimigo inválido",
        getNomeInimigo(None) == (2, None)
        and getNomeInimigo(-1) == (2, None)
        and getNomeInimigo(9999) == (2, None)
    )


def testar_getVidaInimigo():
    print("\n[ getVidaInimigo ]")
    limpar_inimigos()

    # CT-I09
    codigo, id_inimigo = criarInimigo("Orc", 60, 20)
    _resultado(
        "CT-I09",
        "consultar vida de inimigo válido",
        codigo == 0 and getVidaInimigo(id_inimigo) == (0, 60)
    )

    # CT-I10
    _resultado(
        "CT-I10",
        "consultar vida de inimigo inválido",
        getVidaInimigo(None) == (2, None)
        and getVidaInimigo(-1) == (2, None)
        and getVidaInimigo(9999) == (2, None)
    )


def testar_getAtaqueInimigo():
    print("\n[ getAtaqueInimigo ]")
    limpar_inimigos()

    # CT-I11
    codigo, id_inimigo = criarInimigo("Esqueleto", 40, 15)
    _resultado(
        "CT-I11",
        "consultar ataque de inimigo válido",
        codigo == 0 and getAtaqueInimigo(id_inimigo) == (0, 15)
    )

    # CT-I12
    _resultado(
        "CT-I12",
        "consultar ataque de inimigo inválido",
        getAtaqueInimigo(None) == (2, None)
        and getAtaqueInimigo(-1) == (2, None)
        and getAtaqueInimigo(9999) == (2, None)
    )


def testar_receberDanoInimigo():
    print("\n[ receberDanoInimigo ]")
    limpar_inimigos()

    # CT-I13
    codigo, id_inimigo = criarInimigo("Lobo", 50, 10)
    retorno = receberDanoInimigo(id_inimigo, 20)
    _resultado(
        "CT-I13",
        "aplicar dano válido ao inimigo",
        codigo == 0
        and retorno == 0
        and getVidaInimigo(id_inimigo) == (0, 30)
    )

    # CT-I14
    codigo, id_inimigo = criarInimigo("Morcego", 50, 10)
    retorno = receberDanoInimigo(id_inimigo, 70)
    _resultado(
        "CT-I14",
        "aplicar dano maior que a vida do inimigo",
        codigo == 0
        and retorno == 0
        and getVidaInimigo(id_inimigo) == (0, 0)
    )

    # CT-I15
    codigo, id_inimigo = criarInimigo("Aranha", 50, 10)
    retorno = receberDanoInimigo(id_inimigo, -10)
    _resultado(
        "CT-I15",
        "aplicar dano inválido",
        codigo == 0
        and retorno == 2
        and getVidaInimigo(id_inimigo) == (0, 50)
    )

    # CT-I16
    _resultado(
        "CT-I16",
        "aplicar dano em inimigo inválido",
        receberDanoInimigo(None, 10) == 2
        and receberDanoInimigo(-1, 10) == 2
        and receberDanoInimigo(9999, 10) == 2
    )

    # CT-I17
    codigo, id_inimigo = criarInimigo("Zumbi", 50, 10)
    primeiro_retorno = receberDanoInimigo(id_inimigo, 50)
    segundo_retorno = receberDanoInimigo(id_inimigo, 10)
    _resultado(
        "CT-I17",
        "aplicar dano em inimigo já derrotado",
        codigo == 0
        and primeiro_retorno == 0
        and segundo_retorno == 1
    )


def testar_inimigoVivo():
    print("\n[ inimigoVivo ]")
    limpar_inimigos()

    # CT-I18
    codigo, id_inimigo = criarInimigo("Slime", 30, 10)
    _resultado(
        "CT-I18",
        "verificar inimigo vivo",
        codigo == 0 and inimigoVivo(id_inimigo) == (0, True)
    )

    # CT-I19
    codigo, id_inimigo = criarInimigo("Fantasma", 50, 10)
    retorno_dano = receberDanoInimigo(id_inimigo, 50)
    _resultado(
        "CT-I19",
        "verificar inimigo derrotado",
        codigo == 0
        and retorno_dano == 0
        and inimigoVivo(id_inimigo) == (0, False)
    )

    # CT-I20
    _resultado(
        "CT-I20",
        "verificar inimigo inválido",
        inimigoVivo(None) == (2, None)
        and inimigoVivo(-1) == (2, None)
        and inimigoVivo(9999) == (2, None)
    )


def testar_exportarEstadoInimigos():
    print("\n[ exportarEstadoInimigos ]")
    limpar_inimigos()

    # CT-I21
    criarInimigo("Goblin", 50, 10)
    criarInimigo("Orc", 60, 20)
    estado = exportarEstadoInimigos()
    _resultado(
        "CT-I21",
        "exportar estado dos inimigos",
        isinstance(estado, list)
        and len(estado) == 2
        and estado[0] == {"nome": "Goblin", "vida": 50, "ataque": 10}
        and estado[1] == {"nome": "Orc", "vida": 60, "ataque": 20}
    )

    # CT-I22
    estado[0]["vida"] = 999
    novo_estado = exportarEstadoInimigos()
    _resultado(
        "CT-I22",
        "exportar cópia sem alterar lista interna",
        novo_estado[0]["vida"] == 50
    )


def testar_restaurarEstadoInimigos():
    print("\n[ restaurarEstadoInimigos ]")
    limpar_inimigos()

    # CT-I23
    estado = [
        {"nome": "Goblin", "vida": 50, "ataque": 10},
        {"nome": "Orc", "vida": 0, "ataque": 20}
    ]

    retorno = restaurarEstadoInimigos(estado)
    _resultado(
        "CT-I23",
        "restaurar estado válido dos inimigos",
        retorno == 0
        and getNomeInimigo(0) == (0, "Goblin")
        and getVidaInimigo(0) == (0, 50)
        and getAtaqueInimigo(0) == (0, 10)
        and getNomeInimigo(1) == (0, "Orc")
        and getVidaInimigo(1) == (0, 0)
        and getAtaqueInimigo(1) == (0, 20)
        and getVidaInimigo(2) == (2, None)
    )

    # CT-I24
    _resultado(
        "CT-I24",
        "recusar estado inválido dos inimigos",
        restaurarEstadoInimigos(None) == 2
        and restaurarEstadoInimigos("estado inválido") == 2
        and restaurarEstadoInimigos([{"nome": "Goblin", "vida": 50}]) == 2
        and restaurarEstadoInimigos([{"nome": "Goblin", "vida": -1, "ataque": 10}]) == 2
    )


print("========================================")
print("      Testes do módulo Inimigo")
print("========================================")

testar_criarInimigo()
testar_getNomeInimigo()
testar_getVidaInimigo()
testar_getAtaqueInimigo()
testar_receberDanoInimigo()
testar_inimigoVivo()
testar_exportarEstadoInimigos()
testar_restaurarEstadoInimigos()

print("\n========================================")
print(f"Resultado: {testes_passaram}/{total_testes} testes passaram")
print("========================================")