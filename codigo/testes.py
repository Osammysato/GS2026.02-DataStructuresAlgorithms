import random
import unittest
from unittest.mock import patch

from modelos import Servico
from lista_encadeada import ListaEncadeada
from algoritmos import (buscar_por_titulo, buscar_por_categoria, ordenar,
                        contar_por_categoria)
from dados_exemplo import DADOS_EXEMPLO
import main


def nova_lista():
    lista = ListaEncadeada()
    for dados in DADOS_EXEMPLO:
        lista.inserir(Servico(*dados))
    return lista


def ids(lista):
    return [s.id for s in lista.percorrer()]


def integra(lista):
    # confere se cabeca, cauda e tamanho batem com o que da pra percorrer
    nos = list(lista.percorrer())
    if not nos:
        return lista.cabeca is None and lista.cauda is None and lista.tamanho == 0
    return (lista.cauda.servico is nos[-1] and lista.cauda.proximo is None
            and lista.tamanho == len(nos))


class TestCasosNormais(unittest.TestCase):

    def test_01_inserir_mantem_ordem_de_cadastro(self):
        lista = nova_lista()
        self.assertEqual(ids(lista), [7, 3, 12, 1, 9, 5, 15, 8])
        self.assertTrue(integra(lista))

    def test_02_buscar_por_id(self):
        self.assertEqual(nova_lista().buscar_por_id(12).titulo,
                         "Orientação sobre aluguel social")

    def test_03_buscar_por_titulo_ignora_acento_e_maiusculas(self):
        r = buscar_por_titulo(nova_lista(), "ORIENTACAO")
        self.assertEqual([s.id for s in r], [12])

    def test_04_buscar_por_categoria(self):
        r = buscar_por_categoria(nova_lista(), "Segurança alimentar")
        self.assertEqual([s.id for s in r], [3, 5])

    def test_05_atualizar(self):
        lista = nova_lista()
        self.assertTrue(lista.atualizar(5, local_atendimento="Nova unidade"))
        self.assertEqual(lista.buscar_por_id(5).local_atendimento, "Nova unidade")

    def test_06_remover_meio_cabeca_cauda(self):
        lista = nova_lista()
        self.assertEqual(lista.remover(12).id, 12)   # meio
        self.assertEqual(lista.remover(7).id, 7)     # cabeça
        self.assertEqual(lista.remover(8).id, 8)     # cauda
        self.assertEqual(ids(lista), [3, 1, 9, 5, 15])
        self.assertTrue(integra(lista))
        lista.inserir(Servico(99, "Novo", "Habitação", "x", "x", "x"))
        self.assertEqual(ids(lista)[-1], 99)          # cauda continua válida

    def test_07_ordenar_por_id(self):
        lista = nova_lista()
        ordenar(lista, "id")
        self.assertEqual(ids(lista), [1, 3, 5, 7, 8, 9, 12, 15])
        self.assertTrue(integra(lista))

    def test_08_ordenar_por_titulo(self):
        lista = nova_lista()
        ordenar(lista, "titulo")
        titulos = [s.titulo for s in lista.percorrer()]
        self.assertEqual(titulos[0], "Abrigo temporário")
        self.assertEqual(titulos[-1], "Restaurante comunitário")

    def test_09_ordenar_por_categoria(self):
        lista = nova_lista()
        ordenar(lista, "categoria")
        cats = [s.categoria for s in lista.percorrer()]
        self.assertEqual(cats[0], "Atendimento socioassistencial")
        self.assertEqual(cats[-1], "Transferência de renda")

    def test_10_merge_sort_contra_referencia_aleatoria(self):
        rnd = random.Random(42)
        for n in (0, 1, 2, 3, 10, 101, 1000):
            lista = ListaEncadeada()
            valores = rnd.sample(range(1, 100000), n)
            for v in valores:
                lista.inserir(Servico(v, f"t{v}", "Habitação", "", "", ""))
            ordenar(lista, "id")
            self.assertEqual(ids(lista), sorted(valores))   # sorted() só como gabarito
            self.assertTrue(integra(lista))

    def test_11_analise_por_categoria(self):
        c = contar_por_categoria(nova_lista())
        self.assertEqual(c["Segurança alimentar"], 2)
        self.assertEqual(c["Transferência de renda"], 2)
        self.assertEqual(c["Habitação"], 1)
        self.assertEqual(sum(c.values()), 8)


