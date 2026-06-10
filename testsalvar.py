import json
import os
import sys

import inimigos
import itens
import jogador as modulo_jogador
import salvar
from mapa import criarMapa, alocarItemMapa, alocarInimigoMapa

_total = 0
_passou = 0


def _resultado(id_ct, descricao, passou):
    global _total, _passou
    _total += 1
    if passou:
        _passou += 1
        print(f"  [OK] {id_ct}: {descricao}")
    else:
        print(f"  [FALHOU] {id_ct}: {descricao}")


def _limparSave():
    if os.path.isfile("save.json"):
        os.remove("save.json")


def _prepararJogador(nome="Heroi", vida=80, xp=150, ataque=11):
    """Cria/restaura jogador no módulo usando apenas a interface pública."""
    jogador = {
        "nome": nome,
        "vida": vida,
        "vida_max": 100,
        "xp": xp,
        "ataque": ataque,
        "vivo": vida > 0,
        "inventario": [],
        "posicao": (1, 13)
    }

    if modulo_jogador.restaurarJogador(jogador) != 0:
        return None

    return jogador


def _prepararMapa():
    """Cria mapa padrão e aloca um item e um inimigo para os testes."""
    itens.restaurarEstadoItens([])
    inimigos.restaurarEstadoInimigos([])
    _, id_item = itens.criarItem("Pocao simples", "cura", 25)
    _, id_inimigo = inimigos.criarInimigo("Lobo", 35, 7)
    _, mapa = criarMapa()
    alocarItemMapa(mapa, 2, 12, id_item)
    alocarInimigoMapa(mapa, 5, 11, id_inimigo, False)
    return mapa, id_item, id_inimigo


def _prepararItemNoInventario(jogador, nome="Amuleto", tipo="ataque", valor=5):
    """Cria um item no módulo Item e adiciona seu id ao inventário do jogador."""
    codigo, id_item = itens.criarItem(nome, tipo, valor)
    if codigo != 0:
        return None

    nome_jogador = jogador.get("nome")
    resultado = modulo_jogador.exportarJogador(nome_jogador)
    if not isinstance(resultado, tuple) or len(resultado) != 2:
        return None

    codigo_jogador, dados_jogador = resultado
    if codigo_jogador != 0:
        return None

    dados_jogador["inventario"].append(id_item)

    if modulo_jogador.restaurarJogador(dados_jogador) != 0:
        return None

    jogador["inventario"] = dados_jogador["inventario"]
    return id_item

def _prepararEntidadesTeste(mapa):
    """Recria entidades iniciais esperadas pelo módulo salvar durante o carregamento."""
    _, id_item = itens.criarItem("Pocao simples", "cura", 25)
    _, id_inimigo = inimigos.criarInimigo("Lobo", 35, 7)
    alocarItemMapa(mapa, 2, 12, id_item)
    alocarInimigoMapa(mapa, 5, 11, id_inimigo, False)
    return 0

def testar_existeSalvamento():
    print("\n[ existeSalvamento ]")

    # CT-S01: sem arquivo de save
    _limparSave()
    _resultado("CT-S01", "retorna False quando save.json não existe", salvar.existeSalvamento() == False)

    # CT-S02: com arquivo de save presente
    with open("save.json", "w") as f:
        f.write("{}")
    _resultado("CT-S02", "retorna True quando save.json existe", salvar.existeSalvamento() == True)
    _limparSave()

