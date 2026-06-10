

import builtins
import os
import random

import batalha
import inimigos
import itens
import jogador
import salvar
from mapa import (
    alocarInimigoMapa,
    alocarItemMapa,
    criarMapa,
    descreverPosicaoMapa,
    getInimigoMapa,
    getItemMapa,
    getPosicaoInicialMapa,
    inimigoFinalMapa,
    limparEventoMapa,
    moverJogadorMapa,
    registrarInimigoDerrotadoMapa,
    renderizarMapa
)


total_testes = 0
testes_passaram = 0


# ==================================================
# Funções auxiliares do relatório
# ==================================================

def _resultado(caso, descricao, condicao):
    global total_testes
    global testes_passaram

    total_testes += 1

    if condicao:
        testes_passaram += 1
        print(f"    [OK] {caso}: {descricao}")
    else:
        print(f"    [ERRO] {caso}: {descricao}")


def _secao(titulo):
    print(f"\n[ {titulo} ]")


def _limpar_save():
    if os.path.exists("save.json"):
        os.remove("save.json")


def _resetar_itens_inimigos():
    itens.restaurarEstadoItens([])
    inimigos.restaurarEstadoInimigos([])


def _criar_jogador_estado(nome="HeroiIntegrado", vida=100, xp=0, ataque=10, inventario=None):
    if inventario is None:
        inventario = []

    dados = {
        "nome": nome,
        "vida": vida,
        "vida_max": 100,
        "xp": xp,
        "ataque": ataque,
        "vivo": vida > 0,
        "inventario": list(inventario)
    }

    status = jogador.restaurarJogador(dados)
    if status != 0:
        return None

    retorno = dados.copy()
    return retorno


def _preparar_entidades_teste(mapa):
    """Prepara entidades iniciais para testes de save/load, sem acessar listas internas."""
    itens.restaurarEstadoItens([])
    inimigos.restaurarEstadoInimigos([])

    codigo_item, id_item = itens.criarItem("Pocao simples", "cura", 25)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Lobo da trilha", 35, 7)

    if codigo_item != 0 or codigo_inimigo != 0:
        return 1

    if alocarItemMapa(mapa, 2, 12, id_item) != 0:
        return 1

    if alocarInimigoMapa(mapa, 5, 11, id_inimigo, False) != 0:
        return 1

    return 0


class SimularInput:
    def __init__(self, respostas):
        self.respostas = list(respostas)
        self.indice = 0
        self.input_original = builtins.input

    def __enter__(self):
        def fake_input(_mensagem=""):
            if self.indice >= len(self.respostas):
                return ""
            resposta = self.respostas[self.indice]
            self.indice += 1
            return resposta

        builtins.input = fake_input
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        builtins.input = self.input_original


class SimularRandom:
    def __init__(self, uniforme=1.0, aleatorio=1.0):
        self.uniforme = uniforme
        self.aleatorio = aleatorio
        self.uniform_original = random.uniform
        self.random_original = random.random

    def __enter__(self):
        random.uniform = lambda _a, _b: self.uniforme
        random.random = lambda: self.aleatorio
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        random.uniform = self.uniform_original
        random.random = self.random_original


# ==================================================
# Testes integrados
# ==================================================

