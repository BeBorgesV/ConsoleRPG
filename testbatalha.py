import inimigos as inimigos_mod
import jogador as jogador_mod
from batalha import calcularDano, iniciarBatalha, turno, verificarFimBatalha, executarBatalha, TURNO_JOGADOR, TURNO_INIMIGO


def criarJogadorTeste():
    # Registra no estado interno do modulo jogador
    jogador_mod.criarJogador("Jogador")
    return {"nome": "Jogador", "posicao": (0, 0)}


def criarInimigoTeste():
    # Cria via modulo inimigos e retorna o id_inimigo (int)
    inimigos_mod.restaurarEstadoInimigos([])
    _, id_inimigo = inimigos_mod.criarInimigo("Goblin", 50, 5)
    return id_inimigo


# CT-B01 - Calcular dano com ataque válido
# Resultado esperado: dano calculado. Retorno 0.
def test_calcularDano_com_ataque_valido():
    codigo, dano = calcularDano(10)

    assert codigo == 0
    assert dano > 0


# CT-B02 - Calcular dano com ataque inválido
# Resultado esperado: dano não calculado. Retorno 2.
def test_calcularDano_com_ataque_invalido():
    assert calcularDano(-5) == (2, None)
    assert calcularDano(0) == (2, None)
    assert calcularDano(None) == (2, None)
    assert calcularDano("dez") == (2, None)


# CT-B03 - Calcular dano com erro de regra
# Resultado esperado: dano não calculado por resultado inválido. Retorno 1.
def test_calcularDano_com_erro_de_regra():
    codigo, dano = calcularDano(0.1)

    assert codigo == 1
    assert dano is None


# CT-B04 - Iniciar batalha com jogador e inimigo válidos
# Resultado esperado: batalha criada, ativa e começando no turno do jogador. Retorno 0.
def test_iniciarBatalha_com_dados_validos():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()

    codigo, batalha = iniciarBatalha(jogador, inimigo)

    assert codigo == 0
    assert batalha["turno"] == TURNO_JOGADOR
    assert batalha["ativa"] is True
    assert batalha["vencedor"] is None


# CT-B05 - Iniciar batalha com parâmetro inválido
# Resultado esperado: batalha não criada. Retorno 2.
def test_iniciarBatalha_com_parametro_invalido():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()

    assert iniciarBatalha(None, inimigo) == (2, None)
    assert iniciarBatalha(jogador, None) == (2, None)


# CT-B06 - Iniciar batalha com combatente morto
# Resultado esperado: batalha não criada por regra do jogo. Retorno 1.
def test_iniciarBatalha_com_combatente_morto():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    inimigos_mod.receberDanoInimigo(inimigo, 50)  # zera a vida do inimigo

    assert iniciarBatalha(jogador, inimigo) == (1, None)


# CT-B07 - Executar turno do jogador atacando
# Resultado esperado: inimigo recebe dano e turno passa para o inimigo. Retorno 0.
def test_turno_jogador_atacando(monkeypatch):
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    batalha = {
        "turno": TURNO_JOGADOR,
        "ativa": True,
        "vencedor": None
    }

    monkeypatch.setattr("builtins.input", lambda mensagem="": "1")

    codigo = turno(jogador, inimigo, batalha)

    _, vida_inimigo = inimigos_mod.getVidaInimigo(inimigo)
    assert codigo == 0
    assert vida_inimigo < 50
    assert batalha["turno"] == TURNO_INIMIGO


# CT-B08 - Executar turno do inimigo
# Resultado esperado: jogador recebe dano e turno passa para o jogador. Retorno 0.
def test_turno_inimigo_atacando():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    batalha = {
        "turno": TURNO_INIMIGO,
        "ativa": True,
        "vencedor": None
    }

    codigo = turno(jogador, inimigo, batalha)

    _, vida_jogador = jogador_mod.getVida("Jogador")
    assert codigo == 0
    assert vida_jogador < 100
    assert batalha["turno"] == TURNO_JOGADOR