def testar_salvarJogo():
    print("\n[ salvarJogo ]")
    _limparSave()

    # CT-S03: jogador None
    _, mapa = criarMapa()
    _resultado("CT-S03", "retorna 2 quando jogador é None", salvar.salvarJogo(None, mapa) == 2)

    # CT-S04: mapa None
    jogador = _prepararJogador("Teste04")
    jogador["posicao"] = (1, 13)
    _resultado("CT-S04", "retorna 2 quando mapa é None", salvar.salvarJogo(jogador, None) == 2)

    # CT-S05: jogador sem nome
    jogador_sem_nome = {"posicao": (1, 13)}
    _, mapa = criarMapa()
    _resultado("CT-S05", "retorna 2 quando jogador não tem nome", salvar.salvarJogo(jogador_sem_nome, mapa) == 2)

    # CT-S06: jogador sem posicao
    jogador_sem_pos = {"nome": "Alguem"}
    _resultado("CT-S06", "retorna 2 quando jogador não tem posicao", salvar.salvarJogo(jogador_sem_pos, mapa) == 2)

    # CT-S07: jogador com posicao que não é tupla
    jogador_pos_invalida = {"nome": "Alguem", "posicao": [1, 13]}
    _resultado("CT-S07", "retorna 2 quando posicao não é tupla", salvar.salvarJogo(jogador_pos_invalida, mapa) == 2)

    # CT-S08: jogador não cadastrado no módulo jogador
    jogador_nao_cadastrado = {"nome": "Fantasma", "posicao": (1, 13)}
    _resultado("CT-S08", "retorna 1 quando jogador não está no módulo", salvar.salvarJogo(jogador_nao_cadastrado, mapa) == 1)

    # CT-S09: salvar com sucesso — sem itens no inventário
    mapa, _, _ = _prepararMapa()
    jogador = _prepararJogador("Heroi09")
    jogador["posicao"] = (3, 11)
    codigo = salvar.salvarJogo(jogador, mapa)
    _resultado("CT-S09", "retorna 0 com jogador e mapa válidos", codigo == 0)
    _resultado("CT-S10", "arquivo save.json é criado após salvar", os.path.isfile("save.json"))

    # CT-S11: conteúdo do save tem estrutura esperada
    with open("save.json", "r", encoding="utf-8") as f:
        conteudo = json.load(f)
    chaves_esperadas = {"jogador", "itens", "inimigos", "mapa_eventos"}
    _resultado("CT-S11", "save.json contém as chaves esperadas", chaves_esperadas.issubset(conteudo.keys()))

    # CT-S12: posição salva corretamente
    _resultado("CT-S12", "posição do jogador salva corretamente", conteudo["jogador"]["posicao"] == [3, 11])

    # CT-S13: vida salva corretamente
    _resultado("CT-S13", "vida do jogador salva corretamente", conteudo["jogador"]["vida"] == 80)

    # CT-S14: xp salvo corretamente
    _resultado("CT-S14", "xp do jogador salvo corretamente", conteudo["jogador"]["xp"] == 150)

    # CT-S15: ataque salvo corretamente
    _resultado("CT-S15", "ataque do jogador salvo corretamente", conteudo["jogador"]["ataque"] == 11)

    # CT-S16: salvar com item no inventário
    _limparSave()
    mapa, _, _ = _prepararMapa()
    jogador = _prepararJogador("Heroi16")
    jogador["posicao"] = (1, 13)
    _prepararItemNoInventario(jogador, "Pocao", "cura", 25)
    codigo = salvar.salvarJogo(jogador, mapa)
    _resultado("CT-S16", "retorna 0 com item no inventário", codigo == 0)

    with open("save.json", "r", encoding="utf-8") as f:
        conteudo = json.load(f)
    inventario_salvo = conteudo["jogador"]["inventario"]
    _resultado("CT-S17", "inventário salvo com 1 item", len(inventario_salvo) == 1)
    _resultado("CT-S18", "inventário salvo contém id de item", isinstance(inventario_salvo[0], int))

    # CT-S19: estado dos itens do módulo salvo
    _resultado("CT-S19", "itens salvos com itens alocados", len(conteudo["itens"]) > 0)

    # CT-S20: estado dos inimigos do módulo salvo
    _resultado("CT-S20", "inimigos salvos com inimigos alocados", len(conteudo["inimigos"]) > 0)

    # CT-S21: eventos do mapa salvos
    _resultado("CT-S21", "mapa_eventos não está vazio após salvar com entidades", len(conteudo["mapa_eventos"]) > 0)

    _limparSave()

