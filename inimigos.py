_VIDA_MAX = 100
_ATAQUE_MAX = 50

_inimigos = []


def criarInimigo(nome, vida, ataque):
    """
    Objetivo:
        Criar um novo inimigo, armazená-lo no módulo Inimigo e retornar seu identificador.

    Requisitos funcionais:
        - O inimigo deve possuir nome, vida e ataque.
        - O nome não pode ser vazio.
        - Vida e ataque devem ser valores numéricos positivos.
        - A vida não pode ser menor que o ataque.
        - Vida e ataque devem respeitar os limites máximos definidos pelo jogo.
        - Em caso de sucesso, o inimigo deve ser armazenado na lista interna do módulo.

    Acoplamento:
        Entrada:
            nome: nome do inimigo.
            vida: quantidade de vida inicial.
            ataque: valor de ataque inicial.
        Saída:
            id_inimigo: identificador do inimigo criado.
        Retornos:
            (0, id_inimigo): inimigo criado com sucesso.
            (1, None): erro por regra do jogo.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser uma string não vazia.
            - vida deve ser int ou float maior que zero.
            - ataque deve ser int ou float maior que zero.

        Assertivas de saída:
            - se retornar (0, id_inimigo), o inimigo foi armazenado na lista interna.
            - se retornar (0, id_inimigo), id_inimigo referencia um inimigo válido.
            - se retornar (1, None), nenhum inimigo foi criado.
            - se retornar (2, None), nenhum inimigo foi criado.

    Hipóteses e restrições:
        - A estrutura do inimigo é encapsulada pelo módulo.
        - Outros módulos devem utilizar apenas o id_inimigo retornado.
    """

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

    _inimigos.append(inimigo)
    return 0, len(_inimigos) - 1


def getVidaInimigo(id_inimigo):
    """
    Objetivo:
        Consultar a vida atual de um inimigo.

    Requisitos funcionais:
        - O inimigo deve existir no módulo.
        - A função deve retornar a vida associada ao inimigo informado.

    Acoplamento:
        Entrada:
            id_inimigo: identificador do inimigo.
        Saída:
            vida: valor atual da vida do inimigo.
        Retornos:
            (0, vida): consulta realizada com sucesso.
            (2, None): identificador inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - id_inimigo deve referenciar um inimigo existente.

        Assertivas de saída:
            - se retornar (0, vida), vida corresponde ao valor armazenado no módulo.
            - se retornar (2, None), nenhuma informação é retornada.

    Hipóteses e restrições:
        - A estrutura interna do inimigo não é exposta ao módulo cliente.
    """

    # CT-I08: inimigo inválido
    if not verificaIdInimigoValido(id_inimigo):
        return 2, None

    inimigo = _inimigos[id_inimigo]

    # CT-I07: vida retornada com sucesso
    return 0, inimigo["vida"]


def getAtaqueInimigo(id_inimigo):
    """
    Objetivo:
        Consultar o ataque de um inimigo.

    Requisitos funcionais:
        - O inimigo deve existir no módulo.
        - A função deve retornar o ataque associado ao inimigo informado.

    Acoplamento:
        Entrada:
            id_inimigo: identificador do inimigo.
        Saída:
            ataque: valor de ataque do inimigo.
        Retornos:
            (0, ataque): consulta realizada com sucesso.
            (2, None): identificador inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - id_inimigo deve referenciar um inimigo existente.

        Assertivas de saída:
            - se retornar (0, ataque), ataque corresponde ao valor armazenado no módulo.
            - se retornar (2, None), nenhuma informação é retornada.

    Hipóteses e restrições:
        - A estrutura interna do inimigo não é exposta ao módulo cliente.
    """

    # CT-I10: inimigo inválido
    if not verificaIdInimigoValido(id_inimigo):
        return 2, None

    inimigo = _inimigos[id_inimigo]

    # CT-I9: ataque retornado com sucesso
    return 0, inimigo["ataque"]


def receberDanoInimigo(id_inimigo, dano):
    """
    Objetivo:
        Aplicar dano a um inimigo.

    Requisitos funcionais:
        - O inimigo deve existir.
        - O dano deve ser um valor numérico válido.
        - A vida do inimigo deve ser reduzida pelo valor do dano.
        - A vida do inimigo não pode assumir valores negativos.
        - Não é permitido aplicar dano em inimigo já derrotado.

    Acoplamento:
        Entrada:
            id_inimigo: identificador do inimigo.
            dano: quantidade de dano a ser aplicada.
        Saída:
            estado atualizado do inimigo.
        Retornos:
            0: dano aplicado com sucesso.
            1: erro por regra do jogo.
            2: parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - id_inimigo deve referenciar um inimigo existente.
            - dano deve ser int ou float maior ou igual a zero.

        Assertivas de saída:
            - se retornar 0, a vida do inimigo foi atualizada.
            - se retornar 0, a vida final nunca será negativa.
            - se retornar 1, o estado do inimigo permanece inalterado.
            - se retornar 2, o estado do inimigo permanece inalterado.

    Hipóteses e restrições:
        - O acesso ao inimigo ocorre exclusivamente através do identificador.
    """

    # CT-I14: inimigo inválido
    if not verificaIdInimigoValido(id_inimigo):
        return 2

    inimigo = _inimigos[id_inimigo]
    # CT-I13: dano inválido
    if dano is None or not isinstance(dano, (int, float)) or dano < 0:
        return 2

    # CT-I15: inimigo já derrotado
    if inimigo["vida"] <= 0:
        return 1

    # CT-I11 e CT-I12: dano aplicado
    inimigo["vida"] -= dano

    if inimigo["vida"] < 0:
        inimigo["vida"] = 0

    return 0


