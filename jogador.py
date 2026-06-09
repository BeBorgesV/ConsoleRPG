import copy

__all__ = [
    "criarJogador",
    "getVida",
    "getXP",
    "getAtaque",
    "getInventario",
    "receberDanoJogador",
    "curarJogador",
    "ganharXP",
    "atualizarAtaque",
    "adicionarItemJogador",
    "usarItemJogador"
]

# Dicionário interno que armazena todos os TADs de jogadores indexados pelo nome
_jogadores = dict()


def _jogadorExiste(nome):
    """Valida se o nome corresponde a um jogador cadastrado e válido."""
    return nome in _jogadores and isinstance(_jogadores[nome], dict)


def criarJogador(nome):
    """
    Objetivo:
        Inicializar um novo jogador no sistema com atributos padrão e armazená-lo indexado pelo nome.

    Requisitos funcionais:
        - O nome não pode ser nulo.
        - O nome deve ser uma string válida e não vazia.
        - Em caso de sucesso, o jogador deve ser registrado internamente e uma cópia profunda deve ser retornada.

    Acoplamento:
        Entrada:
            nome: string contendo o nome identificador do jogador.
        Saída:
            dicionário interno do jogador inicializado.
        Retornos:
            retorno_seguro (dict): cópia profunda do dicionário do jogador criado com sucesso.
            1: erro por nome vazio ou apenas espaços.
            2: erro por parâmetro inválido ou nulo.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser uma string não vazia.
            - nome não deve ser None.

        Assertivas de saída:
            - se retornar um dicionário, o jogador foi inserido com sucesso na estrutura interna de _jogadores.
            - se retornar um dicionário, ele representa uma cópia isolada para evitar mutações acidentais externas.
            - se retornar 1 ou 2, nenhum estado interno é alterado ou poluído.

    Hipóteses e restrições:
        - O nome do jogador serve como a chave primária única de busca no sistema.
    """
    # CT-J03 - parâmetro inválido
    if nome is None:
        return 2

    # CT-J02 - nome vazio ou apenas espaços
    if not isinstance(nome, str) or not nome.strip():
        return 1

    nome_limpo = nome.strip()
    
    jogador = {
        "nome": nome_limpo,
        "vida": 100,
        "vida_max": 100,
        "xp": 0,
        "ataque": 10,
        "vivo": True,
        "inventario": []
    }
    _jogadores[nome_limpo] = jogador
    
    retorno_seguro = copy.deepcopy(jogador)
    return retorno_seguro


def getVida(nome):
    """
    Objetivo:
        Consultar a quantidade de pontos de vida atuais de um jogador específico.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - A estrutura de dados interna do jogador deve conter o campo de vida.

    Acoplamento:
        Entrada:
            nome: string com o nome do jogador a ser consultado.
        Saída:
            pontos de vida do jogador obtidos.
        Retornos:
            (0, vida): sucesso, retorna o código e o valor numérico da vida.
            (1, None): erro por ausência do campo "vida" no registro do jogador.
            (2, None): erro por jogador não cadastrado ou nome inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve corresponder a um jogador previamente cadastrado no sistema.

        Assertivas de saída:
            - se retornar (0, vida), o valor retornado corresponde exatamente ao valor numérico atualizado da vida interna.
            - se retornar códigos de erro (1 ou 2), o segundo parâmetro da tupla deve ser estritamente None.

    Hipóteses e restrições:
        - Nenhuma alteração de estado ocorre na estrutura interna durante uma consulta.
    """
    # CT-J05 - consultar vida de jogador inválido (não cadastrado)
    if not _jogadorExiste(nome):
        return 2, None

    jogador = _jogadores[nome]
    # CT-J06 - consultar vida sem campo vida
    if "vida" not in jogador:
        return 1, None

    # CT-J04 - consultar vida válida
    return 0, jogador["vida"]


def getXP(nome):
    """
    Objetivo:
        Consultar a quantidade de pontos de experiência (XP) atuais de um jogador específico.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - A estrutura de dados interna do jogador deve conter o campo de experiência.

    Acoplamento:
        Entrada:
            nome: string com o nome do jogador a ser consultado.
        Saída:
            pontos de experiência obtidos.
        Retornos:
            (0, xp): sucesso, retorna o código e o valor numérico de experiência.
            (1, None): erro por ausência do campo "xp" no registro do jogador.
            (2, None): erro por jogador não cadastrado ou nome inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve corresponder a um jogador previamente cadastrado no sistema.

        Assertivas de saída:
            - se retornar (0, xp), o valor é numérico e reflete o acumulado atual de experiência do jogador.
            - se retornar códigos de erro (1 ou 2), o segundo parâmetro deve ser None.

    Hipóteses e restrições:
        - Nenhuma alteração de estado ocorre na estrutura interna durante uma consulta.
    """
    # CT-J08 - consultar XP com jogador inválido
    if not _jogadorExiste(nome):
        return 2, None

    jogador = _jogadores[nome]
    # CT-J09 - consultar XP sem campo xp
    if "xp" not in jogador:
        return 1, None

    # CT-J07 - consultar XP válido
    return 0, jogador["xp"]


