"""Conta as comparacoes que o codigo faz de verdade, pra comparar com o Big-O.
Rodar:  python medir_complexidade.py"""

import math
import random

from modelos import Servico
from lista_encadeada import ListaEncadeada
from algoritmos import _intercalar, _dividir_ao_meio

comparacoes = 0


def montar(n, ordem):
    lista = ListaEncadeada()
    ids = list(range(1, n + 1))
    if ordem == "aleatoria":
        random.Random(1).shuffle(ids)
    elif ordem == "decrescente":
        ids.reverse()
    for i in ids:
        lista.inserir(Servico(i, f"t{i}", "Habitação", "", "", ""))
    return lista


class ChaveContada:
    # embrulha o id e soma 1 cada vez que o <= e usado no merge
    def __init__(self, valor):
        self.valor = valor

    def __le__(self, outro):
        global comparacoes
        comparacoes += 1
        return self.valor <= outro.valor


def merge_sort_contando(cabeca):
    # mesmo merge sort do algoritmos.py, so que com a chave que conta
    if cabeca is None or cabeca.proximo is None:
        return cabeca
    direita = _dividir_ao_meio(cabeca)
    esquerda = merge_sort_contando(cabeca)
    direita = merge_sort_contando(direita)
    return _intercalar(esquerda, direita, lambda s: ChaveContada(s.id))


def comparacoes_merge_sort(lista):
    global comparacoes
    comparacoes = 0
    lista.cabeca = merge_sort_contando(lista.cabeca)
    return comparacoes


def nos_visitados_busca(lista, alvo):
    visitados = 0
    atual = lista.cabeca
    while atual is not None:
        visitados += 1
        if atual.servico.id == alvo:
            break
        atual = atual.proximo
    return visitados


print(f"{'n':>6} | {'n*log2(n)':>10} | {'MS crescente':>12} | {'MS aleatória':>12} | "
      f"{'MS decresc.':>11} | {'busca 1º':>8} | {'busca último':>12} | {'busca inexist.':>14}")
for n in (8, 64, 512, 2048):
    nlogn = round(n * math.log2(n))
    ms = [comparacoes_merge_sort(montar(n, o)) for o in ("crescente", "aleatoria", "decrescente")]
    lst = montar(n, "crescente")
    print(f"{n:>6} | {nlogn:>10} | {ms[0]:>12} | {ms[1]:>12} | {ms[2]:>11} | "
          f"{nos_visitados_busca(lst, 1):>8} | {nos_visitados_busca(lst, n):>12} | "
          f"{nos_visitados_busca(lst, -1):>14}")
