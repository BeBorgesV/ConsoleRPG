import batalha
import salvar
import inimigos
import itens
from jogador import (
    adicionarItemJogador,
    atualizarAtaque,
    criarJogador as _criarJogador,
    ganharXP,
    getAtaque,
    getInventario,
    getVida,
    getXP,
    usarItemJogador
)
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


ITENS_INICIAIS = [
    ((2, 12), "Pocao simples", "cura", 25),
    ((5, 13), "Amuleto de ataque", "ataque", 5),
    ((1, 10), "Chave da clareira", "chave", 1),
    ((8, 5), "Chave da ponte", "chave", 1),
    ((11, 6), "Pocao forte", "cura", 35)
]

INIMIGOS_INICIAIS = [
    ((5, 11), "Lobo da trilha", 35, 7, False),
    ((9, 9), "Bandido do bosque", 45, 9, False),
    ((12, 7), "Guarda do castelo", 55, 11, False),
    ((13, 2), "Chefe do castelo", 75, 13, True)
]

DIRECOES = ["cima", "baixo", "esquerda", "direita"]
COMANDOS_SAIDA = ["salvar e sair", "5"]
ATALHOS = {
    "w": "cima",
    "s": "baixo",
    "a": "esquerda",
    "d": "direita",
    "1": "inventario",
    "2": "mapa",
    "5": "salvar e sair"
}


def criarJogador(nome):
    """
    Objetivo: Criar um novo jogador utilizando o módulo jogador e retornar seu dicionário de estado.

    Requisitos funcionais:
        - O jogador deve ser criado com nome válido.
        - Em caso de sucesso, retorna o dicionário do jogador.

    Acoplamento:
        Entrada:
            nome: nome do jogador.
        Saída:
            jogador: dicionário com os dados do jogador criado.
        Retornos:
            (0, jogador): jogador criado com sucesso.
            (1, None): erro na criação do jogador.

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser uma string não vazia.

        Assertivas de saída:
            - se retornar (0, jogador), jogador é um dicionário válido.
            - se retornar (1, None), nenhum jogador foi criado.

    Hipóteses e restrições:
        - Delega a criação ao módulo jogador (_criarJogador).
    """
    resultado = _criarJogador(nome)

    if isinstance(resultado, dict):
        return 0, resultado

    return resultado, None


def _nomeJogador(jogador):
    """
    Objetivo:
        Retornar o nome do jogador a partir de seu dicionário ou valor direto.

    Requisitos funcionais:
        - Se jogador for dicionário, retorna o valor da chave "nome".
        - Se jogador for string, retorna diretamente.

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador ou string com o nome.
        Saída:
            nome: nome do jogador.
        Retornos:
            str: nome do jogador.
            None: se a chave não existir.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser dict ou str.

        Assertivas de saída:
            - retorna string com o nome ou None.

    Hipóteses e restrições:
        - Função auxiliar interna; não deve ser chamada por outros módulos.
    """
    if isinstance(jogador, dict):
        return jogador.get("nome")

    return jogador


def _posicaoJogador(jogador):
    """
    Objetivo: Retornar a posição atual do jogador no mapa.

    Requisitos funcionais:
        - jogador deve ser um dicionário válido.
        - jogador deve possuir a chave "posicao".

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador.
        Saída:
            posicao: tupla (x, y) com a posição atual.
        Retornos:
            (0, (x, y)): posição obtida com sucesso.
            (1, None): jogador não possui posição definida.
            (2, None): parâmetro inválido.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser um dicionário.

        Assertivas de saída:
            - se retornar (0, posicao), posicao é uma tupla (x, y).
            - se retornar (1, None) ou (2, None), nenhuma posição foi retornada.

    Hipóteses e restrições:
        - Função auxiliar interna; não deve ser chamada por outros módulos.
    """
    if not isinstance(jogador, dict):
        return 2, None

    if "posicao" not in jogador:
        return 1, None

    return 0, jogador["posicao"]