def testar_carregarJogo():
    print("\n[ carregarJogo ]")
    _limparSave()

    # CT-S22: sem arquivo de save
    codigo, j, m = salvar.carregarJogo(_prepararEntidadesTeste)
    _resultado("CT-S22", "retorna (2, None, None) sem save.json", (codigo, j, m) == (2, None, None))

    # CT-S23: arquivo corrompido (JSON inválido)
    with open("save.json", "w") as f:
        f.write("isso nao e json valido {{{")
    codigo, j, m = salvar.carregarJogo(_prepararEntidadesTeste)
    _resultado("CT-S23", "retorna (2, None, None) com JSON inválido", (codigo, j, m) == (2, None, None))
    _limparSave()

    # CT-S24: arquivo com estrutura incompleta (faltando chave)
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump({"jogador": {"nome": "X"}}, f)
    codigo, j, m = salvar.carregarJogo(_prepararEntidadesTeste)
    _resultado("CT-S24", "retorna (2, None, None) com estrutura incompleta", (codigo, j, m) == (2, None, None))
    _limparSave()

    # CT-S25: arquivo com itens_modulo inválido
    save_invalido = {
        "jogador": {
            "nome": "X",
            "vida": 100,
            "vida_max": 100,
            "ataque": 10,
            "xp": 0,
            "vivo": True,
            "posicao": [1, 13],
            "inventario": []
        },
        "itens": "nao e lista",
        "inimigos": [],
        "mapa_eventos": {}
    }
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(save_invalido, f)
    codigo, j, m = salvar.carregarJogo(_prepararEntidadesTeste)
    _resultado("CT-S25", "retorna erro com itens inválido", codigo != 0 and j is None)
    _limparSave()

    # ── Ciclo completo: salvar e carregar ──

    mapa_original, id_item, id_inimigo = _prepararMapa()
    jogador_original = _prepararJogador("Guerreiro")
    jogador_original["posicao"] = (7, 9)
    _prepararItemNoInventario(jogador_original, "Amuleto de ataque", "ataque", 5)

    salvar.salvarJogo(jogador_original, mapa_original)

    # CT-S26: carregamento bem-sucedido
    codigo, jogador_carregado, mapa_carregado = salvar.carregarJogo(_prepararEntidadesTeste)
    _resultado("CT-S26", "retorna 0 após save válido", codigo == 0)
    _resultado("CT-S27", "jogador retornado não é None", jogador_carregado is not None)
    _resultado("CT-S28", "mapa retornado não é None", mapa_carregado is not None)

    # CT-S29: nome do jogador restaurado
    _resultado("CT-S29", "nome do jogador restaurado corretamente",
               jogador_carregado.get("nome") == "Guerreiro")

    # CT-S30: posição do jogador restaurada
    _resultado("CT-S30", "posição do jogador restaurada corretamente",
               jogador_carregado.get("posicao") == (7, 9))

    # CT-S31: vida restaurada
    _resultado("CT-S31", "vida do jogador restaurada corretamente",
               jogador_carregado.get("vida") == 80)

    # CT-S32: xp restaurado
    _resultado("CT-S32", "xp do jogador restaurado corretamente",
               jogador_carregado.get("xp") == 150)

    # CT-S33: ataque restaurado
    _resultado("CT-S33", "ataque do jogador restaurado corretamente",
               jogador_carregado.get("ataque") == 11)

    # CT-S34: inventário restaurado com 1 item
    _, inventario = modulo_jogador.getInventario("Guerreiro")
    _resultado("CT-S34", "inventário restaurado com 1 item", len(inventario) == 1)

    # CT-S35: item do inventário restaurado corretamente
    codigo_tipo, tipo_item = itens.getTipoItem(inventario[0])
    codigo_valor, valor_item = itens.getValorItem(inventario[0])
    _resultado("CT-S35", "item do inventário restaurado corretamente",
               codigo_tipo == 0 and tipo_item == "ataque" and codigo_valor == 0 and valor_item == 5)

    # CT-S36: itens do módulo restaurados
    estado_itens = itens.exportarEstadoItens()
    _resultado("CT-S36", "módulo itens restaurado com itens corretos", len(estado_itens) > 0)

    # CT-S37: inimigos do módulo restaurados
    estado_inimigos = inimigos.exportarEstadoInimigos()
    _resultado("CT-S37", "módulo inimigos restaurado com inimigos corretos", len(estado_inimigos) > 0)

    # CT-S38: eventos do mapa restaurados
    _resultado("CT-S38", "eventos do mapa não estão vazios após carga",
               len(mapa_carregado.get("eventos", {})) > 0)

    # CT-S39: item alocado no mapa restaurado na posição correta
    from mapa import getItemMapa
    status_item, id_item_restaurado = getItemMapa(mapa_carregado, 2, 12)
    _resultado("CT-S39", "item no mapa restaurado na posição (2,12)", status_item == 0)

    # CT-S40: inimigo alocado no mapa restaurado na posição correta
    from mapa import getInimigoMapa
    status_ini, id_ini_restaurado = getInimigoMapa(mapa_carregado, 5, 11)
    _resultado("CT-S40", "inimigo no mapa restaurado na posição (5,11)", status_ini == 0)

    # CT-S41: salvar duas vezes sobrescreve o arquivo
    jogador_original["posicao"] = (9, 9)
    resultado = modulo_jogador.exportarJogador("Guerreiro")
    codigo_jogador, dados_jogador = resultado
    dados_jogador["vida"] = 60
    dados_jogador["vivo"] = True
    modulo_jogador.restaurarJogador(dados_jogador)
    jogador_original["vida"] = 60
    salvar.salvarJogo(jogador_original, mapa_original)
    _, jogador2, _ = salvar.carregarJogo(_prepararEntidadesTeste)
    _resultado("CT-S41", "segundo save sobrescreve o primeiro",
               jogador2.get("posicao") == (9, 9) and jogador2.get("vida") == 60)

    _limparSave()

if __name__ == "__main__":
    print("=" * 50)
    print("  Testes do módulo salvar")
    print("=" * 50)

    testar_existeSalvamento()
    testar_salvarJogo()
    testar_carregarJogo()

    print("\n" + "=" * 50)
    print(f"  Resultado: {_passou}/{_total} testes passaram")
    print("=" * 50)

    sys.exit(0 if _passou == _total else 1)