def getAtaque(nome):
    """
    Objetivo:
        Consultar o valor do atributo de ataque atual de um jogador específico.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - A estrutura de dados interna do jogador deve conter o campo de ataque.

    Acoplamento:
        Entrada:
            nome: string com o nome do jogador a ser consultado.
        Saída:
            valor de ataque obtido.
        Retornos:
            (0, ataque): sucesso, retorna o código e o valor numérico do ataque.
            (1, None): erro por ausência do campo "ataque" no registro do jogador.
            (2, None): erro por jogador não cadastrado ou nome inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve corresponder a um jogador previamente cadastrado no sistema.

        Assertivas de saída:
            - se retornar (0, ataque), o valor retornado reflete exatamente o poder combatente atualizado do jogador.
            - se retornar códigos de erro (1 ou 2), o segundo parâmetro deve ser None.

    Hipóteses e restrições:
        - Nenhuma alteração de estado ocorre na estrutura interna durante uma consulta.
    """
    # CT-J11 - consultar ataque com jogador inválido
    if not _jogadorExiste(nome):
        return 2, None

    jogador = _jogadores[nome]
    # CT-J12 - consultar ataque sem campo ataque
    if "ataque" not in jogador:
        return 1, None

    # CT-J10 - consultar ataque válido
    return 0, jogador["ataque"]


def getInventario(nome):
    """
    Objetivo:
        Obter de forma segura a lista de itens armazenados no inventário de um jogador.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - A estrutura de dados interna do jogador deve conter a lista de inventário.
        - O retorno deve proteger a lista interna original de modificações externas espúrias.

    Acoplamento:
        Entrada:
            nome: string com o nome do jogador a ser consultado.
        Saída:
            lista de inventário do jogador obtida.
        Retornos:
            (0, inventario): sucesso, retorna uma cópia profunda da lista de itens.
            (1, None): erro por ausência do campo "inventario" no registro do jogador.
            (2, None): erro por jogador não cadastrado ou nome inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve corresponder a um jogador previamente cadastrado no sistema.

        Assertivas de saída:
            - se retornar (0, inventario), a estrutura retornada é uma cópia independente de modo que mutações externas na lista não modifiquem a real lista interna do jogador.
            - se retornar códigos de erro (1 ou 2), o segundo parâmetro deve ser None.

    Hipóteses e restrições:
        - A proteção do encapsulamento do TAD é garantida através de cópia em profundidade.
    """
    # CT-J17 - consultar inventário com jogador inválido
    if not _jogadorExiste(nome):
        return 2, None

    jogador = _jogadores[nome]
    # CT-J18 - consultar inventário sem campo inventário
    if "inventario" not in jogador:
        return 1, None

    # CT-J16 - consultar inventário válido
    return 0, copy.deepcopy(jogador["inventario"])


def receberDanoJogador(nome, dano):
    """
    Objetivo:
        Aplicar uma redução nos pontos de vida do jogador baseada em uma quantidade de dano sofrido.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - O valor do dano deve ser numérico, não nulo e maior ou igual a zero.
        - Os pontos de vida resultantes não podem decrescer abaixo de zero.
        - Caso a vida chegue a zero, o estado de vitalidade do jogador deve ser definido como falso (morto).

    Acoplamento:
        Entrada:
            nome: string contendo o nome do jogador.
            dano: valor int ou float correspondente ao dano a ser aplicado.
        Saída:
            pontos de vida e estado de vitalidade do jogador atualizados.
        Retornos:
            0: dano aplicado com sucesso.
            1: erro ao tentar consultar ou ler a vida atual do jogador.
            2: erro por jogador inexistente ou valor de dano inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser de um jogador cadastrado.
            - dano deve ser int ou float maior ou igual a zero.
            - dano não deve ser None.

        Assertivas de saída:
            - se retornar 0, a vida do jogador foi decrementada e limitada a no mínimo 0.
            - se retornar 0 e a vida atingir 0, o atributo "vivo" passa obrigatoriamente a ser False.
            - se retornar 1 ou 2, o estado dos atributos do jogador permanece intacto.

    Hipóteses e restrições:
        - Esta função não calcula reduções de armadura; ela aplica o dano absoluto direto ao montante de vida.
    """
    # CT-J24 - jogador inválido
    if not _jogadorExiste(nome):
        return 2

    # CT-J23 - dano inválido
    if dano is None or not isinstance(dano, (int, float)) or dano < 0:
        return 2

    codigo, vida = getVida(nome)
    if codigo != 0:
        return 1

    # CT-J22 - aplicar dano válido
    jogador = _jogadores[nome]
    jogador["vida"] = max(0, vida - dano)

    if jogador["vida"] == 0:
        jogador["vivo"] = False

    return 0