def testar_fluxo_inicializacao():
    _secao("Fluxo 1 - Inicialização de jogo, mapa, itens e inimigos")
    _resetar_itens_inimigos()

    codigo_mapa, mapa = criarMapa()
    jogador_atual = _criar_jogador_estado("HeroiInicial")
    codigo_pos, posicao = getPosicaoInicialMapa(mapa)

    if jogador_atual is not None and codigo_pos == 0:
        jogador_atual["posicao"] = posicao

    codigo_item, id_item = itens.criarItem("Pocao simples", "cura", 25)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Lobo", 35, 7)
    status_item_mapa = alocarItemMapa(mapa, 2, 12, id_item) if codigo_mapa == 0 and codigo_item == 0 else 1
    status_inimigo_mapa = alocarInimigoMapa(mapa, 5, 11, id_inimigo, False) if codigo_mapa == 0 and codigo_inimigo == 0 else 1

    _resultado(
        "CT-INT-01",
        "criar jogador, mapa e posição inicial",
        codigo_mapa == 0
        and jogador_atual is not None
        and codigo_pos == 0
        and jogador_atual.get("posicao") == posicao
    )

    _resultado(
        "CT-INT-02",
        "criar e alocar item no mapa",
        codigo_item == 0
        and status_item_mapa == 0
        and getItemMapa(mapa, 2, 12) == (0, id_item)
        and itens.getTipoItem(id_item) == (0, "cura")
    )

    _resultado(
        "CT-INT-03",
        "criar e alocar inimigo no mapa",
        codigo_inimigo == 0
        and status_inimigo_mapa == 0
        and getInimigoMapa(mapa, 5, 11) == (0, id_inimigo)
        and inimigos.getNomeInimigo(id_inimigo) == (0, "Lobo")
    )

    _resultado(
        "CT-INT-04",
        "descrever e renderizar mapa criado",
        descreverPosicaoMapa(mapa, 1, 13)[0] == 0
        and renderizarMapa(mapa, jogador_atual.get("posicao"))[0] == 0
    )


def testar_fluxo_item_jogador():
    _secao("Fluxo 2 - Integração Item + Jogador + Inventário")
    _resetar_itens_inimigos()

    nome = "HeroiItens"
    jogador_atual = _criar_jogador_estado(nome, vida=50, ataque=10)

    codigo_cura, id_cura = itens.criarItem("Pocao", "cura", 30)
    codigo_ataque, id_ataque = itens.criarItem("Espada", "ataque", 5)
    codigo_chave, id_chave = itens.criarItem("Chave", "chave", 1)

    status_add_cura = jogador.adicionarItemJogador(nome, id_cura)
    status_add_ataque = jogador.adicionarItemJogador(nome, id_ataque)
    status_add_chave = jogador.adicionarItemJogador(nome, id_chave)
    _, inventario = jogador.getInventario(nome)

    _resultado(
        "CT-INT-05",
        "adicionar IDs de itens ao inventário do jogador",
        jogador_atual is not None
        and codigo_cura == 0
        and codigo_ataque == 0
        and codigo_chave == 0
        and status_add_cura == 0
        and status_add_ataque == 0
        and status_add_chave == 0
        and id_cura in inventario
        and id_ataque in inventario
        and id_chave in inventario
    )

    status_usar_cura = jogador.usarItemJogador(nome, id_cura)
    _, vida_depois_cura = jogador.getVida(nome)
    _, inventario_depois_cura = jogador.getInventario(nome)

    _resultado(
        "CT-INT-06",
        "usar item de cura altera vida e remove item do inventário",
        status_usar_cura == 0
        and vida_depois_cura == 80
        and id_cura not in inventario_depois_cura
    )

    status_usar_ataque = jogador.usarItemJogador(nome, id_ataque)
    _, ataque_depois = jogador.getAtaque(nome)
    _, inventario_depois_ataque = jogador.getInventario(nome)

    _resultado(
        "CT-INT-07",
        "usar item de ataque altera ataque e remove item do inventário",
        status_usar_ataque == 0
        and ataque_depois == 15
        and id_ataque not in inventario_depois_ataque
    )

    status_usar_chave = jogador.usarItemJogador(nome, id_chave)
    _, inventario_depois_chave = jogador.getInventario(nome)

    _resultado(
        "CT-INT-08",
        "usar item chave remove do inventário sem alterar vida ou ataque",
        status_usar_chave == 0
        and id_chave not in inventario_depois_chave
        and jogador.getVida(nome) == (0, 80)
        and jogador.getAtaque(nome) == (0, 15)
    )


