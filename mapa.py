def criarMapa(estrutura=None):
    # CT-M03: parâmetro inválido (None)
    if estrutura is None:
        return 2, None

    # CT-M02: estrutura vazia
    if not isinstance(estrutura, dict) or len(estrutura) == 0:
        return 1, None

    # CT-M01: mapa criado com sucesso
    mapa = {
        "regioes": estrutura.get("regioes", []),
        "tamanho": estrutura.get("tamanho", (10, 10)),
        "posicao_inicial": estrutura.get("posicao_inicial", (0, 0))
    }
    return 0, mapa