def curarJogador(nome, valor):
    """
    Objetivo:
        Incrementar os pontos de vida do jogador baseado em um valor de cura recebido.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - O valor da cura deve ser numérico, não nulo e maior ou igual a zero.
        - O jogador não pode receber cura se já estiver com seus pontos de vida em capacidade máxima.
        - A vida pós-cura não pode exceder o limite máximo estabelecido pelo atributo "vida_max".

    Acoplamento:
        Entrada:
            nome: string contendo o nome do jogador.
            valor: valor int ou float correspondente à cura aplicada.
        Saída:
            pontos de vida do jogador atualizados.
        Retornos:
            0: cura aplicada com sucesso.
            1: erro caso o jogador já possua vida máxima ou falha em ler os campos limites.
            2: erro por jogador inexistente ou valor de cura inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser de um jogador cadastrado.
            - valor deve ser int ou float maior ou igual a zero.
            - valor não deve ser None.

        Assertivas de saída:
            - se retornar 0, a vida do jogador aumentou, sem nunca ultrapassar o campo "vida_max".
            - se retornar 1, o valor de vida atual já era exatamente igual ou maior que "vida_max".
            - se retornar 2, nenhum parâmetro interno de vida foi alterado.

    Hipóteses e restrições:
        - Personagens mortos não possuem impedimento explícito de cura nesta camada caso a vida esteja menor que o máximo, operando sob regras gerais.
    """
    # parâmetro inválido
    if not _jogadorExiste(nome):
        return 2

    if valor is None or not isinstance(valor, (int, float)) or valor < 0:
        return 2

    codigo, vida = getVida(nome)
    if codigo != 0:
        return 1

    jogador = _jogadores[nome]
    if "vida_max" not in jogador:
        return 1

    # CT-J26 - vida cheia
    if vida >= jogador["vida_max"]:
        return 1

    # CT-J25 - cura aplicada corretamente
    jogador["vida"] = min(vida + valor, jogador["vida_max"])
    return 0


def ganharXP(nome, xp):
    """
    Objetivo:
        Incrementar o montante total de pontos de experiência (XP) acumulados pelo jogador.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - O valor de experiência ganho deve ser numérico, não nulo e maior ou igual a zero.

    Acoplamento:
        Entrada:
            nome: string contendo o nome do jogador.
            xp: valor int ou float correspondente à experiência adquirida.
        Saída:
            pontos de experiência (xp) do jogador incrementados.
        Retornos:
            0: experiência adicionada com sucesso.
            1: erro ao tentar consultar ou ler o XP atual do jogador.
            2: erro por jogador inexistente ou quantidade de XP inválida.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser de um jogador cadastrado.
            - xp deve ser int ou float maior ou igual a zero.

        Assertivas de saída:
            - se retornar 0, o campo "xp" interno do jogador refletirá de maneira exata o acúmulo da soma anterior com o novo valor.
            - se retornar 1 ou 2, nenhum incremento é realizado.

    Hipóteses e restrições:
        - Ganhar XP não engatilha automaticamente o método de atualizar ataque; a evolução de poder deve ser disparada externamente.
    """
    # jogador inválido
    if not _jogadorExiste(nome):
        return 2

    # CT-J29 - ganhar XP inválido
    if xp is None or not isinstance(xp, (int, float)) or xp < 0:
        return 2

    codigo, xpAtual = getXP(nome)
    if codigo != 0:
        return 1

    # CT-J28 - ganhar XP válido
    _jogadores[nome]["xp"] = xpAtual + xp
    return 0