def testar_fluxo_mapa_movimento_eventos():
    _secao("Fluxo 3 - Integração Mapa + Jogador + Itens + Inimigos")
    _resetar_itens_inimigos()

    codigo_mapa, mapa = criarMapa()
    jogador_atual = _criar_jogador_estado("HeroiMapa")
    _, posicao_inicial = getPosicaoInicialMapa(mapa)
    jogador_atual["posicao"] = posicao_inicial

    codigo_item, id_item = itens.criarItem("Pocao do mapa", "cura", 20)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Guardiao", 40, 8)
    alocarItemMapa(mapa, 2, 12, id_item)
    alocarInimigoMapa(mapa, 5, 11, id_inimigo, False)

    movimento_valido = moverJogadorMapa(mapa, jogador_atual, "direita")
    posicao_apos_movimento = jogador_atual.get("posicao")
    movimento_invalido = moverJogadorMapa(mapa, jogador_atual, "baixo")

    _resultado(
        "CT-INT-09",
        "movimentar jogador no mapa e bloquear obstáculo",
        codigo_mapa == 0
        and codigo_item == 0
        and codigo_inimigo == 0
        and movimento_valido == 0
        and posicao_apos_movimento == (2, 13)
        and movimento_invalido == 1
        and jogador_atual.get("posicao") == (2, 13)
    )

    jogador_atual["posicao"] = (2, 12)
    status_item, item_encontrado = getItemMapa(mapa, 2, 12)
    status_add = jogador.adicionarItemJogador("HeroiMapa", item_encontrado)
    status_limpar = limparEventoMapa(mapa, 2, 12)
    _, inventario = jogador.getInventario("HeroiMapa")

    _resultado(
        "CT-INT-10",
        "coletar item do mapa, adicionar ao inventário e limpar evento",
        status_item == 0
        and item_encontrado == id_item
        and status_add == 0
        and id_item in inventario
        and status_limpar == 0
        and getItemMapa(mapa, 2, 12) == (1, None)
    )

    status_inimigo, inimigo_encontrado = getInimigoMapa(mapa, 5, 11)
    status_derrotado = registrarInimigoDerrotadoMapa(mapa, 5, 11)

    _resultado(
        "CT-INT-11",
        "identificar inimigo no mapa e registrar derrota",
        status_inimigo == 0
        and inimigo_encontrado == id_inimigo
        and status_derrotado == 0
        and getInimigoMapa(mapa, 5, 11) == (1, None)
    )


def testar_fluxo_portao_chaves_chefe():
    _secao("Fluxo 4 - Integração Chaves + Portão + Chefe")
    _resetar_itens_inimigos()

    codigo_mapa, mapa = criarMapa()
    jogador_atual = _criar_jogador_estado("HeroiChaves")
    jogador_atual["posicao"] = (13, 5)

    status_bloqueado = moverJogadorMapa(mapa, jogador_atual, "cima", False)
    posicao_bloqueada = jogador_atual.get("posicao")

    codigo_chave1, id_chave1 = itens.criarItem("Chave 1", "chave", 1)
    codigo_chave2, id_chave2 = itens.criarItem("Chave 2", "chave", 1)
    jogador.adicionarItemJogador("HeroiChaves", id_chave1)
    jogador.adicionarItemJogador("HeroiChaves", id_chave2)

    status_liberado = moverJogadorMapa(mapa, jogador_atual, "cima", True)
    posicao_liberada = jogador_atual.get("posicao")

    codigo_chefe, id_chefe = inimigos.criarInimigo("Chefe", 75, 13)
    status_alocar_chefe = alocarInimigoMapa(mapa, 13, 2, id_chefe, True)
    status_final, eh_chefe = inimigoFinalMapa(mapa, 13, 2)

    _resultado(
        "CT-INT-12",
        "bloquear passagem no portão sem chaves",
        codigo_mapa == 0
        and status_bloqueado == 3
        and posicao_bloqueada == (13, 5)
    )

    _resultado(
        "CT-INT-13",
        "liberar passagem no portão com chaves",
        codigo_chave1 == 0
        and codigo_chave2 == 0
        and status_liberado == 0
        and posicao_liberada == (13, 4)
    )

    _resultado(
        "CT-INT-14",
        "alocar e identificar chefe final no mapa",
        codigo_chefe == 0
        and status_alocar_chefe == 0
        and status_final == 0
        and eh_chefe is True
        and getInimigoMapa(mapa, 13, 2) == (0, id_chefe)
    )


