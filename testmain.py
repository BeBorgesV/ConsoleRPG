from main import *
import builtins


def main():
    status, jogador, mapa = iniciarJogo("Ana")
    if status != 0:
        print("Erro ao iniciar jogo")
        return
    exibirStatus(jogador, mapa)
    print("Todos os testes passaram com sucesso!")

def testar_processarComando():
    _, jogador = criarJogador("Ana")
    estrutura = {
        "regioes": ["floresta", "cidade", "dungeon"],
        "tamanho": (10, 10),
        "posicao_inicial": (0, 0)
    }
    _, mapa = criarMapa(estrutura)

    entrada_original = builtins.input
    builtins.input = lambda _="": "4"
    resultado = processarComando(jogador, mapa, "mover")
    builtins.input = entrada_original

    assert processarComando(jogador, mapa, "voar") == 1
    assert processarComando(None, mapa, "mover") == 2
    assert processarComando(jogador, None, "mover") == 2
    assert processarComando(jogador, mapa, None) == 2
    print("testar_processarComando: OK")

def testar_loopJogo():
    _, jogador = criarJogador("Ana")
    estrutura = {
        "regioes": ["floresta", "cidade", "dungeon"],
        "tamanho": (10, 10),
        "posicao_inicial": (0, 0)
    }
    _, mapa = criarMapa(estrutura)

    # CT-P06: saída normal com comando "sair"
    entrada_original = builtins.input
    builtins.input = lambda _="": "sair"
    assert loopJogo(jogador, mapa) == 0
    builtins.input = entrada_original
    print("CT-P06: OK")

    # CT-P07: jogador morre
    _, jogador2 = criarJogador("Ana")
    jogador2["vida"] = 0
    assert loopJogo(jogador2, mapa) == 0
    print("CT-P07: OK")

    # parâmetros inválidos
    assert loopJogo(None, mapa) == 2
    assert loopJogo(jogador, None) == 2
    print("CT-parametro invalido: OK")
    
    print("testar_loopJogo: OK")

if __name__ == "__main__":
    testar_processarComando()
    testar_loopJogo()
    main()