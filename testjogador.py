import itens  # Importa o módulo itens para gerar os IDs válidos nos testes
from jogador import *

def testar_criarJogador():
    # CT-J01 - Sucesso retorna o dicionário cópia
    res = criarJogador("Ana")
    assert isinstance(res, dict)
    assert res["nome"] == "Ana"
    assert res["vida"] == 100

    # CT-J02 - Erros continuam retornando os códigos numéricos
    assert criarJogador("") == 1

    # CT-J03
    assert criarJogador(None) == 2

    print("testar_criarJogador: OK")

testar_criarJogador()


def testar_getVida():
    criarJogador("Ana")

    # CT-J04
    assert getVida("Ana") == (0, 100)

    # CT-J05 / CT-J06
    assert getVida("Inexistente") == (2, None)
    assert getVida(None) == (2, None)

    print("testar_getVida: OK")

testar_getVida()


def testar_getXP():
    criarJogador("Ana")

    # CT-J07
    assert getXP("Ana") == (0, 0)

    # CT-J08 / CT-J09
    assert getXP("Inexistente") == (2, None)
    assert getXP(None) == (2, None)

    print("testar_getXP: OK")

testar_getXP()


def testar_getAtaque():
    criarJogador("Ana")

    # CT-J10
    assert getAtaque("Ana") == (0, 10)

    # CT-J11 / CT-J12
    assert getAtaque("Inexistente") == (2, None)

    print("testar_getAtaque: OK")

testar_getAtaque()


def testar_getInventario():
    criarJogador("Ana")

    # CT-J16 - Inventário inicialmente vazio
    assert getInventario("Ana") == (0, [])

    # CT-J17 / CT-J18
    assert getInventario("Inexistente") == (2, None)

    print("testar_getInventario: OK")

testar_getInventario()


def testar_receberDanoJogador():
    criarJogador("Ana")

    # CT-J22
    assert receberDanoJogador("Ana", 20) == 0
    assert getVida("Ana") == (0, 80)

    # CT-J23
    assert receberDanoJogador("Ana", -10) == 2

    # CT-J24
    assert receberDanoJogador("Inexistente", 10) == 2

    print("testar_receberDanoJogador: OK")

testar_receberDanoJogador()


def testar_curarJogador():
    criarJogador("Ana")
    receberDanoJogador("Ana", 50)

    # CT-J25
    assert curarJogador("Ana", 20) == 0
    assert getVida("Ana") == (0, 70)

    # Completa a vida
    curarJogador("Ana", 100)

    # CT-J26
    assert curarJogador("Ana", 20) == 1

    # CT-J27 (Cura inválida)
    assert curarJogador("Ana", -10) == 2

    print("testar_curarJogador: OK")

testar_curarJogador()


def testar_ganharXP():
    criarJogador("Ana")

    # CT-J28
    assert ganharXP("Ana", 20) == 0
    assert getXP("Ana") == (0, 20)

    # CT-J29
    assert ganharXP("Ana", -5) == 2

    print("testar_ganharXP: OK")

testar_ganharXP()


def testar_atualizarAtaque():
    criarJogador("Ana")
    ganharXP("Ana", 100)

    # CT-J30
    assert atualizarAtaque("Ana") == 0
    assert getAtaque("Ana") == (0, 11)

    # CT-J31
    assert atualizarAtaque("Inexistente") == 2

    print("testar_atualizarAtaque: OK")

testar_atualizarAtaque()


def testar_adicionarItemJogador():
    criarJogador("Ana")

    # Criamos um item real usando o módulo itens para obter um id válido
    codigo_item, id_pocao = itens.criarItem("Poção", "cura", 20)
    assert codigo_item == 0

    # CT-J32 - Adiciona passando o ID inteiro recebido
    assert adicionarItemJogador("Ana", id_pocao) == 0

    codigo, inventario = getInventario("Ana")
    # Agora o inventário deve conter o ID (inteiro), não o dicionário
    assert id_pocao in inventario
    assert isinstance(inventario[0], int)

    # Preenche inventário até o limite (já tem 1 item, adiciona mais 4 IDs)
    for i in range(4):
        _, id_extra = itens.criarItem(f"item{i}", "ataque", 5)
        adicionarItemJogador("Ana", id_extra)

    # CT-J33 - Limite excedido (5 itens já guardados)
    _, id_excedente = itens.criarItem("Excedente", "chave", 1)
    assert adicionarItemJogador("Ana", id_excedente) == 1

    # CT-J34 - Parâmetros inválidos
    assert adicionarItemJogador("Inexistente", id_pocao) == 2
    assert adicionarItemJogador("Ana", None) == 2
    assert adicionarItemJogador("Ana", -5) == 2  # ID negativo inválido

    print("testar_adicionarItemJogador: OK")

testar_adicionarItemJogador()