def _contarChaves(jogador):
    """
    Objetivo: Contar quantas chaves o jogador possui no inventário.

    Requisitos funcionais:
        - Percorre o inventário do jogador.
        - Conta apenas itens reconhecidos como chave pelo módulo itens.

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador.
        Saída:
            total: número de chaves no inventário.
        Retornos:
            int: quantidade de chaves (0 em caso de erro).

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser um dicionário com nome válido.

        Assertivas de saída:
            - retorna inteiro >= 0.
            - retorna 0 se getInventario falhar.

    Hipóteses e restrições:
        - Verifica tipo de cada item via itens.getTipoItem.
    """
    codigo, inventario = getInventario(_nomeJogador(jogador))

    if codigo != 0:
        return 0

    total = 0

    for id_item in inventario:
        codigo_tipo, tipo = itens.getTipoItem(id_item)
        if codigo_tipo == 0 and tipo == "chave":
            total += 1

    return total


def _garantirPosicaoJogador(jogador, mapa):
    """
    Objetivo:
        Garantir que o jogador possui uma posição definida no mapa,
        atribuindo a posição inicial caso necessário.

    Requisitos funcionais:
        - Se jogador já tiver posição, não altera nada.
        - Se não tiver, obtém a posição inicial do mapa e a atribui.

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador.
            mapa: objeto do mapa atual.
        Saída:
            nenhuma saída direta; jogador pode ser modificado.
        Retornos:
            0: posição garantida com sucesso.
            1: falha ao obter posição inicial do mapa.
            2: parâmetros inválidos.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser um dicionário.
            - mapa não deve ser None.

        Assertivas de saída:
            - se retornar 0, jogador["posicao"] está definido.
            - se retornar 1 ou 2, jogador não foi modificado.

    Hipóteses e restrições:
        - Delega a obtenção da posição inicial ao módulo mapa (getPosicaoInicialMapa).
    """
    if not isinstance(jogador, dict) or mapa is None:
        return 2

    if "posicao" in jogador:
        return 0

    status, posicao = getPosicaoInicialMapa(mapa)

    if status == 0:
        jogador["posicao"] = posicao

    return status


def _prepararEntidades(mapa):
    """
    Objetivo: Inicializar e alocar todos os itens e inimigos no mapa para o início do jogo.

    Requisitos funcionais:
        - Restaurar o estado dos módulos itens e inimigos antes de criar novas entidades.
        - Criar todos os itens definidos em ITENS_INICIAIS e alocá-los no mapa.
        - Criar todos os inimigos definidos em INIMIGOS_INICIAIS e alocá-los no mapa.
        - Interromper e retornar erro se qualquer criação ou alocação falhar.

    Acoplamento:
        Entrada:
            mapa: objeto do mapa onde as entidades serão alocadas.
        Saída:
            nenhuma saída direta; mapa é modificado internamente.
        Retornos:
            0: todas as entidades foram criadas e alocadas com sucesso.
            1: erro ao criar ou alocar alguma entidade.

    Condições de acoplamento:
        Assertivas de entrada:
            - mapa deve ser um objeto válido já criado pelo módulo mapa.

        Assertivas de saída:
            - se retornar 0, todos os itens e inimigos estão alocados no mapa.
            - se retornar 1, o estado do mapa pode estar parcialmente inicializado.

    Hipóteses e restrições:
        - Depende dos módulos itens, inimigos e mapa.
        - As listas ITENS_INICIAIS e INIMIGOS_INICIAIS são constantes do módulo.
    """
    if itens.restaurarEstadoItens([]) != 0:
        return 1

    for posicao, nome, tipo, valor in ITENS_INICIAIS:
        status, id_item = itens.criarItem(nome, tipo, valor)

        if status != 0:
            return 1

        if alocarItemMapa(mapa, posicao[0], posicao[1], id_item) != 0:
            return 1

    if inimigos.restaurarEstadoInimigos([]) != 0:
        return 1

    for posicao, nome, vida, ataque, final in INIMIGOS_INICIAIS:
        status, id_inimigo = inimigos.criarInimigo(nome, vida, ataque)

        if status != 0:
            return 1

        if alocarInimigoMapa(mapa, posicao[0], posicao[1], id_inimigo, final) != 0:
            return 1

    return 0


