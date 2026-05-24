from main import *

def main():
    status, jogador, mapa = iniciarJogo("Ana")
    if status != 0:
        print("Erro ao iniciar jogo")
        return
    exibirStatus(jogador, mapa)
    print("Todos os testes passaram com sucesso!")

if __name__ == "__main__":
    main()