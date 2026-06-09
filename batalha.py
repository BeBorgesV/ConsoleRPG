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


def _barraHP(atual, maximo):
    barras = max(0, min(10, int((atual / maximo) * 10)))
    return "[" + "█" * barras + "░" * (10 - barras) + "] " + str(atual) + "/" + str(maximo)


def _exibirStatusBatalha(jogador_atual, inimigo_atual, batalha):
    nome_j = _nomeJogador(jogador_atual)
    _, vida_j = jogador.getVida(nome_j)
    _, vida_i = inimigos.getVidaInimigo(inimigo_atual)

    if vida_j is None or vida_i is None:
        return

    nome_i = batalha.get("nome_inimigo", "Inimigo")
    vida_max_i = batalha.get("vida_max_inimigo", vida_i)

    print(f"  {nome_j:<14} {_barraHP(vida_j, 100)}")
    print(f"  {nome_i:<14} {_barraHP(vida_i, vida_max_i)}")


def _nomeJogador(jogador_atual):
    if isinstance(jogador_atual, dict):
        return jogador_atual.get("nome")

    return jogador_atual


def _itensUsaveis(inventario):
    usaveis = []

    for item in inventario:
        if isinstance(item, dict) and item.get("tipo") in ["cura", "ataque"]:
            usaveis.append(item)

    return usaveis


def _exibirInventarioBatalha(jogador_atual):
    codigo_inventario, inventario = jogador.getInventario(_nomeJogador(jogador_atual))

    if codigo_inventario != 0:
        return codigo_inventario

    itens_usaveis = _itensUsaveis(inventario)

    if len(itens_usaveis) == 0:
        print("Nenhum item de batalha disponível.")
        return 1

    print("\nInventário:")

    for indice in range(len(itens_usaveis)):
        item = itens_usaveis[indice]
        nome = item.get("nome", "Item")
        tipo = item.get("tipo", "tipo")
        valor = item.get("valor", 0)
        print(str(indice + 1) + " - " + nome + " (" + tipo + ": " + str(valor) + ")")

    print("0 - Voltar")
    return 0


def _selecionarItemInventario(jogador_atual, escolha):
    if escolha is None or not isinstance(escolha, str) or not escolha.strip():
        return 2, None

    codigo_inventario, inventario = jogador.getInventario(_nomeJogador(jogador_atual))

    if codigo_inventario != 0:
        return codigo_inventario, None

    itens_usaveis = _itensUsaveis(inventario)

    if not escolha.strip().isdigit():
        return 1, None

    numero = int(escolha.strip())

    if numero == 0:
        return 3, None

    if numero < 1 or numero > len(itens_usaveis):
        return 1, None

    return 0, itens_usaveis[numero - 1]


def calcularDano(ataque):
    """
    Objetivo:
        Calcular o dano causado em um ataque com variação aleatória.

    Requisitos funcionais:
        - O valor de ataque deve ser numérico e positivo.
        - O dano calculado deve ser um inteiro positivo.
        - O cálculo deve aplicar um multiplicador aleatório entre 0.7 e 1.5.

    Acoplamento:
        Entrada:
            ataque: valor base de ataque do atacante.
        Saída:
            dano: valor inteiro de dano calculado.
        Retornos:
            (0, dano): dano calculado com sucesso.
            (1, None): dano resultante igual a zero após cálculo.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - ataque deve ser int ou float maior que zero.
        Assertivas de saída:
            - se retornar (0, dano), dano é um inteiro positivo.
            - se retornar (1, None), o cálculo produziu dano zero ou negativo.
            - se retornar (2, None), o parâmetro recebido é inválido.

    Hipóteses e restrições:
        - O multiplicador aleatório está no intervalo [0.7, 1.5].
        - O dano é truncado para inteiro após o cálculo.
    """
    if ataque is None or not isinstance(ataque, (int, float)) or ataque <= 0:
        return 2, None

    multiplicador = random.uniform(0.7, 1.5)
    dano = int(ataque * multiplicador)

    if dano <= 0:
        return 1, None

    return 0, dano