def _resolverEventoAtual(jogador, mapa):
    """
    Objetivo:
        Verificar e resolver o evento presente na posição atual do jogador
        (item, inimigo comum ou chefe).

    Requisitos funcionais:
        - Se houver item na posição, tentar adicioná-lo ao inventário do jogador.
        - Se houver inimigo na posição, executar batalha.
        - Se o inimigo for o chefe e o jogador vencer, encerrar o jogo com vitória.
        - Conceder XP ao jogador após vitória em batalha.
        - Limpar o evento do mapa após resolução bem-sucedida.

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador.
            mapa: objeto do mapa atual.
        Saída:
            nenhuma saída direta; estado do jogador e mapa podem ser modificados.
        Retornos:
            0: evento resolvido com sucesso ou sem evento.
            1: erro interno ao resolver evento.
            2: erro de parâmetro inválido em submódulo.
            3: chefe derrotado, jogo encerrado com vitória.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser um dicionário com posição definida.
            - mapa deve ser um objeto válido.

        Assertivas de saída:
            - se retornar 0, o evento foi resolvido ou não havia evento.
            - se retornar 3, o chefe foi derrotado e o jogo deve encerrar.
            - se retornar 1 ou 2, o estado pode estar inconsistente.

    Hipóteses e restrições:
        - Depende dos módulos batalha, itens, inimigos e mapa.
        - XP concedido: 50 para inimigos comuns, 120 para o chefe.
    """
    nome = _nomeJogador(jogador)
    status, posicao = _posicaoJogador(jogador)

    if status != 0:
        return status

    x, y = posicao
    status_item, id_item = getItemMapa(mapa, x, y)

    if status_item == 0:
        status_adicionar = adicionarItemJogador(nome, id_item)

        if status_adicionar == 0:
            codigo_tipo, tipo_item = itens.getTipoItem(id_item)
            _, valor_item = itens.getValorItem(id_item)
            if codigo_tipo == 0 and tipo_item == "chave":
                chaves_atuais = _contarChaves(jogador)
                print(f"  Chave   : obtida ({chaves_atuais}/2).")
                if chaves_atuais >= 2:
                    print("  Portao  : desbloqueado! Voce pode entrar no castelo.")
            else:
                print(f"  Achado  : [{tipo_item}: +{valor_item}] adicionado ao inventario.")
            limparEventoMapa(mapa, x, y)
            return 0

        if status_adicionar == 1:
            print("  Achado  : ha um item aqui, mas o inventario esta cheio.")
            return 0

        return status_adicionar

    status_inimigo, id_inimigo = getInimigoMapa(mapa, x, y)

    if status_inimigo != 0:
        return 2 if status_item == 2 or status_inimigo == 2 else 0

    status_final, chefe = inimigoFinalMapa(mapa, x, y)

    if status_final != 0:
        return status_final

    if chefe:
        print("  Alerta  : voce encontrou o chefe da torre.")

    status_batalha, vencedor = batalha.executarBatalha(jogador, id_inimigo)

    if status_batalha != 0:
        return status_batalha

    if vencedor != "jogador":
        return 0

    xp = 120 if chefe else 50
    registrarInimigoDerrotadoMapa(mapa, x, y)
    ganharXP(nome, xp)
    atualizarAtaque(nome)
    print(f"  XP      : voce ganhou {xp} pontos de experiencia.")

    if chefe:
        print("  Objetivo: chefe derrotado.")
        print("\nFim de jogo: voce atravessou o bosque e venceu o chefe do castelo!")
        return 3

    return 0


