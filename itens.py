_itens = []


def criarItem(nome, tipo, valor):
    """
    Objetivo:
        Criar um novo item, armazená-lo no módulo Item e retornar seu identificador.

    Requisitos funcionais:
        - O item deve possuir nome, tipo e valor.
        - O nome não pode ser vazio.
        - O tipo deve ser um dos tipos aceitos pelo jogo: "cura", "ataque" ou "chave".
        - O valor do item deve ser numérico e maior que zero.
        - Em caso de sucesso, o item deve ser armazenado na lista interna de itens.

    Acoplamento:
        Entrada:
            nome: nome do item a ser criado.
            tipo: tipo do item, podendo ser "cura", "ataque" ou "chave".
            valor: valor aplicado pelo item.
        Saída:
            id_item: identificador do item criado, correspondente à sua posição na lista interna.
        Retornos:
            (0, id_item): item criado com sucesso.
            (1, None): erro ao criar item por regra do jogo.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser uma string não vazia.
            - tipo deve ser uma string pertencente aos tipos aceitos pelo módulo.
            - valor deve ser int ou float maior que zero.

        Assertivas de saída:
            - se retornar (0, id_item), o item foi criado e armazenado na lista interna do módulo.
            - se retornar (0, id_item), id_item referencia o item criado.
            - se retornar (1, None), nenhum item foi criado por violação de regra do jogo.
            - se retornar (2, None), nenhum item foi criado por parâmetro inválido.
            - outros módulos devem usar apenas o id_item retornado, sem acessar a estrutura interna do item.

    Hipóteses e restrições:
        - A estrutura interna do item é encapsulada no módulo Item.
        - O id_item deve ser utilizado nas demais funções de acesso do módulo.
    """
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

    _itens.append(item)
    id_item = len(_itens) - 1
    return 0, id_item

# Funções de consulta de tipo e valor de item
def getTipoItem(id_item):
    """
    Objetivo:
        Consultar o tipo de um item.

    Requisitos funcionais:
        - O item deve existir no módulo.
        - A função deve retornar o tipo associado ao item informado.

    Acoplamento:
        Entrada:
            id_item: identificador do item.
        Saída:
            tipo: tipo do item.
        Retornos:
            (0, tipo): consulta realizada com sucesso.
            (2, None): identificador inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - id_item deve referenciar um item existente.

        Assertivas de saída:
            - se retornar (0, tipo), tipo corresponde ao valor armazenado no módulo.
            - se retornar (2, None), nenhuma informação é retornada.

    Hipóteses e restrições:
        - A estrutura interna do item não é exposta ao módulo cliente.
    """

    if not _verificaIdItemValido(id_item):
        return 2, None

    return 0, _itens[id_item]["tipo"]

def getValorItem(id_item):
    """
    Objetivo:
        Consultar o valor de um item.

    Requisitos funcionais:
        - O item deve existir no módulo.
        - A função deve retornar o valor associado ao item informado.

    Acoplamento:
        Entrada:
            id_item: identificador do item.
        Saída:
            valor: valor do item.
        Retornos:
            (0, valor): consulta realizada com sucesso.
            (2, None): identificador inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - id_item deve referenciar um item existente.

        Assertivas de saída:
            - se retornar (0, valor), valor corresponde ao valor armazenado no módulo.
            - se retornar (2, None), nenhuma informação é retornada.

    Hipóteses e restrições:
        - A estrutura interna do item não é exposta ao módulo cliente.
    """

    if not _verificaIdItemValido(id_item):
        return 2, None

    return 0, _itens[id_item]["valor"]

def _verificaIdItemValido(id_item):
    """
    Objetivo:
        Verificar se um identificador de item corresponde a um item existente no módulo.

    Requisitos funcionais:
        - O identificador deve ser validado antes de acessar a lista interna de itens.
        - IDs inexistentes, negativos ou não inteiros devem ser considerados inválidos.

    Acoplamento:
        Entrada:
            id_item: identificador do item.
        Saída:
            valor booleano indicando se o identificador é válido.
        Retornos:
            True: id_item válido.
            False: id_item inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - id_item deve ser um inteiro.
            - id_item deve ser maior ou igual a zero.

        Assertivas de saída:
            - se retornar True, id_item referencia um item existente na lista interna.
            - se retornar False, id_item não referencia um item válido.
            - a função não altera a lista interna de itens.

    Hipóteses e restrições:
        - O id_item representa a posição do item na lista interna encapsulada pelo módulo.
    """
    if id_item is None or not isinstance(id_item, int) or id_item < 0:
        return False

    if id_item >= len(_itens):
        return False

    return True