def iniciarBatalha(jogador_atual, inimigo_atual):
    """
    Objetivo:
        Inicializar o estado de uma batalha entre o jogador e um inimigo.

    Requisitos funcionais:
        - O jogador deve ser válido e estar vivo.
        - O inimigo deve ser válido e estar vivo.
        - A batalha deve começar no turno do jogador.
        - O estado inicial deve registrar o nome e a vida máxima do inimigo.

    Acoplamento:
        Entrada:
            jogador_atual: dicionário do jogador participante da batalha.
            inimigo_atual: identificador do inimigo a ser enfrentado.
        Saída:
            batalha: dicionário com o estado inicial da batalha.
        Retornos:
            (0, batalha): batalha iniciada com sucesso.
            (1, None): erro por regra do jogo (jogador ou inimigo sem vida).
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador_atual deve ser um dicionário válido registrado no módulo jogador.
            - inimigo_atual deve ser um identificador inteiro válido no módulo inimigos.
            - ambos devem possuir vida maior que zero.
        Assertivas de saída:
            - se retornar (0, batalha), o estado de batalha está ativo e no turno do jogador.
            - se retornar (1, None) ou (2, None), nenhum estado de batalha é criado.

    Hipóteses e restrições:
        - O nome do inimigo é obtido exclusivamente via função de acesso do módulo inimigos.
        - O estado de batalha é um dicionário interno ao módulo batalha.
    """
    if jogador_atual is None or inimigo_atual is None:
        return 2, None

    nome_jogador = _nomeJogador(jogador_atual)
    codigo_vida_jogador, vida_jogador = jogador.getVida(nome_jogador)
    codigo_vida_inimigo, vida_inimigo = inimigos.getVidaInimigo(inimigo_atual)

    if codigo_vida_jogador == 2 or codigo_vida_inimigo == 2:
        return 2, None

    if codigo_vida_jogador != 0 or codigo_vida_inimigo != 0:
        return 1, None

    if vida_jogador <= 0 or vida_inimigo <= 0:
        return 1, None

    nome_inimigo = "Inimigo"
    codigo_nome, nome_obtido = inimigos.getNomeInimigo(inimigo_atual)
    if codigo_nome == 0:
        nome_inimigo = nome_obtido

    batalha = {
        "turno": TURNO_JOGADOR,
        "ativa": True,
        "vencedor": None,
        "defendendo": False,
        "atordoado": False,
        "nome_inimigo": nome_inimigo,
        "vida_max_inimigo": vida_inimigo
    }

    print(f"\n{nome_inimigo} apareceu! A batalha começou.")
    return 0, batalha


def turno(jogador_atual, inimigo_atual, batalha):
    """
    Objetivo:
        Executar um turno de batalha, processando a ação do jogador ou do inimigo.

    Requisitos funcionais:
        - No turno do jogador, apresentar as opções: atacar, usar item ou defender.
        - Atacar deve aplicar dano calculado ao inimigo.
        - Usar item deve consumir um item do inventário do jogador.
        - Defender deve reduzir o próximo dano recebido e ter chance de atordoar o inimigo.
        - No turno do inimigo, aplicar dano calculado ao jogador.
        - Inimigo atordoado deve perder seu turno.

    Acoplamento:
        Entrada:
            jogador_atual: dicionário do jogador participante da batalha.
            inimigo_atual: identificador do inimigo participante.
            batalha: dicionário com o estado atual da batalha.
        Saída:
            estado de batalha e dos participantes atualizado.
        Retornos:
            0: turno executado com sucesso.
            1: erro interno ao executar o turno.
            2: ação inválida ou parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador_atual deve ser um dicionário válido registrado no módulo jogador.
            - inimigo_atual deve ser um identificador inteiro válido no módulo inimigos.
            - batalha deve ser um dicionário contendo o campo "turno".
        Assertivas de saída:
            - se retornar 0, o turno foi alternado corretamente.
            - se retornar 2, nenhuma ação foi aplicada e o estado permanece inalterado.

    Hipóteses e restrições:
        - A defesa reduz o dano recebido à metade e tem 35% de chance de atordoar o inimigo.
        - O atordoamento faz o inimigo perder exatamente um turno.
    """
    if jogador_atual is None or inimigo_atual is None or batalha is None:
        return 2

    if "turno" not in batalha:
        return 1

    if batalha["turno"] == TURNO_JOGADOR:
        _exibirStatusBatalha(jogador_atual, inimigo_atual, batalha)
        print("\nSeu turno:")
        print("1 - Atacar")
        print("2 - Usar item")
        print("3 - Defender")

        acao = input("Escolha sua ação: ").strip()

        if acao == ATACAR:
            codigo_ataque, ataque = jogador.getAtaque(_nomeJogador(jogador_atual))

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

            codigo_item = jogador.usarItemJogador(_nomeJogador(jogador_atual), item)

            if codigo_item != 0:
                return codigo_item

            print("Item usado com sucesso.")
            batalha["turno"] = TURNO_INIMIGO
            return 0

        if acao == DEFENDER:
            batalha["defendendo"] = True
            batalha["turno"] = TURNO_INIMIGO
            print("Você se defendeu. (35% de chance de atordoar o inimigo)")
            return 0

        return 2

    if batalha["turno"] == TURNO_INIMIGO:
        if batalha.get("atordoado"):
            batalha["atordoado"] = False
            batalha["turno"] = TURNO_JOGADOR
            print(f"O {batalha.get('nome_inimigo', 'inimigo')} está atordoado e perde o turno.")
            return 0

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
            if random.random() < 0.35:
                batalha["atordoado"] = True
                print(f"Sua defesa atordoou o {batalha.get('nome_inimigo', 'inimigo')}! Ele perde o próximo turno.")

        codigo_receber = jogador.receberDanoJogador(_nomeJogador(jogador_atual), dano)

        if codigo_receber != 0:
            return codigo_receber

        print("O inimigo causou", dano, "de dano ao jogador.")
        batalha["turno"] = TURNO_JOGADOR
        return 0

    return 1