def inimigoVivo(id_inimigo):
    """
    Objetivo:
        Verificar se um inimigo está vivo ou derrotado.

    Requisitos funcionais:
        - O inimigo deve existir.
        - A função deve retornar True quando a vida for maior que zero.
        - A função deve retornar False quando a vida for igual a zero.

    Acoplamento:
        Entrada:
            id_inimigo: identificador do inimigo.
        Saída:
            estado de vida do inimigo.
        Retornos:
            (0, True): inimigo vivo.
            (0, False): inimigo derrotado.
            (2, None): identificador inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - id_inimigo deve referenciar um inimigo existente.

        Assertivas de saída:
            - se retornar (0, True), a vida do inimigo é maior que zero.
            - se retornar (0, False), a vida do inimigo é igual a zero.
            - se retornar (2, None), nenhuma informação é retornada.

    Hipóteses e restrições:
        - A verificação utiliza exclusivamente os dados encapsulados do módulo.
    """

    # CT-I18: inimigo inválido
    if not verificaIdInimigoValido(id_inimigo):
        return 2, None

    inimigo = _inimigos[id_inimigo]

    # CT-I16: inimigo vivo
    if inimigo["vida"] > 0:
        return 0, True

    # CT-I17: inimigo derrotado
    return 0, False


def verificaIdInimigoValido(id_inimigo):
    """
    Objetivo:
        Verificar se um identificador referencia um inimigo válido.

    Requisitos funcionais:
        - O identificador deve ser validado antes do acesso à lista interna.
        - IDs negativos, inexistentes ou não inteiros devem ser rejeitados.

    Acoplamento:
        Entrada:
            id_inimigo: identificador a ser validado.
        Saída:
            valor booleano indicando validade.
        Retornos:
            True: identificador válido.
            False: identificador inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - id_inimigo pode ser qualquer valor recebido pelo módulo.

        Assertivas de saída:
            - se retornar True, o id referencia um inimigo existente.
            - se retornar False, o id não referencia um inimigo existente.
            - a lista interna não é modificada.

    Hipóteses e restrições:
        - O id corresponde à posição do inimigo na lista encapsulada.
    """

    if id_inimigo is None or not isinstance(id_inimigo, int) or id_inimigo < 0:
        return False

    if id_inimigo >= len(_inimigos):
        return False

    return True


def exportarEstadoInimigos():
    """
    Objetivo:
        Exportar uma cópia do estado atual dos inimigos.

    Requisitos funcionais:
        - A função deve disponibilizar os dados necessários para persistência.
        - A lista interna não deve ser exposta diretamente.

    Acoplamento:
        Entrada:
            nenhuma.
        Saída:
            lista contendo cópias dos inimigos.
        Retornos:
            lista de inimigos exportados.

    Condições de acoplamento:
        Assertivas de entrada:
            - a função não recebe parâmetros.

        Assertivas de saída:
            - o retorno deve ser uma lista.
            - alterações na lista retornada não devem alterar diretamente a lista interna.
            - a ordem dos inimigos deve ser preservada.

    Hipóteses e restrições:
        - O formato do arquivo é responsabilidade do módulo de persistência.
    """

    estado = []

    for inimigo in _inimigos:
        estado.append(inimigo.copy())

    return estado


def restaurarEstadoInimigos(estado):
    """
    Objetivo:
        Restaurar o estado dos inimigos previamente exportado.

    Requisitos funcionais:
        - O estado deve ser uma lista válida.
        - Cada inimigo deve possuir nome, vida e ataque.
        - Apenas estados válidos podem ser restaurados.

    Acoplamento:
        Entrada:
            estado: lista contendo os inimigos exportados.
        Saída:
            lista interna atualizada.
        Retornos:
            0: restauração realizada com sucesso.
            2: parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - estado deve ser uma lista.
            - cada elemento deve ser um dicionário válido.
            - cada inimigo deve possuir nome, vida e ataque válidos.

        Assertivas de saída:
            - se retornar 0, a lista interna foi substituída pelo estado restaurado.
            - se retornar 2, nenhum estado inválido deve ser carregado.
            - a ordem dos inimigos deve ser preservada.

    Hipóteses e restrições:
        - O estado foi obtido previamente através da função de exportação.
    """
    
    if estado is None or not isinstance(estado, list):
        return 2

    nova_lista = []

    for inimigo in estado:
        if not isinstance(inimigo, dict):
            return 2

        nome = inimigo.get("nome")
        vida = inimigo.get("vida")
        ataque = inimigo.get("ataque")

        if nome is None or not isinstance(nome, str) or not nome.strip():
            return 2

        if vida is None or not isinstance(vida, (int, float)) or vida < 0:
            return 2

        if ataque is None or not isinstance(ataque, (int, float)) or ataque <= 0:
            return 2

        nova_lista.append({
            "nome": nome.strip(),
            "vida": vida,
            "ataque": ataque
        })

    _inimigos.clear()
    _inimigos.extend(nova_lista)

    return 0