class TestRegistrosInexistentes(unittest.TestCase):

    def test_12_buscar_id_inexistente(self):
        self.assertIsNone(nova_lista().buscar_por_id(404))

    def test_13_remover_id_inexistente_nao_altera_lista(self):
        lista = nova_lista()
        self.assertIsNone(lista.remover(404))
        self.assertEqual(len(lista), 8)
        self.assertTrue(integra(lista))

    def test_14_atualizar_id_inexistente(self):
        self.assertFalse(nova_lista().atualizar(404, titulo="X"))

    def test_15_pesquisa_sem_resultado(self):
        self.assertEqual(buscar_por_titulo(nova_lista(), "vacina"), [])


class TestEntradasInvalidas(unittest.TestCase):

    def test_16_id_duplicado(self):
        lista = nova_lista()
        with self.assertRaises(ValueError):
            lista.inserir(Servico(7, "Outro", "Habitação", "x", "x", "x"))
        self.assertEqual(len(lista), 8)

    def test_17_id_invalido(self):
        for invalido in (0, -1, "abc", 1.5, True):
            with self.assertRaises(ValueError):
                Servico(invalido, "T", "Habitação", "x", "x", "x")

    def test_18_titulo_vazio_e_categoria_invalida(self):
        with self.assertRaises(ValueError):
            Servico(1, "   ", "Habitação", "x", "x", "x")
        with self.assertRaises(ValueError):
            Servico(1, "T", "Esportes", "x", "x", "x")

    def test_19_atualizar_com_valor_invalido_nao_altera(self):
        lista = nova_lista()
        with self.assertRaises(ValueError):
            lista.atualizar(3, titulo="Novo", categoria="Esportes")
        self.assertEqual(lista.buscar_por_id(3).titulo, "Cesta básica emergencial")

    def test_20_criterio_de_ordenacao_invalido(self):
        with self.assertRaises(ValueError):
            ordenar(nova_lista(), "preco")

    def test_23_menu_recusa_entradas_estranhas(self):
        # "²" passava no isdigit() e derrubava o programa no int()
        with patch("builtins.input", side_effect=["²", "abc", "9", "2"]), \
             patch("builtins.print"):
            self.assertEqual(main.escolher_categoria(), "Segurança alimentar")
        with patch("builtins.input", side_effect=["1_000", "--1", "-1", "0", "15"]), \
             patch("builtins.print"):
            self.assertEqual(main.ler_inteiro_positivo("ID: "), 15)


class TestListaVazia(unittest.TestCase):

    def test_21_operacoes_com_lista_vazia(self):
        lista = ListaEncadeada()
        self.assertTrue(lista.esta_vazia())
        self.assertIsNone(lista.buscar_por_id(1))
        self.assertIsNone(lista.remover(1))
        self.assertFalse(lista.atualizar(1, titulo="X"))
        self.assertEqual(buscar_por_titulo(lista, "x"), [])
        ordenar(lista, "id")
        self.assertEqual(ids(lista), [])
        self.assertEqual(sum(contar_por_categoria(lista).values()), 0)
        self.assertTrue(integra(lista))

    def test_22_remover_unico_elemento_esvazia_lista(self):
        lista = ListaEncadeada()
        lista.inserir(Servico(1, "T", "Habitação", "x", "x", "x"))
        lista.remover(1)
        self.assertTrue(integra(lista))
        self.assertTrue(lista.esta_vazia())


if __name__ == "__main__":
    unittest.main(verbosity=2)