def verificarFimBatalha(jogador_atual, inimigo_atual, batalha):
    """
    Objetivo:
        Verificar se a batalha chegou ao fim e registrar o vencedor.

    Requisitos funcionais:
        - Se a vida do jogador for zero, o inimigo vence.
        - Se a vida do inimigo for zero, o jogador vence.
        - O resultado deve ser registrado no estado da batalha.

    Acoplamento:
        Entrada:
            jogador_atual: dicionário do jogador participante.
            inimigo_atual: identificador do inimigo participante.
            batalha: dicionário com o estado atual da batalha.
        Saída:
            estado da batalha atualizado com vencedor e flag ativa.
        Retornos:
            0: verificação realizada com sucesso.
            1: erro ao consultar estado dos participantes.
            2: parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador_atual deve ser um dicionário válido registrado no módulo jogador.
            - inimigo_atual deve ser um identificador inteiro válido no módulo inimigos.
            - batalha deve ser um dicionário com os campos "ativa" e "vencedor".
        Assertivas de saída:
            - se retornar 0 e batalha["ativa"] for False, batalha["vencedor"] está definido.
            - se retornar 0 e batalha["ativa"] for True, a batalha ainda não terminou.
            - se retornar 1 ou 2, o estado da batalha não é alterado.

    Hipóteses e restrições:
        - A vida dos participantes é consultada exclusivamente via funções de acesso dos módulos.
    """
    if jogador_atual is None or inimigo_atual is None or batalha is None:
        return 2

    codigo_vida_jogador, vida_jogador = jogador.getVida(_nomeJogador(jogador_atual))
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
    """
    Objetivo:
        Executar uma batalha completa entre o jogador e um inimigo até o fim.

    Requisitos funcionais:
        - A batalha deve ser iniciada antes do primeiro turno.
        - Os turnos devem se alternar até que um dos participantes seja derrotado.
        - O resultado final deve indicar quem venceu.

    Acoplamento:
        Entrada:
            jogador_atual: dicionário do jogador participante.
            inimigo_atual: identificador do inimigo a ser enfrentado.
        Saída:
            vencedor: string indicando o resultado da batalha.
        Retornos:
            (0, "jogador"): jogador venceu a batalha.
            (0, "inimigo"): inimigo venceu a batalha.
            (1, None): erro interno durante a batalha.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador_atual deve ser um dicionário válido registrado no módulo jogador.
            - inimigo_atual deve ser um identificador inteiro válido no módulo inimigos.
        Assertivas de saída:
            - se retornar (0, vencedor), a batalha foi concluída normalmente.
            - se retornar (0, "jogador"), a vida do inimigo chegou a zero.
            - se retornar (0, "inimigo"), a vida do jogador chegou a zero.
            - se retornar (1, None) ou (2, None), a batalha foi interrompida por erro.

    Hipóteses e restrições:
        - Delega a lógica de cada turno para a função turno().
        - A batalha termina quando verificarFimBatalha() detecta vida zero em algum participante.
    """
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