def iniciarJogo(nome):
    """
    Objetivo:
        Inicializar todos os componentes do jogo: jogador, mapa e entidades.

    Requisitos funcionais:
        - Criar o jogador com o nome fornecido.
        - Criar o mapa e preparar todas as entidades iniciais.
        - Definir a posição inicial do jogador no mapa.
        - Retornar jogador e mapa prontos para uso.

    Acoplamento:
        Entrada:
            nome: nome do jogador.
        Saída:
            jogador: dicionário com os dados do jogador inicializado.
            mapa: objeto do mapa com entidades alocadas.
        Retornos:
            (0, jogador, mapa): jogo inicializado com sucesso.
            (1, None, None): erro na inicialização.
            (2, None, None): parâmetro inválido (nome None).

    Condições de acoplamento:
        Assertivas de entrada:
            - nome deve ser uma string não vazia.

        Assertivas de saída:
            - se retornar (0, jogador, mapa), ambos estão prontos para uso.
            - se retornar (1, None, None) ou (2, None, None), nada foi inicializado.

    Hipóteses e restrições:
        - Depende dos módulos jogador, mapa, itens e inimigos.
    """
    if nome is None:
        return 2, None, None

    status, jogador = criarJogador(nome)

    if status != 0 or jogador is None:
        return 1, None, None

    status, mapa = criarMapa()

    if status != 0 or _prepararEntidades(mapa) != 0:
        return 1, None, None

    status, posicao = getPosicaoInicialMapa(mapa)

    if status != 0:
        return 1, None, None

    jogador["posicao"] = posicao
    return 0, jogador, mapa


def exibirStatus(jogador, mapa):
    """
    Objetivo:
        Exibir no console o status atual do jogador formatado com barra de vida.

    Requisitos funcionais:
        - Exibir nome, vida, ataque, XP, chaves e posição do jogador.
        - Representar a vida com barra visual proporcional.
        - Garantir que o jogador possui posição antes de exibir.

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador.
            mapa: objeto do mapa atual.
        Saída:
            nenhuma saída direta; imprime no console.
        Retornos:
            0: status exibido com sucesso.
            1: erro ao obter dados do jogador.
            2: parâmetros inválidos.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser um dicionário válido.
            - mapa não deve ser None.

        Assertivas de saída:
            - se retornar 0, o status foi impresso no console.
            - se retornar 1 ou 2, nada foi impresso.

    Hipóteses e restrições:
        - A vida máxima é obtida de jogador["vida_max"] com padrão 100.
    """
    if jogador is None or mapa is None:
        return 1

    status = _garantirPosicaoJogador(jogador, mapa)

    if status != 0:
        return status

    nome = _nomeJogador(jogador)
    _, vida = getVida(nome)
    _, ataque = getAtaque(nome)
    _, xp = getXP(nome)
    _, posicao = _posicaoJogador(jogador)
    chaves = _contarChaves(jogador)
    vida_maxima = jogador.get("vida_max", 100)
    barras = int((vida / vida_maxima) * 10)
    barra_vida = "█" * barras + "░" * (10 - barras)

    print("=" * 30)
    print(f"  Jogador : {nome}")
    print(f"  Vida    : [{barra_vida}] {vida}/{vida_maxima}")
    print(f"  Ataque  : {ataque}")
    print(f"  XP      : {xp}")
    print(f"  Chaves  : {chaves}/2")
    print(f"  Posição : {posicao}")
    print("=" * 30)
    return 0


def _normalizarComando(comando):
    """
    Objetivo:
        Normalizar a entrada do jogador, traduzindo atalhos para comandos reconhecidos.

    Requisitos funcionais:
        - Remover espaços e converter para minúsculas.
        - Traduzir atalhos definidos em ATALHOS (ex: "w" -> "cima").
        - Retornar None se a entrada não for string.

    Acoplamento:
        Entrada:
            comando: string digitada pelo jogador.
        Saída:
            comando_normalizado: comando traduzido ou original.
        Retornos:
            str: comando normalizado ou traduzido.
            None: se comando não for string.

    Condições de acoplamento:
        Assertivas de entrada:
            - comando deve ser string.

        Assertivas de saída:
            - se retornar str, é um comando válido ou vazio.
            - se retornar None, o tipo de entrada era inválido.

    Hipóteses e restrições:
        - A tabela de atalhos é definida pela constante ATALHOS do módulo.
    """
    if not isinstance(comando, str):
        return None

    comando = comando.strip().lower()
    return ATALHOS.get(comando, comando)