# CT-B09 - Executar turno com ação inválida
# Resultado esperado: turno não executado. Retorno 2.
def test_turno_com_acao_invalida(monkeypatch):
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    batalha = {
        "turno": TURNO_JOGADOR,
        "ativa": True,
        "vencedor": None
    }

    monkeypatch.setattr("builtins.input", lambda mensagem="": "9")

    codigo = turno(jogador, inimigo, batalha)

    assert codigo == 2
    assert batalha["turno"] == TURNO_JOGADOR


# CT-B10 - Executar turno com parâmetro inválido
# Resultado esperado: turno não executado. Retorno 2.
def test_turno_com_parametro_invalido():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    batalha = {
        "turno": TURNO_JOGADOR,
        "ativa": True,
        "vencedor": None
    }

    assert turno(None, inimigo, batalha) == 2
    assert turno(jogador, None, batalha) == 2
    assert turno(jogador, inimigo, None) == 2


# CT-B11 - Executar turno com estrutura de batalha inválida
# Resultado esperado: turno não executado por erro de regra. Retorno 1.
def test_turno_com_batalha_sem_turno():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    batalha = {
        "ativa": True,
        "vencedor": None
    }

    assert turno(jogador, inimigo, batalha) == 1


# CT-B12 - Verificar fim com os dois combatentes vivos
# Resultado esperado: batalha continua ativa. Retorno 0.
def test_verificarFimBatalha_sem_vencedor():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    batalha = {
        "turno": TURNO_JOGADOR,
        "ativa": True,
        "vencedor": None
    }

    codigo = verificarFimBatalha(jogador, inimigo, batalha)

    assert codigo == 0
    assert batalha["ativa"] is True
    assert batalha["vencedor"] is None


# CT-B13 - Verificar fim com inimigo derrotado
# Resultado esperado: batalha encerrada com jogador vencedor. Retorno 0.
def test_verificarFimBatalha_com_jogador_vencedor():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    inimigos_mod.receberDanoInimigo(inimigo, 50)  # zera a vida do inimigo
    batalha = {
        "turno": TURNO_JOGADOR,
        "ativa": True,
        "vencedor": None
    }

    codigo = verificarFimBatalha(jogador, inimigo, batalha)

    assert codigo == 0
    assert batalha["ativa"] is False
    assert batalha["vencedor"] == "jogador"


# CT-B14 - Verificar fim com jogador derrotado
# Resultado esperado: batalha encerrada com inimigo vencedor. Retorno 0.
def test_verificarFimBatalha_com_inimigo_vencedor():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    jogador_mod.receberDanoJogador("Jogador", 100)  # zera a vida do jogador
    batalha = {
        "turno": TURNO_JOGADOR,
        "ativa": True,
        "vencedor": None
    }

    codigo = verificarFimBatalha(jogador, inimigo, batalha)

    assert codigo == 0
    assert batalha["ativa"] is False
    assert batalha["vencedor"] == "inimigo"


# CT-B15 - Verificar fim com parâmetro inválido
# Resultado esperado: verificação não realizada. Retorno 2.
def test_verificarFimBatalha_com_parametro_invalido():
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()
    batalha = {
        "turno": TURNO_JOGADOR,
        "ativa": True,
        "vencedor": None
    }

    assert verificarFimBatalha(None, inimigo, batalha) == 2
    assert verificarFimBatalha(jogador, None, batalha) == 2
    assert verificarFimBatalha(jogador, inimigo, None) == 2


# CT-B16 - Executar batalha completa
# Resultado esperado: batalha termina com algum vencedor. Retorno 0.
def test_executarBatalha_com_batalha_completa(monkeypatch):
    jogador = criarJogadorTeste()
    inimigo = criarInimigoTeste()

    monkeypatch.setattr("builtins.input", lambda mensagem="": "1")

    codigo, vencedor = executarBatalha(jogador, inimigo)

    assert codigo == 0
    assert vencedor == "jogador" or vencedor == "inimigo"
