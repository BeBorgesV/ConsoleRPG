import json
import os

import jogador as modulo_jogador
from inimigos import exportarEstadoInimigos, restaurarEstadoInimigos
from itens import exportarEstadoItens, restaurarEstadoItens
from mapa import criarMapa, exportarEstadoMapa

__all__ = [
    "salvarJogo",
    "carregarJogo",
    "existeSalvamento"
]

_ARQUIVO_SAVE = "save.json"


def existeSalvamento():
    """
    Objetivo:
        Verificar se existe um arquivo de salvamento disponível para carregamento.

    Requisitos funcionais:
        - Verificar a existência do arquivo de save no diretório atual.

    Acoplamento:
        Entrada:
            nenhuma.
        Saída:
            existe: booleano indicando se o arquivo de save existe.
        Retornos:
            True: arquivo de save encontrado.
            False: arquivo de save não encontrado.

    Condições de acoplamento:
        Assertivas de entrada:
            - nenhuma.

        Assertivas de saída:
            - retorna True apenas se o arquivo existir e puder ser lido.
            - não lança exceções.

    Hipóteses e restrições:
        - O arquivo de save é sempre salvo com o nome definido em _ARQUIVO_SAVE.
    """
    return os.path.isfile(_ARQUIVO_SAVE)


def salvarJogo(jogador_atual, mapa):
    """
    Objetivo:
        Persistir o estado atual do jogo em arquivo JSON, incluindo o estado do
        jogador, eventos restantes do mapa, lista de inimigos e lista de itens.

    Requisitos funcionais:
        - Exportar os dados do jogador via função exportarJogador do módulo jogador.
        - Salvar a posição atual do jogador.
        - Salvar o estado dos eventos do mapa.
        - Exportar e salvar o estado atual dos inimigos.
        - Exportar e salvar o estado atual dos itens.
        - Gravar tudo em um arquivo JSON no diretório atual.

    Acoplamento:
        Entrada:
            jogador_atual: dicionário do jogador com ao menos "nome" e "posicao".
            mapa: objeto do mapa com eventos alocados.
        Saída:
            arquivo save.json gravado no diretório atual.
        Retornos:
            0: jogo salvo com sucesso.
            1: erro ao acessar dados do jogador ou ao gravar o arquivo.
            2: parâmetros inválidos.

    Condições de acoplamento:
        Assertivas de entrada:
            - jogador_atual deve ser um dicionário com "nome" e "posicao" (tupla).
            - mapa deve ser um dicionário válido com "eventos".

        Assertivas de saída:
            - se retornar 0, o arquivo save.json foi gravado com sucesso.
            - se retornar 1 ou 2, nenhum arquivo foi gravado.

    Hipóteses e restrições:
        - Depende das funções de exportação dos módulos jogador, inimigos e itens.
        - Ao carregar, o mapa é recriado via _prepararEntidades e os eventos
          já resolvidos são removidos conforme o estado salvo.
        - Chaves de tupla do mapa são convertidas para string no JSON.
    """
    if not isinstance(jogador_atual, dict) or mapa is None:
        return 2

    nome = jogador_atual.get("nome")
    posicao = jogador_atual.get("posicao")

    if not nome or not isinstance(posicao, tuple):
        return 2

    resultado_jogador = modulo_jogador.exportarJogador(nome)
    if not isinstance(resultado_jogador, tuple) or len(resultado_jogador) != 2:
        return 1

    codigo_jogador, dados_jogador = resultado_jogador
    if codigo_jogador != 0 or not isinstance(dados_jogador, dict):
        return 1

    dados_jogador["posicao"] = list(posicao)

    def converter_chaves(dicionario):
        return {str(k): v for k, v in dicionario.items()}

    status_mapa, estado_mapa = exportarEstadoMapa(mapa)
    eventos_mapa = estado_mapa["eventos"] if status_mapa == 0 else {}

    save = {
        "jogador": dados_jogador,
        "mapa_eventos": converter_chaves(eventos_mapa),
        "inimigos": exportarEstadoInimigos(),
        "itens": exportarEstadoItens()
    }

    try:
        with open(_ARQUIVO_SAVE, "w", encoding="utf-8") as arquivo:
            json.dump(save, arquivo, ensure_ascii=False, indent=2)
        return 0
    except (OSError, TypeError):
        return 1


