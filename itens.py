def _tipoValido(tipo):
    tiposValidos = ("cura", "ataque")
    return tipo in tiposValidos


def criarItem(nome, tipo, valor):
    # CT-T03: criar item com nome vazio
    if nome is None or not isinstance(nome, str) or not nome.strip():
        return 2, None

    # CT-T04: criar item com tipo inválido
    if tipo is None or not isinstance(tipo, str) or not _tipoValido(tipo):
        return 2, None

    # CT-T05: criar item com valor inválido
    if valor is None or not isinstance(valor, (int, float)) or valor <= 0:
        return 2, None

    # CT-T01 e CT-T02: item criado com sucesso
    item = {
        "nome": nome.strip(),
        "tipo": tipo,
        "valor": valor
    }

    return 0, item


def aplicarItem(jogador, item):
    # CT-T09: aplicar item com jogador inválido
    if jogador is None or not isinstance(jogador, dict):
        return 2

    # CT-T10: aplicar item inválido
    if item is None or not isinstance(item, dict):
        return 2

    if "tipo" not in item or "valor" not in item:
        return 2

    tipo = item["tipo"]
    valor = item["valor"]

    if not isinstance(valor, (int, float)) or valor <= 0:
        return 2

    # CT-T11: aplicar item com tipo desconhecido
    if not _tipoValido(tipo):
        return 1

    # CT-T07: aplicar item de cura em jogador válido
    if tipo == "cura":
        if "vida" not in jogador:
            return 2

        # CT-T12: aplicar item de cura em jogador com vida cheia
        if jogador["vida"] >= 100:
            return 1

        jogador["vida"] += valor

        if jogador["vida"] > 100:
            jogador["vida"] = 100

        return 0

    # CT-T08: aplicar item de ataque em jogador válido
    if tipo == "ataque":
        if "ataque" not in jogador:
            return 2

        jogador["ataque"] += valor
        return 0

    return 1