def atualizarAtaque(nome):
    """
    Objetivo:
        Recalcular e atualizar o poder de ataque do jogador proporcionalmente com base em sua experiência.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - O ataque deve ser recalculado pela fórmula padrão: 10 somado à divisão inteira da experiência por 100.

    Acoplamento:
        Entrada:
            nome: string contendo o nome do jogador.
        Saída:
            atributo de ataque do jogador atualizado internamente.
        Retornos:
            0: ataque recalculado e atualizado com sucesso.
            1: erro obtido ao ler a experiência do jogador.
            2: erro por jogador inválido ou não cadastrado.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser de um jogador cadastrado.

        Assertivas de saída:
            - se retornar 0, o novo valor de ataque passa a respeitar rigorosamente a equação funcional baseada no XP.
            - se retornar 1 ou 2, o atributo de ataque permanece sem modificações.

    Hipóteses e restrições:
        - O cálculo utiliza estritamente o operador de divisão inteira (//) para determinar os bônus de patamar de poder.
    """
    # CT-J31 - jogador inválido
    if not _jogadorExiste(nome):
        return 2

    codigo, xp = getXP(nome)
    if codigo != 0:
        return 1

    # CT-J30 - atualizar ataque corretamente
    _jogadores[nome]["ataque"] = 10 + (xp // 100)
    return 0


def adicionarItemJogador(nome, item):
    """
    Objetivo:
        Adicionar um objeto de item estruturado ao fim da lista de inventário de um jogador.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - O item a ser adicionado não pode ser nulo.
        - O inventário do jogador não pode ultrapassar o limite máximo de armazenamento fixado em 5 itens.

    Acoplamento:
        Entrada:
            nome: string contendo o nome do jogador.
            item: dicionário contendo os dados e propriedades estruturadas do item.
        Saída:
            lista interna do inventário do jogador atualizada por acréscimo.
        Retornos:
            0: item adicionado com sucesso ao inventário.
            1: erro decorrente de falha de leitura ou capacidade de inventário esgotada (limite >= 5).
            2: erro por jogador inexistente ou item inválido/nulo.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser de um jogador cadastrado.
            - item deve ser um dicionário estruturado válido e não ser None.

        Assertivas de saída:
            - se retornar 0, o item foi anexado ao final da lista de inventário real do jogador.
            - se retornar 1 ou 2, o inventário permanece com o mesmo tamanho e elementos de antes.

    Hipóteses e restrições:
        - O módulo jogador não valida os campos internos do item recebido (como nome ou valor do item), confiando na validação prévia do módulo Item.
    """
    # CT-J34 - parâmetro inválido
    if not _jogadorExiste(nome):
        return 2

    if item is None:
        return 2

    codigo, inventario = getInventario(nome)
    if codigo != 0:
        return 1

    # CT-J33 - inventário cheio
    if len(inventario) >= 5:
        return 1

    # CT-J32 - adicionar item válido
    _jogadores[nome]["inventario"].append(item)
    return 0


def usarItemJogador(nome, item):
    """
    Objetivo:
        Consumir um item contido no inventário do jogador, aplicando seus respectivos efeitos e removendo-o em seguida.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - O item a ser utilizado não pode ser nulo.
        - O item especificado deve obrigatoriamente constar na lista atual de itens do jogador.
        - Se o tipo do item for "cura", incrementa diretamente a vida do jogador.
        - Se o tipo do item for "ataque", incrementa diretamente o ataque do jogador.
        - Ao final do uso com sucesso, o item deve ser expelido da lista de inventário.

    Acoplamento:
        Entrada:
            nome: string contendo o nome do jogador.
            item: dicionário contendo as propriedades do item a ser consumido.
        Saída:
            atributos afetados do jogador (vida ou ataque) modificados e item removido do inventário.
        Retornos:
            0: item consumido e aplicado com sucesso.
            1: erro decorrente de item inexistente dentro do inventário ou falha estrutural.
            2: erro por jogador inexistente ou objeto item nulo.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser de um jogador cadastrado.
            - item deve constar na lista extraída do inventário do jogador.
            - item não deve ser None.

        Assertivas de saída:
            - se retornar 0, o item foi completamente removido da lista interna do inventário.
            - se retornar 0, as propriedades do jogador mudaram de forma correspondente ao tipo e valor do item.
            - se retornar 1 ou 2, nenhuma alteração de atributos ou remoção de itens é executada.

    Hipóteses e restrições:
        - O item é comparado por igualdade estrutural completa de seus campos dentro da lista.
    """
    # CT-J37 - parâmetro inválido
    if not _jogadorExiste(nome):
        return 2

    if item is None:
        return 2

    codigo, inventario = getInventario(nome)
    if codigo != 0:
        return 1

    # CT-J36 - usar item inexistente
    if item not in inventario:
        return 1

    # CT-J35 - usar item válido
    jogador = _jogadores[nome]
    if item.get("tipo") == "cura":
        jogador["vida"] += item["valor"]
    elif item.get("tipo") == "ataque":
        jogador["ataque"] += item["valor"]

    jogador["inventario"].remove(item)
    return 0