def _exibirMapa(jogador, mapa):
    """
    Objetivo:
        Renderizar e exibir o mapa no console com a posição atual do jogador.

    Requisitos funcionais:
        - Obter a posição atual do jogador.
        - Delegar a renderização ao módulo mapa.
        - Imprimir o desenho resultante no console.

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador.
            mapa: objeto do mapa atual.
        Saída:
            nenhuma saída direta; imprime no console.
        Retornos:
            0: mapa exibido com sucesso.
            1: erro ao renderizar o mapa.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ter posição definida.
            - mapa deve ser um objeto válido.

        Assertivas de saída:
            - se retornar 0, o mapa foi impresso no console.
            - se retornar 1, nada foi impresso.

    Hipóteses e restrições:
        - Delega a renderização ao módulo mapa (renderizarMapa).
    """
    _, posicao = _posicaoJogador(jogador)
    status, desenho = renderizarMapa(mapa, posicao)

    if status == 0:
        print(desenho)

    return status


def _exibirInventario(jogador):
    """
    Objetivo:
        Exibir no console o inventário completo e os atributos atuais do jogador.

    Requisitos funcionais:
        - Listar todos os itens do inventário por nome.
        - Exibir vida, ataque, XP, chaves e posição do jogador.
        - Exibir "vazio" se o inventário estiver sem itens.

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador.
        Saída:
            nenhuma saída direta; imprime no console.
        Retornos:
            0: inventário exibido com sucesso.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser um dicionário com nome válido.

        Assertivas de saída:
            - sempre retorna 0.
            - o inventário é impresso no console independente de estar vazio.

    Hipóteses e restrições:
        - Itens do inventário são IDs inteiros; tipo e valor obtidos via itens.getTipoItem/getValorItem.
    """
    nome = _nomeJogador(jogador)
    _, vida = getVida(nome)
    _, ataque = getAtaque(nome)
    _, xp = getXP(nome)
    _, posicao = _posicaoJogador(jogador)
    _, inventario = getInventario(nome)
    chaves = _contarChaves(jogador)
    nomes = []

    for id_item in inventario:
        _, tipo = itens.getTipoItem(id_item)
        _, valor = itens.getValorItem(id_item)
        nomes.append(f"[{tipo}: +{valor}]")

    texto_inventario = ", ".join(nomes) if nomes else "vazio"

    print("=" * 30)
    print(f"  Jogador : {nome}")
    print(f"  Vida    : {vida}/{jogador.get('vida_max', 100)}")
    print(f"  Ataque  : {ataque}")
    print(f"  XP      : {xp}")
    print(f"  Chaves  : {chaves}/2")
    print(f"  Posição : {posicao}")
    print(f"  Inventário: {texto_inventario}")
    print("=" * 30)
    return 0


