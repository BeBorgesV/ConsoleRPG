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
    "usarItemJogador", 
    "exportarJogador",
    "restaurarJogador",
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
            - se retornar códigos de erro (1 ou 2), o second parâmetro deve ser None.

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


def adicionarItemJogador(nome, id_item):
    """
    Objetivo:
        Adicionar o identificador de um item ao fim da lista de inventário de um jogador.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - O identificador do item (id_item) deve ser um número inteiro válido.
        - O inventário do jogador não pode ultrapassar o limite máximo de armazenamento fixado em 5 itens.

    Acoplamento:
        Entrada:
            nome: string contendo o nome do jogador.
            id_item: inteiro correspondente ao identificador do item.
        Saída:
            lista interna do inventário do jogador atualizada com o novo id.
        Retornos:
            0: identificador do item adicionado com sucesso ao inventário.
            1: erro decorrente de capacidade de inventário esgotada (limite >= 5).
            2: erro por jogador inexistente ou id_item inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser de um jogador cadastrado.
            - id_item deve ser um número inteiro maior ou igual a zero.
            - id_item não deve ser None.

        Assertivas de saída:
            - se retornar 0, o id_item foi anexado ao final da lista de inventário real do jogador.
            - se retornar 1 ou 2, o inventário permanece inalterado.

    Hipóteses e restrições:
        - O módulo jogador armazena estritamente o ID numérico e delega a validação da existência física do item para quem chama ou para o módulo Item.
    """
    # CT-J34 - parâmetro inválido
    if not _jogadorExiste(nome):
        return 2

    if id_item is None or not isinstance(id_item, int) or id_item < 0:
        return 2

    codigo, inventario = getInventario(nome)
    if codigo != 0:
        return 1

    # CT-J33 - inventário cheio
    if len(inventario) >= 5:
        return 1

    # CT-J32 - adicionar ID válido
    _jogadores[nome]["inventario"].append(id_item)
    return 0


def usarItemJogador(nome, id_item):
    """
    Objetivo:
        Consumir um item do inventário do jogador pelo seu identificador, consultando suas propriedades de forma encapsulada através do módulo de itens e aplicando os bônus correspondentes.

    Requisitos funcionais:
        - O jogador associado ao nome deve existir.
        - O id_item não pode ser nulo e deve ser um inteiro válido e maior ou igual a zero.
        - O id_item especificado deve obrigatoriamente constar na lista de inventário do jogador.
        - O tipo e o valor do item devem ser obtidos estritamente pelas funções exportadas do módulo 'itens'.
        - Ao final do uso com sucesso, o id_item deve ser removido do inventário.

    Acoplamento:
        Entrada:
            nome: string contendo o nome do jogador.
            id_item: número inteiro identificador do item a ser consumido.
        Saída:
            item removido do inventário e atributos do jogador (vida ou ataque) modificados via interface.
        Retornos:
            0: item consumido com sucesso.
            1: erro decorrente de ID inexistente no inventário ou falha ao obter dados do item.
            2: erro por jogador inexistente ou id_item inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser de um jogador cadastrado.
            - id_item deve constar na lista extraída do inventário do jogador.
            - id_item deve ser um inteiro válido e maior ou igual a zero.

        Assertivas de saída:
            - se retornar 0, o id_item foi completamente removido da lista interna do inventário.
            - se retornar 0 e o tipo do item for "cura", a função curarJogador foi acionada com o valor do item.
            - se retornar 0 e o tipo do item for "ataque", o atributo 'ataque' do jogador foi incrementado com o valor do item.
            - se retornar 1 ou 2, nenhuma alteração de atributos ou remoção é executada.

    Hipóteses e restrições:
        - O encapsulamento é mantido utilizando as funções interfaceadoras do módulo 'itens', impedindo o jogador de acessar diretamente a estrutura interna do item.
    """
    # CT-J37 - parâmetro inválido
    if not _jogadorExiste(nome):
        return 2

    # Correção: Adicionada validação robusta se id_item < 0 em consistência com adicionarItemJogador
    if id_item is None or not isinstance(id_item, int) or id_item < 0:
        return 2

    jogador = _jogadores[nome]
    
    # CT-J36 - usar item inexistente no inventário
    if id_item not in jogador["inventario"]:
        return 1

    # INTERAÇÃO ENCAPSULADA COM O MÓDULO ITENS
    import itens
    
    # Obtém o tipo e o valor do item sem acessar dicionários diretamente
    codigo_tipo, tipo_item = itens.getTipoItem(id_item)
    codigo_valor, valor_item = itens.getValorItem(id_item)
    
    if codigo_tipo != 0 or codigo_valor != 0:
        return 1  # Falha ao ler propriedades do item do módulo externo

    # Aplica o efeito utilizando as regras do jogador
    if tipo_item == "cura":
        curarJogador(nome, valor_item)
    elif tipo_item == "ataque":
        jogador["ataque"] += valor_item

    # Remove o ID do inventário do jogador
    jogador["inventario"].remove(id_item)
    return 0