def testar_usarItemJogador():
    criarJogador("Ana")
    receberDanoJogador("Ana", 50)  # Vida cai de 100 para 50

    # Cria um item de cura no módulo itens e adiciona o id ao jogador
    # Nota: Assumindo que itens.criarItem retorna (codigo, id_item)
    _, id_pocao = itens.criarItem("Poção Grande", "cura", 30)
    adicionarItemJogador("Ana", id_pocao)

    # CT-J35 - Usar o item passando o ID de forma encapsulada
    assert usarItemJogador("Ana", id_pocao) == 0
    assert getVida("Ana") == (0, 80)  # 50 + 30 = 80 pontos de vida

    # CT-J36 - Tentar usar o mesmo item novamente (ele já foi removido)
    assert usarItemJogador("Ana", id_pocao) == 1

    # CT-J37 - Parâmetros inválidos
    assert usarItemJogador("Inexistente", id_pocao) == 2
    assert usarItemJogador("Ana", None) == 2
    assert usarItemJogador("Ana", -5) == 2  # ID negativo inválido

    print("testar_usarItemJogador: OK")

# Chamada única corrigida
testar_usarItemJogador()


def testar_encapsulamento():
    res = criarJogador("Carlos")
    res["vida"] = 999  # Tenta modificar a cópia de retorno externa
    
    # O TAD real do jogador deve continuar protegido com 100 de vida
    assert getVida("Carlos") == (0, 100)
    print("testar_encapsulamento: OK")

testar_encapsulamento()


def testar_exportarJogador():
    criarJogador("Ana")
    
    # CT-J38 (Sucesso): Exporta o jogador cadastrado com sucesso
    codigo, dados_ana = exportarJogador("Ana")
    assert codigo == 0
    assert isinstance(dados_ana, dict)
    assert dados_ana["nome"] == "Ana"
    assert dados_ana["vida"] == 100
    assert dados_ana["inventario"] == []

    # CT-J39 (Encapsulamento): Modificar a cópia exportada não altera o TAD real
    dados_ana["vida"] = 5  # Altera a cópia externamente
    assert getVida("Ana") == (0, 100)  # A vida real continua intacta

    # CT-J40 (Erros): Parâmetro inválido ou jogador inexistente
    assert exportarJogador("Inexistente") == 2
    assert exportarJogador("") == 2
    assert exportarJogador(None) == 2

    print("testar_exportarJogador: OK")

testar_exportarJogador()

def testar_restaurarJogador():
    # Estrutura de dados válida simulando um arquivo de gravação correto
    save_valido = {
        "nome": "Arthur ",
        "vida": 90,
        "vida_max": 100,
        "xp": 150,
        "ataque": 11,
        "vivo": True,
        "inventario": [0, 4]
    }

    # CT-J41 (Sucesso): Restauração bem-sucedida de um novo jogador
    assert restaurarJogador(save_valido) == 0
    
    # Valida se os dados foram de facto gravados no TAD através das funções públicas
    assert getVida("Arthur") == (0, 90)
    assert getXP("Arthur") == (0, 150)
    assert getInventario("Arthur") == (0, [0, 4])

    # Sobrescrita: Se enviarmos dados modificados para o mesmo nome, ele deve atualizar
    save_modificado = save_valido.copy()
    save_modificado["vida"] = 40
    assert restaurarJogador(save_modificado) == 0
    assert getVida("Arthur") == (0, 40)

    # CT-J42 (Segurança - Dados corrompidos ou inconsistentes):
    # Caso 1: Vida maior que a vida máxima
    save_invalido = save_valido.copy()
    save_invalido["vida"] = 300
    assert restaurarJogador(save_invalido) == 1

    # Caso 2: Vida zero mas marcado como vivo=True (Inconsistência de estado)
    save_invalido = save_valido.copy()
    save_invalido["vida"] = 0
    save_invalido["vivo"] = True
    assert restaurarJogador(save_invalido) == 1

    # Caso 3: Inventário com tipo de dado inválido (string em vez de id numérico)
    save_invalido = save_valido.copy()
    save_invalido["inventario"] = [0, "id_corrompido"]
    assert restaurarJogador(save_invalido) == 1

    # Caso 4: Chave obrigatória ausente
    save_incompleto = {
        "nome": "Incompleto",
        "vida": 100
    }
    assert restaurarJogador(save_incompleto) == 1

    # CT-J43 (Parâmetros inválidos)
    assert restaurarJogador(None) == 2
    assert restaurarJogador([1, 2, 3]) == 2

    # Verificação de Encapsulamento pós-restauração:
    # Modificar o dicionário original de fora não pode alterar o TAD interno
    save_modificado["vida"] = 5
    assert getVida("Arthur") == (0, 40)  # Continua isolado e protegido

    print("testar_restaurarJogador: OK")

testar_restaurarJogador()

print("\n>>> Todos os testes atualizados do módulo Jogador passaram com sucesso! <<<")