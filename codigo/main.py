# Citizen Assist AI - Assistencia social (GS 2026.2 - DSA)
# menu no terminal. rodar: python main.py

from modelos import CATEGORIAS, Servico
from lista_encadeada import ListaEncadeada
from algoritmos import (buscar_por_titulo, buscar_por_categoria, ordenar,
                        contar_por_categoria)
from dados_exemplo import DADOS_EXEMPLO

MENU = """
========== CITIZEN ASSIST AI - ASSISTÊNCIA SOCIAL ==========
 1 - Cadastrar serviço
 2 - Consultar serviço por ID
 3 - Atualizar serviço
 4 - Excluir serviço
 5 - Pesquisar (título ou categoria)
 6 - Ordenar e exibir
 7 - Listar todos
 8 - Apresentar análise
 9 - Carregar dados de exemplo
 0 - Encerrar
============================================================"""


# funcoes de leitura (ficam pedindo de novo ate vir algo valido)

def ler_texto(msg, obrigatorio=True):
    while True:
        texto = input(msg).strip()
        if texto or not obrigatorio:
            return texto
        print("  ! Campo obrigatório. Tente novamente.")


def ler_inteiro_positivo(msg):
    while True:
        bruto = input(msg).strip()
        # isdecimal pra nao aceitar coisas tipo "1_000" ou "²"
        digitos = bruto[1:] if bruto.startswith("-") else bruto
        if not digitos.isdecimal():
            print(f"  ! '{bruto}' não é um número inteiro. Tente novamente.")
            continue
        valor = int(bruto)
        if valor <= 0:
            print("  ! O ID deve ser maior que zero.")
            continue
        return valor


def escolher_categoria(permitir_vazio=False):
    for i, nome in enumerate(CATEGORIAS, start=1):
        print(f"   {i} - {nome}")
    while True:
        bruto = input("  Categoria (número)" + (" [Enter mantém]" if permitir_vazio else "") + ": ").strip()
        if permitir_vazio and bruto == "":
            return None
        if bruto.isdecimal() and 1 <= int(bruto) <= len(CATEGORIAS):
            return CATEGORIAS[int(bruto) - 1]
        print(f"  ! Opção inválida. Digite de 1 a {len(CATEGORIAS)}.")


def exibir(servicos):
    for s in servicos:
        print(s)
        print("-" * 60)


# operacoes do menu

def cadastrar(lista):
    print("\n--- CADASTRAR ---")
    id_servico = ler_inteiro_positivo("  ID: ")
    if lista.buscar_por_id(id_servico) is not None:
        print(f"  ! ID {id_servico} já cadastrado. Cadastro cancelado.")
        return
    titulo = ler_texto("  Título: ")
    categoria = escolher_categoria()
    publico = ler_texto("  Público atendido: ")
    requisitos = ler_texto("  Requisitos: ")
    local = ler_texto("  Local de atendimento: ")
    lista.inserir(Servico(id_servico, titulo, categoria, publico, requisitos, local))
    print("  Serviço cadastrado com sucesso.")


def consultar(lista):
    print("\n--- CONSULTAR POR ID ---")
    if lista.esta_vazia():
        print("  Nenhum serviço cadastrado.")
        return
    id_servico = ler_inteiro_positivo("  ID: ")
    servico = lista.buscar_por_id(id_servico)
    if servico is None:
        print(f"  Nenhum serviço encontrado com o ID {id_servico}.")
    else:
        print(servico)


def atualizar(lista):
    print("\n--- ATUALIZAR ---")
    if lista.esta_vazia():
        print("  Nenhum serviço cadastrado.")
        return
    id_servico = ler_inteiro_positivo("  ID do serviço: ")
    servico = lista.buscar_por_id(id_servico)
    if servico is None:
        print(f"  Nenhum serviço encontrado com o ID {id_servico}.")
        return
    print(servico)
    print("  (Enter mantém o valor atual)")
    campos = {}
    for campo, rotulo in (("titulo", "Título"), ("publico_alvo", "Público atendido"),
                          ("requisitos", "Requisitos"), ("local_atendimento", "Local de atendimento")):
        novo = ler_texto(f"  {rotulo}: ", obrigatorio=False)
        if novo:
            campos[campo] = novo
    categoria = escolher_categoria(permitir_vazio=True)
    if categoria:
        campos["categoria"] = categoria
    if not campos:
        print("  Nada foi alterado.")
        return
    lista.atualizar(id_servico, **campos)
    print("  Serviço atualizado.")


