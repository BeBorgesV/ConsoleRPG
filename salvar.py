import json
import os

import jogador as modulo_jogador
from mapa import criarMapa

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
        Persistir o estado atual do jogo em arquivo JSON, incluindo nome, posição,
        inventário, vida, XP, ataque do jogador e eventos restantes do mapa.

    Requisitos funcionais:
        - Exportar os dados do jogador via funções de acesso do módulo jogador.
        - Salvar a posição atual do jogador no mapa.
        - Salvar o estado dos eventos do mapa (quais posições ainda têm item ou inimigo).
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
        - Depende apenas do módulo jogador para leitura dos atributos.
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

    codigo_vida, vida = modulo_jogador.getVida(nome)
    codigo_ataque, ataque = modulo_jogador.getAtaque(nome)
    codigo_xp, xp = modulo_jogador.getXP(nome)
    codigo_inv, inventario = modulo_jogador.getInventario(nome)

    if any(c != 0 for c in [codigo_vida, codigo_ataque, codigo_xp, codigo_inv]):
        return 1

    def converter_chaves(dicionario):
        return {str(k): v for k, v in dicionario.items()}

    save = {
        "jogador": {
            "nome": nome,
            "vida": vida,
            "vida_max": jogador_atual.get("vida_max", 100),
            "ataque": ataque,
            "xp": xp,
            "posicao": list(posicao),
            "inventario": inventario
        },
        "mapa_eventos": converter_chaves(mapa.get("eventos", {}))
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
        Carregar o estado do jogo a partir do arquivo de salvamento, recriando
        o mapa com todas as entidades e removendo os eventos já resolvidos.

    Requisitos funcionais:
        - Ler e validar o arquivo de save JSON.
        - Recriar o jogador no módulo jogador com os dados salvos.
        - Recriar o mapa completo via prepararEntidades (itens e inimigos iniciais).
        - Remover do mapa os eventos que já haviam sido resolvidos no save.
        - Retornar o dicionário do jogador e o mapa prontos para uso.

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

    if dados_jogador is None or eventos_salvos is None:
        return 2, None, None

    # Recria jogador
    nome = dados_jogador.get("nome")
    if not nome:
        return 2, None, None

    resultado = modulo_jogador.criarJogador(nome)
    if not isinstance(resultado, dict):
        return 1, None, None

    jogador_atual = resultado
    jogador_interno = modulo_jogador._jogadores.get(nome)
    if jogador_interno is None:
        return 1, None, None

    jogador_interno["vida"]      = dados_jogador.get("vida", 100)
    jogador_interno["xp"]        = dados_jogador.get("xp", 0)
    jogador_interno["ataque"]    = dados_jogador.get("ataque", 10)
    jogador_interno["vida_max"]  = dados_jogador.get("vida_max", 100)
    jogador_interno["inventario"] = dados_jogador.get("inventario", [])

    jogador_atual["vida"]     = jogador_interno["vida"]
    jogador_atual["xp"]       = jogador_interno["xp"]
    jogador_atual["ataque"]   = jogador_interno["ataque"]
    jogador_atual["vida_max"] = jogador_interno["vida_max"]

    posicao_lista = dados_jogador.get("posicao")
    if not isinstance(posicao_lista, list) or len(posicao_lista) != 2:
        return 2, None, None

    jogador_atual["posicao"] = tuple(posicao_lista)

    # Recria mapa com todas as entidades iniciais
    status_mapa, mapa = criarMapa()
    if status_mapa != 0:
        return 1, None, None

    if prepararEntidades(mapa) != 0:
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