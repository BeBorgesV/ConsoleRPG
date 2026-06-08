_VIDA_MAX = 100
_ATAQUE_MAX = 50


def criarInimigo(nome, vida, ataque):
    # CT-I02: nome vazio
    if nome is None or not isinstance(nome, str) or not nome.strip():
        return 2, None

    # CT-I03: vida inválida
    if vida is None or not isinstance(vida, (int, float)) or vida <= 0:
        return 2, None

    # CT-I04: ataque inválido
    if ataque is None or not isinstance(ataque, (int, float)) or ataque <= 0:
        return 2, None

    # CT-I05: vida menor que ataque
    if vida < ataque:
        return 1, None

    # CT-I06: atributos acima do limite máximo
    if vida > _VIDA_MAX or ataque > _ATAQUE_MAX:
        return 1, None

    # CT-I01: inimigo criado com sucesso
    inimigo = {
        "nome": nome.strip(),
        "vida": vida,
        "ataque": ataque
    }

    return 0, inimigo


def getVidaInimigo(inimigo):
    # CT-I08: inimigo inválido
    if inimigo is None:
        return 2, None

    # CT-I09: inimigo sem campo vida
    if "vida" not in inimigo:
        return 1, None

    # CT-I07: vida retornada com sucesso
    return 0, inimigo["vida"]


def getAtaqueInimigo(inimigo):
    # CT-I11: inimigo inválido
    if inimigo is None:
        return 2, None

    # CT-I12: inimigo sem campo ataque
    if "ataque" not in inimigo:
        return 1, None

    # CT-I10: ataque retornado com sucesso
    return 0, inimigo["ataque"]


def receberDanoInimigo(inimigo, dano):
    # CT-I16: inimigo inválido
    if inimigo is None:
        return 2

    # CT-I15: dano inválido
    if dano is None or not isinstance(dano, (int, float)) or dano < 0:
        return 2

    if "vida" not in inimigo:
        return 1

    # CT-I17: inimigo já derrotado
    if inimigo["vida"] <= 0:
        return 1

    # CT-I13 e CT-I14: dano aplicado
    inimigo["vida"] -= dano

    if inimigo["vida"] < 0:
        inimigo["vida"] = 0

    return 0


def inimigoVivo(inimigo):
    # CT-I20: inimigo inválido
    if inimigo is None:
        return 2, None

    # CT-I21: inimigo sem campo vida
    if "vida" not in inimigo:
        return 1, None

    # CT-I18: inimigo vivo
    if inimigo["vida"] > 0:
        return 0, True

    # CT-I19: inimigo derrotado
    return 0, False