def excluir(lista):
    print("\n--- EXCLUIR ---")
    if lista.esta_vazia():
        print("  Nenhum serviço cadastrado.")
        return
    id_servico = ler_inteiro_positivo("  ID do serviço: ")
    removido = lista.remover(id_servico)
    if removido is None:
        print(f"  Nenhum serviço encontrado com o ID {id_servico}.")
    else:
        print(f"  Serviço '{removido.titulo}' excluído.")


def pesquisar(lista):
    print("\n--- PESQUISAR ---")
    if lista.esta_vazia():
        print("  Nenhum serviço cadastrado.")
        return
    print("   1 - Por título (contém o texto)\n   2 - Por categoria")
    opcao = input("  Opção: ").strip()
    if opcao == "1":
        termo = ler_texto("  Texto do título: ")
        resultado = buscar_por_titulo(lista, termo)
    elif opcao == "2":
        resultado = buscar_por_categoria(lista, escolher_categoria())
    else:
        print("  ! Opção inválida.")
        return
    if not resultado:
        print("  Nenhum serviço encontrado.")
    else:
        print(f"  {len(resultado)} serviço(s) encontrado(s):")
        exibir(resultado)


def ordenar_e_exibir(lista):
    print("\n--- ORDENAR (Merge Sort) ---")
    if lista.esta_vazia():
        print("  Nenhum serviço cadastrado.")
        return
    print("   1 - Por ID\n   2 - Por título\n   3 - Por categoria (e título)")
    criterios = {"1": "id", "2": "titulo", "3": "categoria"}
    opcao = input("  Critério: ").strip()
    if opcao not in criterios:
        print("  ! Opção inválida.")
        return
    ordenar(lista, criterios[opcao])
    print(f"  Lista ordenada por {criterios[opcao]}:")
    exibir(lista.percorrer())


def listar(lista):
    print("\n--- TODOS OS SERVIÇOS ---")
    if lista.esta_vazia():
        print("  Nenhum serviço cadastrado.")
        return
    exibir(lista.percorrer())


def analise(lista):
    print("\n--- ANÁLISE ---")
    total = len(lista)
    print(f"  Total de serviços cadastrados: {total}")
    if total == 0:
        return
    for categoria, qtd in contar_por_categoria(lista).items():
        pct = qtd * 100 / total
        print(f"  {categoria:<30} {qtd:>3}  ({pct:5.1f}%)  {'#' * qtd}")


def carregar_exemplo(lista):
    inseridos = 0
    for dados in DADOS_EXEMPLO:
        try:
            lista.inserir(Servico(*dados))
            inseridos += 1
        except ValueError:
            pass  # ID já existe: mantém o registro atual
    print(f"  {inseridos} serviço(s) de exemplo carregado(s).")


def main():
    lista = ListaEncadeada()
    acoes = {"1": cadastrar, "2": consultar, "3": atualizar, "4": excluir,
             "5": pesquisar, "6": ordenar_e_exibir, "7": listar,
             "8": analise, "9": carregar_exemplo}
    while True:
        print(MENU)
        try:
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "0":
                print("Encerrando o Citizen Assist AI. Até logo!")
                break
            acao = acoes.get(opcao)
            if acao is None:
                print(f"  ! Opção '{opcao}' inexistente.")
            else:
                acao(lista)
        except ValueError as erro:
            # nao deveria chegar aqui, mas se chegar o menu nao cai
            print(f"  ! Erro: {erro}")
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando o Citizen Assist AI. Até logo!")
            break


if __name__ == "__main__":
    main()