def carregarJogo(prepararEntidades):
    """
    Objetivo:
        Carregar o estado do jogo a partir do arquivo de salvamento, restaurando
        jogador, mapa, inimigos e itens.

    Requisitos funcionais:
        - Ler e validar o arquivo de save JSON.
        - Restaurar o jogador no módulo jogador por meio da função restaurarJogador.
        - Recriar o mapa completo via prepararEntidades.
        - Restaurar a lista de inimigos a partir do estado salvo.
        - Restaurar a lista de itens a partir do estado salvo.
        - Remover do mapa os eventos que já haviam sido resolvidos no save.

    Acoplamento:
        Entrada:
            prepararEntidades: função da main que recria itens e inimigos no mapa.
        Saída:
            jogador_atual: dicionário do jogador restaurado com posição.
            mapa: objeto do mapa com estado restaurado.
        Retornos:
            (0, jogador_atual, mapa): jogo carregado com sucesso.
            (1, None, None): erro ao restaurar dados.
            (2, None, None): arquivo de save não encontrado ou corrompido.

    Condições de acoplamento:
        Assertivas de entrada:
            - o arquivo save.json deve existir e estar no formato correto.
            - prepararEntidades deve ser uma função que recebe um mapa e retorna 0 em sucesso.

        Assertivas de saída:
            - se retornar (0, jogador, mapa), ambos estão prontos para uso imediato.
            - se retornar (1, None, None) ou (2, None, None), nada foi restaurado.

    Hipóteses e restrições:
        - O mapa é sempre recriado do zero via criarMapa + prepararEntidades.
        - Jogador, inimigos e itens são restaurados apenas por funções de interface dos seus módulos.
        - Os eventos já resolvidos são identificados pela comparação entre o estado
          salvo e o estado inicial, e removidos com limparEventoMapa.
        - Chaves de posição são convertidas de string para tupla ao carregar.
    """
    if not existeSalvamento():
        return 2, None, None

    try:
        with open(_ARQUIVO_SAVE, "r", encoding="utf-8") as arquivo:
            save = json.load(arquivo)
    except (OSError, json.JSONDecodeError):
        return 2, None, None

    if not isinstance(save, dict):
        return 2, None, None

    dados_jogador = save.get("jogador")
    eventos_salvos = save.get("mapa_eventos")
    inimigos_salvos = save.get("inimigos")
    itens_salvos = save.get("itens")

    if dados_jogador is None or eventos_salvos is None:
        return 2, None, None

    if inimigos_salvos is None or itens_salvos is None:
        return 2, None, None

    if not isinstance(dados_jogador, dict):
        return 2, None, None

    posicao_lista = dados_jogador.get("posicao")
    if not isinstance(posicao_lista, list) or len(posicao_lista) != 2:
        return 2, None, None

    status_jogador = modulo_jogador.restaurarJogador(dados_jogador)
    if status_jogador == 2:
        return 2, None, None

    if status_jogador != 0:
        return 1, None, None

    jogador_atual = dados_jogador.copy()
    jogador_atual["posicao"] = tuple(posicao_lista)

    if restaurarEstadoInimigos([]) != 0:
        return 1, None, None

    if restaurarEstadoItens([]) != 0:
        return 1, None, None

    # Recria mapa com todas as entidades iniciais
    status_mapa, mapa = criarMapa()
    if status_mapa != 0:
        return 1, None, None

    if prepararEntidades(mapa) != 0:
        return 1, None, None

    if restaurarEstadoInimigos(inimigos_salvos) != 0:
        return 1, None, None

    if restaurarEstadoItens(itens_salvos) != 0:
        return 1, None, None

    # Remove do mapa os eventos já resolvidos (que estavam como "vazio" no save)
    from mapa import limparEventoMapa
    for chave_str, evento_salvo in eventos_salvos.items():
        partes = chave_str.strip("()").split(", ")
        if len(partes) != 2:
            continue
        x, y = int(partes[0]), int(partes[1])
        if evento_salvo == "vazio":
            limparEventoMapa(mapa, x, y)

    return 0, jogador_atual, mapa