def _tipoValido(tipo):
    tiposValidos = ("cura", "ataque", "chave")
    return tipo in tiposValidos

def exportarEstadoItens():
    """
    Objetivo:
        Exportar o estado atual dos itens para que outro módulo possa persistir os dados.

    Requisitos funcionais:
        - A função deve retornar os itens cadastrados no módulo.
        - A função deve retornar uma cópia dos itens, sem expor diretamente a lista interna.
        - O estado exportado deve poder ser usado posteriormente para restauração.

    Acoplamento:
        Entrada:
            Nenhuma.
        Saída:
            estado: lista contendo cópias dos itens armazenados.
        Retornos:
            estado: lista de dicionários com os dados dos itens.

    Condições de acoplamento:
        Assertivas de entrada:
            - a função não recebe parâmetros.
            - a lista interna de itens pode estar vazia ou conter itens cadastrados.

        Assertivas de saída:
            - o retorno deve ser uma lista.
            - cada elemento retornado deve ser uma cópia de um item armazenado no módulo.
            - alterações realizadas na lista retornada não devem alterar diretamente a lista interna _itens.
            - a ordem dos itens exportados deve ser preservada para manter a correspondência dos ids.

    Hipóteses e restrições:
        - O formato final do arquivo não é responsabilidade do módulo Item.
        - O módulo Item apenas fornece o estado interno em uma estrutura simples.
    """
    estado = []

    for item in _itens:
        estado.append(item.copy())

    return estado

def restaurarEstadoItens(estado):
    """
    Objetivo:
        Restaurar a lista interna de itens a partir de um estado previamente exportado.

    Requisitos funcionais:
        - O estado recebido deve ser uma lista.
        - Cada item da lista deve possuir nome, tipo e valor.
        - O nome deve ser válido.
        - O tipo deve ser aceito pelo módulo.
        - O valor deve ser numérico e maior que zero.
        - A lista interna de itens deve ser substituída pelo estado restaurado apenas se todo o estado for válido.

    Acoplamento:
        Entrada:
            estado: lista contendo os itens a serem restaurados.
        Saída:
            lista interna de itens atualizada.
        Retornos:
            0: estado restaurado com sucesso.
            2: parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - estado deve ser uma lista.
            - cada elemento de estado deve ser um dicionário.
            - cada dicionário deve possuir os campos "nome", "tipo" e "valor".
            - o campo "nome" deve ser uma string não vazia.
            - o campo "tipo" deve ser reconhecido pelo módulo.
            - o campo "valor" deve ser int ou float maior que zero.

        Assertivas de saída:
            - se retornar 0, a lista interna de itens foi substituída pelo estado restaurado.
            - se retornar 0, a ordem dos itens foi preservada para manter a correspondência dos ids.
            - se retornar 2, o estado não foi restaurado por parâmetro inválido.
            - se retornar 2, nenhum estado inválido deve ser carregado na lista interna.

    Hipóteses e restrições:
        - A função recebe uma estrutura já lida pelo módulo responsável pela persistência.
        - O módulo Item não conhece o formato do arquivo usado para salvar os dados.
    """
    if estado is None or not isinstance(estado, list):
        return 2

    nova_lista = []

    for item in estado:
        if not isinstance(item, dict):
            return 2

        nome = item.get("nome")
        tipo = item.get("tipo")
        valor = item.get("valor")

        if nome is None or not isinstance(nome, str) or not nome.strip():
            return 2

        if tipo is None or not isinstance(tipo, str) or not _tipoValido(tipo):
            return 2

        if valor is None or not isinstance(valor, (int, float)) or valor <= 0:
            return 2

        novo_item = {
            "nome": nome.strip(),
            "tipo": tipo,
            "valor": valor
        }

        nova_lista.append(novo_item)

    _itens.clear()
    _itens.extend(nova_lista)

    return 0