def exportarJogador(nome):
    """
    Objetivo:
        Exportar o estado interno completo de um jogador específico a partir de uma cópia profunda (deep copy).

    Requisitos funcionais:
        - O jogador associado ao nome deve existir no sistema.
        - O nome deve ser uma string válida e não vazia.
        - Em caso de sucesso, deve retornar uma cópia isolada do dicionário para persistência ou auditoria externa.

    Acoplamento:
        Entrada:
            nome: string contendo o nome identificador do jogador.
        Saída:
            cópia segura do dicionário estruturado do jogador.
        Retornos:
            (0, jogador_copia): sucesso, retorna o código e o dicionário exportado.
            2: erro por jogador não cadastrado, nome vazio ou parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve corresponder a um jogador previamente cadastrado.
            - nome não deve ser vazio ou None.

        Assertivas de saída:
            - se retornar (0, jogador_copia), a estrutura retornada é um dict contendo todos os atributos atuais.
            - se retornar (0, jogador_copia), modificações externas no dict retornado não afetam o estado real do jogador armazenado em _jogadores.
            - se retornar 2, nenhum dado é exposto.

    Hipóteses e restrições:
        - O formato exportado depende da estrutura atual do dicionário interno do TAD Jogador.
    """
    # Validação de parâmetro e existência
    if nome is None or not isinstance(nome, str) or not nome.strip():
        return 2

    if not _jogadorExiste(nome.strip()):
        return 2

    # Retorna cópia profunda e isolada para garantir o encapsulamento
    jogador_copia = copy.deepcopy(_jogadores[nome.strip()])
    return 0, jogador_copia


def restaurarJogador(dados_externos):
    """
    Objetivo:
        Restaurar ou sobrescrever o estado interno de um jogador no sistema a partir de um 
        dicionário externo, realizando validações rigorosas de segurança, tipos e limites 
        de atributos antes da gravação.

    Requisitos funcionais:
        - O parâmetro dados_externos deve ser obrigatoriamente um dicionário válido.
        - Deve conter todas as chaves obrigatórias do TAD: "nome", "vida", "vida_max", "xp", "ataque", "vivo", "inventario".
        - Os tipos e limites lógicos de cada atributo devem ser validados (ex: vida não pode ser negativa ou maior que vida_max).
        - O inventário não pode ter mais do que 5 itens e todos os IDs guardados devem ser inteiros válidos.

    Acoplamento:
        Entrada:
            dados_externos: dicionário contendo a estrutura de atributos de um jogador a ser restaurado.
        Saída:
            sobrescrita ou criação do registro do jogador na estrutura interna _jogadores.
        Retornos:
            0: jogador restaurado com sucesso.
            1: erro de validação (atributos fora dos limites, tipos incorretos ou chaves em falta).
            2: parâmetro inválido (dados_externos nulo ou não é um dicionário).

    Condições de acoplamento:
        Assertivas de entrada:
            - dados_externos deve ser um dict e não pode ser None.

        Assertivas de saída:
            - se retornar 0, uma cópia profunda (deep copy) de dados_externos foi guardada em _jogadores no índice correspondente ao nome limpo.
            - se retornar 1 ou 2, nenhuma alteração é feita na estrutura interna de _jogadores.

    Hipóteses e restrições:
        - Esta função isola completamente o estado interno através de uma cópia profunda, blindando o TAD contra modificações externas subsequentes na referência enviada.
    """
    # CT-J43: Parâmetro inválido
    if dados_externos is None or not isinstance(dados_externos, dict):
        return 2

    # Verificação de existência de todas as chaves obrigatórias
    chaves_obrigatorias = ["nome", "vida", "vida_max", "xp", "ataque", "vivo", "inventario"]
    for chave in chaves_obrigatorias:
        if chave not in dados_externos:
            return 1  # CT-J42: Estrutura incompleta

    nome = dados_externos["nome"]
    vida = dados_externos["vida"]
    vida_max = dados_externos["vida_max"]
    xp = dados_externos["xp"]
    ataque = dados_externos["ataque"]
    vivo = dados_externos["vivo"]
    inventario = dados_externos["inventario"]

    # Validações de Tipo e Domínio Lógico (Filtros de Segurança)
    if not isinstance(nome, str) or not nome.strip():
        return 1
    
    if not isinstance(vida_max, (int, float)) or vida_max <= 0:
        return 1

    if not isinstance(vida, (int, float)) or vida < 0 or vida > vida_max:
        return 1

    if not isinstance(xp, (int, float)) or xp < 0:
        return 1

    if not isinstance(ataque, (int, float)) or ataque < 0:
        return 1

    if not isinstance(vivo, bool):
        return 1

    # Consistência lógica de vitalidade (Evitar estados impossíveis como vida=0 e vivo=True)
    if (vida == 0 and vivo is True) or (vida > 0 and vivo is False):
        return 1

    # Validação do inventário baseado em IDs numéricos inteiros
    if not isinstance(inventario, list) or len(inventario) > 5:
        return 1

    for id_item in inventario:
        if not isinstance(id_item, int) or id_item < 0:
            return 1

    # Se passar em todas as barreiras, limpa o nome e salva a cópia profunda
    nome_limpo = nome.strip()
    _jogadores[nome_limpo] = copy.deepcopy(dados_externos)
    _jogadores[nome_limpo]["nome"] = nome_limpo  # Garante o alinhamento sem espaços
    
    return 0