def _usarItemMapa(jogador):
    """
    Objetivo:
        Permitir ao jogador selecionar e usar um item utilizável do inventário.

    Requisitos funcionais:
        - Listar apenas itens dos tipos "cura" e "ataque".
        - Exibir opção de cancelamento.
        - Validar a escolha do jogador antes de usar o item.
        - Delegar o uso do item ao módulo jogador.

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador.
        Saída:
            nenhuma saída direta; estado do jogador pode ser modificado.
        Retornos:
            0: item usado com sucesso, cancelado pelo jogador, ou sem itens utilizáveis.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser um dicionário com nome e inventário válidos.

        Assertivas de saída:
            - sempre retorna 0.
            - se item usado, estado do jogador é atualizado pelo módulo jogador.

    Hipóteses e restrições:
        - Apenas itens dos tipos "cura" e "ataque" são utilizáveis fora de batalha.
        - Delega o uso ao módulo jogador (usarItemJogador).
        - Tipo e valor obtidos via itens.getTipoItem/getValorItem.
    """
    nome = _nomeJogador(jogador)
    _, inventario = getInventario(nome)

    usaveis = []
    for id_item in inventario:
        codigo_tipo, tipo = itens.getTipoItem(id_item)
        if codigo_tipo == 0 and tipo in ["cura", "ataque"]:
            usaveis.append(id_item)

    if not usaveis:
        print("  Nenhum item utilizável no inventário.")
        return 0

    for i, id_item in enumerate(usaveis):
        _, tipo = itens.getTipoItem(id_item)
        _, valor = itens.getValorItem(id_item)
        print(f"  {i + 1} - [{tipo}: +{valor}]")
    print("  0 - Cancelar")

    try:
        escolha = input("  Usar item: ").strip()
    except (EOFError, KeyboardInterrupt):
        return 0

    if not escolha.isdigit() or int(escolha) == 0:
        return 0

    num = int(escolha)
    if num < 1 or num > len(usaveis):
        print("  Opção inválida.")
        return 0

    id_item = usaveis[num - 1]
    codigo = usarItemJogador(nome, id_item)

    if codigo == 0:
        _, tipo = itens.getTipoItem(id_item)
        print(f"  Item de {tipo} utilizado.")
    else:
        print("  Não foi possível usar o item.")

    return 0


def processarComando(jogador, mapa, comando):
    """
    Objetivo:
        Processar um comando do jogador e executar a ação correspondente no jogo.

    Requisitos funcionais:
        - Normalizar o comando recebido.
        - Executar movimento se o comando for uma direção válida.
        - Exibir inventário e permitir uso de item se o comando for "inventario".
        - Exibir o mapa se o comando for "mapa".
        - Resolver o evento da posição após cada movimento.

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador.
            mapa: objeto do mapa atual.
            comando: string com o comando normalizado ou bruto.
        Saída:
            nenhuma saída direta; estado do jogador e mapa podem ser modificados.
        Retornos:
            0: comando executado com sucesso.
            1: comando inválido ou não reconhecido.
            2: parâmetro inválido.
            3: chefe derrotado, jogo encerrado com vitória.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser um dicionário válido.
            - mapa deve ser um objeto válido.
            - comando deve ser string.

        Assertivas de saída:
            - se retornar 0, a ação foi executada com sucesso.
            - se retornar 3, o jogo deve ser encerrado.
            - se retornar 1, nenhuma ação foi executada.
            - se retornar 2, os parâmetros eram inválidos.

    Hipóteses e restrições:
        - Depende de DIRECOES e ATALHOS definidos no módulo.
        - Delega movimento ao módulo mapa e eventos a _resolverEventoAtual.
    """
    if jogador is None or mapa is None or comando is None:
        return 2

    comando = _normalizarComando(comando)

    if comando is None:
        return 2

    if not comando:
        return 1

    status = _garantirPosicaoJogador(jogador, mapa)

    if status != 0:
        return status

    if comando in DIRECOES:
        status_movimento = moverJogadorMapa(mapa, jogador, comando, _contarChaves(jogador) >= 2)

        if status_movimento == 3:
            print(f"  Portão trancado. Você tem {_contarChaves(jogador)}/2 chaves.")
            return _exibirMapa(jogador, mapa)

        if status_movimento != 0:
            print("Movimento inválido. Tente outra direção.")
            return _exibirMapa(jogador, mapa)

        _, posicao = _posicaoJogador(jogador)
        print(f"  Posição : {posicao}")

        status_descricao, descricao = descreverPosicaoMapa(mapa, posicao[0], posicao[1])

        if status_descricao == 0:
            print(f"  Local   : {descricao}")

        status_evento = _resolverEventoAtual(jogador, mapa)

        if status_evento != 0:
            return status_evento

        return _exibirMapa(jogador, mapa)

    if comando == "inventario":
        _exibirInventario(jogador)
        return _usarItemMapa(jogador)

    if comando == "mapa":
        return _exibirMapa(jogador, mapa)

    if comando == "salvar e sair":
        return 4   # sinal para loopJogo chamar o save

    return 1