def testar_fluxo_batalha():
    _secao("Fluxo 5 - Integração Batalha + Jogador + Inimigo + Item")
    _resetar_itens_inimigos()

    nome = "HeroiBatalha"
    jogador_atual = _criar_jogador_estado(nome, vida=60, ataque=10)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Goblin", 30, 6)
    codigo_inicio, estado_batalha = batalha.iniciarBatalha(jogador_atual, id_inimigo)

    _resultado(
        "CT-INT-15",
        "iniciar batalha com jogador e inimigo válidos",
        codigo_inimigo == 0
        and codigo_inicio == 0
        and isinstance(estado_batalha, dict)
        and estado_batalha.get("turno") == batalha.TURNO_JOGADOR
        and estado_batalha.get("ativa") is True
    )

    with SimularInput([batalha.ATACAR]), SimularRandom(uniforme=1.0):
        status_turno_ataque = batalha.turno(jogador_atual, id_inimigo, estado_batalha)

    _resultado(
        "CT-INT-16",
        "turno do jogador atacando aplica dano ao inimigo e alterna turno",
        status_turno_ataque == 0
        and inimigos.getVidaInimigo(id_inimigo) == (0, 20)
        and estado_batalha.get("turno") == batalha.TURNO_INIMIGO
    )

    with SimularRandom(uniforme=1.0):
        status_turno_inimigo = batalha.turno(jogador_atual, id_inimigo, estado_batalha)

    _, vida_jogador = jogador.getVida(nome)

    _resultado(
        "CT-INT-17",
        "turno do inimigo aplica dano ao jogador e alterna turno",
        status_turno_inimigo == 0
        and vida_jogador == 54
        and estado_batalha.get("turno") == batalha.TURNO_JOGADOR
    )

    codigo_item, id_item = itens.criarItem("Pocao batalha", "cura", 20)
    jogador.adicionarItemJogador(nome, id_item)

    with SimularInput([batalha.USAR_ITEM, "1"]), SimularRandom(uniforme=1.0):
        status_turno_item = batalha.turno(jogador_atual, id_inimigo, estado_batalha)

    _, vida_apos_item = jogador.getVida(nome)
    _, inventario_apos_item = jogador.getInventario(nome)

    _resultado(
        "CT-INT-18",
        "turno do jogador usando item de cura atualiza vida e inventário",
        codigo_item == 0
        and status_turno_item == 0
        and vida_apos_item == 74
        and id_item not in inventario_apos_item
        and estado_batalha.get("turno") == batalha.TURNO_INIMIGO
    )

    estado_batalha["turno"] = batalha.TURNO_JOGADOR
    with SimularInput([batalha.DEFENDER]), SimularRandom(uniforme=1.0):
        status_defender = batalha.turno(jogador_atual, id_inimigo, estado_batalha)

    with SimularRandom(uniforme=1.0, aleatorio=0.0):
        status_inimigo_defesa = batalha.turno(jogador_atual, id_inimigo, estado_batalha)

    _, vida_apos_defesa = jogador.getVida(nome)

    _resultado(
        "CT-INT-19",
        "defesa reduz dano recebido e pode atordoar inimigo",
        status_defender == 0
        and status_inimigo_defesa == 0
        and vida_apos_defesa == 71
        and estado_batalha.get("atordoado") is True
        and estado_batalha.get("turno") == batalha.TURNO_JOGADOR
    )

    inimigos.receberDanoInimigo(id_inimigo, 20)
    status_fim = batalha.verificarFimBatalha(jogador_atual, id_inimigo, estado_batalha)

    _resultado(
        "CT-INT-20",
        "verificar fim de batalha com vitória do jogador",
        status_fim == 0
        and estado_batalha.get("ativa") is False
        and estado_batalha.get("vencedor") == "jogador"
    )


