import random

import jogador
import inimigos

__all__ = [
    "TURNO_JOGADOR",
    "TURNO_INIMIGO",
    "ATACAR",
    "USAR_ITEM",
    "DEFENDER",
    "calcularDano",
    "iniciarBatalha",
    "turno",
    "verificarFimBatalha",
    "executarBatalha"
]

TURNO_JOGADOR = 0
TURNO_INIMIGO = 1

ATACAR = "1"
USAR_ITEM = "2"
DEFENDER = "3"


def _exibirInventarioBatalha(jogador_atual):
    codigo_inventario, inventario = jogador.getInventario(jogador_atual)

    if codigo_inventario != 0:
        return codigo_inventario

    if len(inventario) == 0:
        print("Inventário vazio.")
        return 1

    print("\nInventário:")

    for indice in range(len(inventario)):
        item = inventario[indice]
        nome = item.get("nome", "Item")
        tipo = item.get("tipo", "tipo")
        valor = item.get("valor", 0)
        print(str(indice + 1) + " - " + nome + " (" + tipo + ": " + str(valor) + ")")

    print("0 - Voltar")
    return 0


def _selecionarItemInventario(jogador_atual, escolha):
    if escolha is None or not isinstance(escolha, str) or not escolha.strip():
        return 2, None

    codigo_inventario, inventario = jogador.getInventario(jogador_atual)

    if codigo_inventario != 0:
        return codigo_inventario, None

    if not escolha.strip().isdigit():
        return 1, None

    numero = int(escolha.strip())

    if numero == 0:
        return 3, None

    if numero < 1 or numero > len(inventario):
        return 1, None

    return 0, inventario[numero - 1]


def calcularDano(ataque):
    if ataque is None or not isinstance(ataque, (int, float)) or ataque <= 0:
        return 2, None

    multiplicador = random.uniform(0.7, 1.5)
    dano = int(ataque * multiplicador)

    if dano <= 0:
        return 1, None

    return 0, dano


def iniciarBatalha(jogador_atual, inimigo_atual):
    if jogador_atual is None or inimigo_atual is None:
        return 2, None

    codigo_vida_jogador, vida_jogador = jogador.getVida(jogador_atual)
    codigo_vida_inimigo, vida_inimigo = inimigos.getVidaInimigo(inimigo_atual)

    if codigo_vida_jogador == 2 or codigo_vida_inimigo == 2:
        return 2, None

    if codigo_vida_jogador != 0 or codigo_vida_inimigo != 0:
        return 1, None

    if vida_jogador <= 0 or vida_inimigo <= 0:
        return 1, None

    batalha = {
        "turno": TURNO_JOGADOR,
        "ativa": True,
        "vencedor": None,
        "defendendo": False
    }

    print("\nUma batalha começou!")
    return 0, batalha


def turno(jogador_atual, inimigo_atual, batalha):
    if jogador_atual is None or inimigo_atual is None or batalha is None:
        return 2

    if "turno" not in batalha:
        return 1

    if batalha["turno"] == TURNO_JOGADOR:
        print("\nSeu turno:")
        print("1 - Atacar")
        print("2 - Usar item")
        print("3 - Defender")

        acao = input("Escolha sua ação: ").strip()

        if acao == ATACAR:
            codigo_ataque, ataque = jogador.getAtaque(jogador_atual)

            if codigo_ataque != 0:
                return codigo_ataque

            codigo_dano, dano = calcularDano(ataque)

            if codigo_dano != 0:
                return codigo_dano

            codigo_receber = inimigos.receberDanoInimigo(inimigo_atual, dano)

            if codigo_receber != 0:
                return codigo_receber

            print("Você causou", dano, "de dano ao inimigo.")
            batalha["turno"] = TURNO_INIMIGO
            return 0

        if acao == USAR_ITEM:
            if not hasattr(jogador, "usarItemJogador"):
                return 1

            codigo_inventario = _exibirInventarioBatalha(jogador_atual)

            if codigo_inventario == 1:
                return 0

            if codigo_inventario != 0:
                return codigo_inventario

            escolha_item = input("Escolha o item: ").strip()
            codigo_busca, item = _selecionarItemInventario(jogador_atual, escolha_item)

            if codigo_busca == 3:
                print("Voltando ao menu da batalha.")
                return 0

            if codigo_busca != 0:
                print("Item inválido.")
                return 0

            codigo_item = jogador.usarItemJogador(jogador_atual, item)

            if codigo_item != 0:
                return codigo_item

            print("Item usado com sucesso.")
            batalha["turno"] = TURNO_INIMIGO
            return 0

        if acao == DEFENDER:
            batalha["defendendo"] = True
            batalha["turno"] = TURNO_INIMIGO
            print("Você se defendeu.")
            return 0

        return 2

    if batalha["turno"] == TURNO_INIMIGO:
        codigo_ataque, ataque = inimigos.getAtaqueInimigo(inimigo_atual)

        if codigo_ataque != 0:
            return codigo_ataque

        codigo_dano, dano = calcularDano(ataque)

        if codigo_dano != 0:
            return codigo_dano

        if batalha.get("defendendo"):
            dano = dano // 2
            batalha["defendendo"] = False
            print("Sua defesa reduziu o dano recebido.")

        codigo_receber = jogador.receberDanoJogador(jogador_atual, dano)

        if codigo_receber != 0:
            return codigo_receber

        print("O inimigo causou", dano, "de dano ao jogador.")
        batalha["turno"] = TURNO_JOGADOR
        return 0

    return 1


def verificarFimBatalha(jogador_atual, inimigo_atual, batalha):
    if jogador_atual is None or inimigo_atual is None or batalha is None:
        return 2

    codigo_vida_jogador, vida_jogador = jogador.getVida(jogador_atual)
    codigo_vida_inimigo, vida_inimigo = inimigos.getVidaInimigo(inimigo_atual)

    if codigo_vida_jogador != 0:
        return codigo_vida_jogador

    if codigo_vida_inimigo != 0:
        return codigo_vida_inimigo

    if vida_jogador <= 0:
        batalha["ativa"] = False
        batalha["vencedor"] = "inimigo"
        return 0

    if vida_inimigo <= 0:
        batalha["ativa"] = False
        batalha["vencedor"] = "jogador"
        return 0

    return 0


def executarBatalha(jogador_atual, inimigo_atual):
    codigo_inicio, batalha = iniciarBatalha(jogador_atual, inimigo_atual)

    if codigo_inicio != 0:
        return codigo_inicio, None

    while batalha["ativa"]:
        codigo_turno = turno(jogador_atual, inimigo_atual, batalha)

        if codigo_turno == 2:
            print("Ação inválida. Tente novamente.")
            continue

        if codigo_turno != 0:
            return codigo_turno, None

        codigo_fim = verificarFimBatalha(jogador_atual, inimigo_atual, batalha)

        if codigo_fim != 0:
            return codigo_fim, None

    if batalha["vencedor"] == "jogador":
        print("\nVocê venceu a batalha!")
    else:
        print("\nVocê perdeu a batalha.")

    return 0, batalha["vencedor"]