def loopJogo(jogador, mapa):
    """
    Objetivo:
        Executar o loop principal do jogo, processando comandos até o encerramento.

    Requisitos funcionais:
        - Exibir status inicial e objetivo do jogo.
        - Repetir a leitura e processamento de comandos até encerramento.
        - Encerrar se o jogador morrer, vencer ou solicitar saída.
        - Tratar interrupções de entrada (EOFError, KeyboardInterrupt).

    Acoplamento:
        Entrada:
            jogador: dicionário do jogador inicializado.
            mapa: objeto do mapa com entidades alocadas.
        Saída:
            nenhuma saída direta; estado do jogo evolui a cada iteração.
        Retornos:
            0: jogo encerrado normalmente (vitória, derrota ou saída).
            1: erro interno durante o loop.
            2: parâmetros inválidos.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador deve ser um dicionário válido com posição definida.
            - mapa deve ser um objeto válido com entidades alocadas.

        Assertivas de saída:
            - se retornar 0, o jogo foi encerrado de forma esperada.
            - se retornar 1, ocorreu erro interno durante o processamento.
            - se retornar 2, os parâmetros eram inválidos.

    Hipóteses e restrições:
        - Depende de processarComando e exibirStatus.
        - COMANDOS_SAIDA define as entradas que encerram o jogo.
    """
    if jogador is None or mapa is None:
        return 2

    if _garantirPosicaoJogador(jogador, mapa) != 0:
        return 2

    exibirStatus(jogador, mapa)
    print("Objetivo : pegue 2 chaves, entre no castelo e derrote o chefe.")

    nome = _nomeJogador(jogador)

    if getVida(nome)[1] > 0:
        _exibirMapa(jogador, mapa)

    while True:
        _, vida = getVida(nome)

        if vida <= 0:
            print("\nVocê morreu. Fim de jogo.")
            return 0

        print("\n" + "-" * 46)
        print("Movimento: W-Cima | S-Baixo | A-Esquerda | D-Direita")
        print("Ações    : 1-Inventário | 2-Mapa | 5-Salvar e sair")

        try:
            comando = input("\n> Escolha: ")
        except (EOFError, KeyboardInterrupt):
            print("\nJogo interrompido.")
            return 0

        comando_normalizado = _normalizarComando(comando)

        if not comando_normalizado:
            print("Escolha uma opção.")
            continue

        if comando_normalizado in COMANDOS_SAIDA:
            resultado = salvar.salvarJogo(jogador, mapa)
            print("Jogo salvo com sucesso!")
            print("Encerrando o jogo...")
            return 0

        status = processarComando(jogador, mapa, comando_normalizado)

        if status == 1:
            print(f"Comando '{comando}' inválido. Tente outro.")
        elif status == 2:
            print("Erro interno ao processar comando.")
            return 1
        elif status == 3:
            return 0
        elif status == 4:
            salvar.salvarJogo(jogador, mapa)
            print("Jogo salvo com sucesso!")
            return 0


if __name__ == "__main__":
    import salvar

    print("=== ConsoleRPG ===")

    if salvar.existeSalvamento():
        print("\n1 - Novo jogo")
        print("2 - Continuar jogo salvo")
        escolha = input("\n> Escolha: ").strip()

        if escolha == "2":
            status, jogador, mapa = salvar.carregarJogo(_prepararEntidades)
            if status != 0:
                print("Erro ao carregar save. Iniciando novo jogo...")
                escolha = "1"
            else:
                print(f"\nBem-vindo de volta, {jogador.get('nome')}!")

        if escolha != "2":
            nome = input("Digite seu nome: ")
            status, jogador, mapa = iniciarJogo(nome)
    else:
        nome = input("Digite seu nome: ")
        status, jogador, mapa = iniciarJogo(nome)

    if status != 0:
        print("Erro ao iniciar jogo!")
    else:
        loopJogo(jogador, mapa)