def testar_fluxo_batalha_completa():
    _secao("Fluxo 6 - Execução completa de batalha simulada")
    _resetar_itens_inimigos()

    nome = "HeroiExecucao"
    jogador_atual = _criar_jogador_estado(nome, vida=100, ataque=50)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Slime", 30, 5)

    with SimularInput([batalha.ATACAR]), SimularRandom(uniforme=1.0):
        codigo_batalha, vencedor = batalha.executarBatalha(jogador_atual, id_inimigo)

    _resultado(
        "CT-INT-21",
        "executar batalha completa até vitória do jogador",
        codigo_inimigo == 0
        and codigo_batalha == 0
        and vencedor == "jogador"
        and inimigos.inimigoVivo(id_inimigo) == (0, False)
    )


# ==================================================
# Fluxo 7 - Casos negativos de batalha
# ==================================================
def testar_fluxos_negativos_batalha():
    _secao("Fluxo 7 - Casos negativos de batalha")
    _resetar_itens_inimigos()

    nome = "HeroiDerrota"
    jogador_atual = _criar_jogador_estado(nome, vida=10, ataque=1)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Dragao", 80, 20)
    codigo_inicio, estado_batalha = batalha.iniciarBatalha(jogador_atual, id_inimigo)

    if isinstance(estado_batalha, dict):
        estado_batalha["turno"] = batalha.TURNO_INIMIGO

    with SimularRandom(uniforme=1.0):
        status_turno = batalha.turno(jogador_atual, id_inimigo, estado_batalha)

    status_fim = batalha.verificarFimBatalha(jogador_atual, id_inimigo, estado_batalha)

    _resultado(
        "CT-INT-22",
        "encerrar batalha com derrota do jogador",
        jogador_atual is not None
        and codigo_inimigo == 0
        and codigo_inicio == 0
        and status_turno == 0
        and status_fim == 0
        and jogador.getVida(nome) == (0, 0)
        and estado_batalha.get("ativa") is False
        and estado_batalha.get("vencedor") == "inimigo"
    )

    nome = "HeroiAcaoInvalida"
    jogador_atual = _criar_jogador_estado(nome, vida=100, ataque=10)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Goblin", 30, 6)
    codigo_inicio, estado_batalha = batalha.iniciarBatalha(jogador_atual, id_inimigo)

    with SimularInput(["9"]), SimularRandom(uniforme=1.0):
        status_acao_invalida = batalha.turno(jogador_atual, id_inimigo, estado_batalha)

    _resultado(
        "CT-INT-23",
        "recusar ação inválida no turno do jogador",
        codigo_inimigo == 0
        and codigo_inicio == 0
        and status_acao_invalida == 2
        and inimigos.getVidaInimigo(id_inimigo) == (0, 30)
        and jogador.getVida(nome) == (0, 100)
        and estado_batalha.get("turno") == batalha.TURNO_JOGADOR
    )

    nome = "HeroiSemItem"
    jogador_atual = _criar_jogador_estado(nome, vida=80, ataque=10)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Morcego", 30, 6)
    codigo_inicio, estado_batalha = batalha.iniciarBatalha(jogador_atual, id_inimigo)

    with SimularInput([batalha.USAR_ITEM]), SimularRandom(uniforme=1.0):
        status_sem_item = batalha.turno(jogador_atual, id_inimigo, estado_batalha)

    _resultado(
        "CT-INT-24",
        "tratar tentativa de usar item sem itens disponíveis",
        jogador_atual is not None
        and codigo_inimigo == 0
        and codigo_inicio == 0
        and status_sem_item == 0
        and jogador.getVida(nome) == (0, 80)
        and inimigos.getVidaInimigo(id_inimigo) == (0, 30)
        and estado_batalha.get("turno") == batalha.TURNO_JOGADOR
    )


def testar_fluxo_xp_e_evolucao():
    _secao("Fluxo 8 - XP e atualização de ataque após combate")
    _resetar_itens_inimigos()

    nome = "HeroiXP"
    _criar_jogador_estado(nome, vida=100, ataque=10)

    status_xp = jogador.ganharXP(nome, 250)
    status_ataque = jogador.atualizarAtaque(nome)
    _, xp = jogador.getXP(nome)
    _, ataque = jogador.getAtaque(nome)

    _resultado(
        "CT-INT-25",
        "ganhar XP e atualizar ataque do jogador",
        status_xp == 0
        and status_ataque == 0
        and xp == 250
        and ataque == 12
    )


def testar_fluxo_exportacao_restauracao():
    _secao("Fluxo 9 - Exportação e restauração dos TADs")
    _resetar_itens_inimigos()

    nome = "HeroiExportacao"
    jogador_atual = _criar_jogador_estado(nome, vida=70, xp=90, ataque=11)
    codigo_item, id_item = itens.criarItem("Pocao exportada", "cura", 15)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Inimigo exportado", 40, 8)
    jogador.adicionarItemJogador(nome, id_item)

    resultado_exportar = jogador.exportarJogador(nome)
    estado_itens = itens.exportarEstadoItens()
    estado_inimigos = inimigos.exportarEstadoInimigos()

    jogador.receberDanoJogador(nome, 20)
    itens.restaurarEstadoItens([])
    inimigos.restaurarEstadoInimigos([])

    if isinstance(resultado_exportar, tuple) and len(resultado_exportar) == 2:
        codigo_exportar_jogador, estado_jogador = resultado_exportar
    else:
        codigo_exportar_jogador, estado_jogador = 2, None

    status_restaurar_jogador = jogador.restaurarJogador(estado_jogador)
    status_restaurar_itens = itens.restaurarEstadoItens(estado_itens)
    status_restaurar_inimigos = inimigos.restaurarEstadoInimigos(estado_inimigos)

    _resultado(
        "CT-INT-26",
        "exportar e restaurar jogador, itens e inimigos mantendo estado",
        jogador_atual is not None
        and codigo_item == 0
        and codigo_inimigo == 0
        and codigo_exportar_jogador == 0
        and status_restaurar_jogador == 0
        and status_restaurar_itens == 0
        and status_restaurar_inimigos == 0
        and jogador.getVida(nome) == (0, 70)
        and jogador.getInventario(nome)[1] == [id_item]
        and itens.getValorItem(id_item) == (0, 15)
        and inimigos.getNomeInimigo(id_inimigo) == (0, "Inimigo exportado")
    )


def testar_fluxo_save_load():
    _secao("Fluxo 10 - Salvamento e carregamento integrado")
    _limpar_save()
    _resetar_itens_inimigos()

    codigo_mapa, mapa = criarMapa()
    jogador_atual = _criar_jogador_estado("HeroiSave", vida=80, xp=100, ataque=11)
    jogador_atual["posicao"] = (2, 12)

    codigo_item, id_item = itens.criarItem("Pocao Save", "cura", 25)
    codigo_inimigo, id_inimigo = inimigos.criarInimigo("Inimigo Save", 35, 7)
    alocarItemMapa(mapa, 2, 12, id_item)
    alocarInimigoMapa(mapa, 5, 11, id_inimigo, False)
    jogador.adicionarItemJogador("HeroiSave", id_item)
    limparEventoMapa(mapa, 2, 12)

    status_salvar = salvar.salvarJogo(jogador_atual, mapa)
    existe_save = salvar.existeSalvamento()

    _resultado(
        "CT-INT-27",
        "salvar jogo com jogador, mapa, item e inimigo",
        codigo_mapa == 0
        and codigo_item == 0
        and codigo_inimigo == 0
        and status_salvar == 0
        and existe_save is True
    )

    itens.restaurarEstadoItens([])
    inimigos.restaurarEstadoInimigos([])
    _criar_jogador_estado("HeroiSave", vida=10, xp=0, ataque=1)

    codigo_carregar, jogador_carregado, mapa_carregado = salvar.carregarJogo(_preparar_entidades_teste)
    _, inventario_carregado = jogador.getInventario("HeroiSave")

    _resultado(
        "CT-INT-28",
        "carregar jogo restaura jogador, itens, inimigos e mapa",
        codigo_carregar == 0
        and jogador_carregado is not None
        and mapa_carregado is not None
        and jogador_carregado.get("posicao") == (2, 12)
        and jogador.getVida("HeroiSave") == (0, 80)
        and jogador.getXP("HeroiSave") == (0, 100)
        and id_item in inventario_carregado
        and itens.getTipoItem(id_item) == (0, "cura")
        and inimigos.getNomeInimigo(id_inimigo) == (0, "Inimigo Save")
        and getItemMapa(mapa_carregado, 2, 12) == (1, None)
    )

    _limpar_save()


def testar_fluxos_de_erro_integrados():
    _secao("Fluxo 11 - Erros integrados e entradas inválidas")
    _limpar_save()
    _resetar_itens_inimigos()

    codigo_sem_save, jogador_sem_save, mapa_sem_save = salvar.carregarJogo(_preparar_entidades_teste)

    codigo_mapa, mapa = criarMapa()
    jogador_atual = _criar_jogador_estado("HeroiErro")
    jogador_atual["posicao"] = (1, 13)

    status_item_invalido = jogador.usarItemJogador("HeroiErro", 999)
    status_batalha_invalida, batalha_invalida = batalha.iniciarBatalha(jogador_atual, 999)
    status_mapa_invalido = moverJogadorMapa(mapa, jogador_atual, "diagonal")
    status_salvar_invalido = salvar.salvarJogo(None, mapa)

    _resultado(
        "CT-INT-29",
        "tratar ausência de save e parâmetros inválidos entre módulos",
        codigo_sem_save == 2
        and jogador_sem_save is None
        and mapa_sem_save is None
        and codigo_mapa == 0
        and status_item_invalido == 1
        and status_batalha_invalida == 2
        and batalha_invalida is None
        and status_mapa_invalido == 1
        and status_salvar_invalido == 2
    )

    _limpar_save()
    with open("save.json", "w", encoding="utf-8") as arquivo:
        arquivo.write("{ arquivo json invalido")

    codigo_json_invalido, jogador_json_invalido, mapa_json_invalido = salvar.carregarJogo(_preparar_entidades_teste)

    _resultado(
        "CT-INT-30",
        "recusar carregamento com arquivo JSON inválido",
        codigo_json_invalido == 2
        and jogador_json_invalido is None
        and mapa_json_invalido is None
    )

    _limpar_save()


# ==================================================
# Execução dos testes integrados
# ==================================================

print("==================================================")
print("        TESTE INTEGRADO - ConsoleRPG")
print("==================================================")

testar_fluxo_inicializacao()
testar_fluxo_item_jogador()
testar_fluxo_mapa_movimento_eventos()
testar_fluxo_portao_chaves_chefe()
testar_fluxo_batalha()
testar_fluxo_batalha_completa()
testar_fluxos_negativos_batalha()
testar_fluxo_xp_e_evolucao()
testar_fluxo_exportacao_restauracao()
testar_fluxo_save_load()
testar_fluxos_de_erro_integrados()

print("\n==================================================")
print(f"Resultado final: {testes_passaram}/{total_testes} testes integrados passaram")
print("==================================================")

if testes_passaram == total_testes:
    print("Todos os fluxos integrados foram executados com sucesso.")
else:
    print("Alguns fluxos integrados apresentaram erro. Verifique os CTs marcados com [ERRO].")