from modelos import CATEGORIAS, No

CAMPOS_EDITAVEIS = ("titulo", "categoria", "publico_alvo",
                    "requisitos", "local_atendimento")


class ListaEncadeada:

    def __init__(self):
        self.cabeca = None
        self.cauda = None
        self.tamanho = 0

    def esta_vazia(self):
        return self.cabeca is None

    def __len__(self):
        return self.tamanho

    def percorrer(self):
        # vai do primeiro ao ultimo devolvendo cada servico
        atual = self.cabeca
        while atual is not None:
            yield atual.servico
            atual = atual.proximo

    def __iter__(self):
        return self.percorrer()

    def buscar_por_id(self, id_servico):
        # busca sequencial, retorna None se nao achar
        atual = self.cabeca
        while atual is not None:
            if atual.servico.id == id_servico:
                return atual.servico
            atual = atual.proximo
        return None

    def inserir(self, servico):
        # a propria lista nao deixa entrar ID repetido
        if self.buscar_por_id(servico.id) is not None:
            raise ValueError(f"Já existe um serviço com o ID {servico.id}.")

        novo = No(servico)
        if self.cabeca is None:
            self.cabeca = novo
            self.cauda = novo
        else:
            self.cauda.proximo = novo
            self.cauda = novo
        self.tamanho += 1

    def remover(self, id_servico):
        anterior = None
        atual = self.cabeca
        while atual is not None and atual.servico.id != id_servico:
            anterior = atual
            atual = atual.proximo

        if atual is None:          # nao achou (ou lista vazia)
            return None

        if anterior is None:       # era a cabeca
            self.cabeca = atual.proximo
        else:
            anterior.proximo = atual.proximo

        if atual is self.cauda:    # era o ultimo, a cauda volta um
            self.cauda = anterior

        atual.proximo = None
        self.tamanho -= 1
        return atual.servico

    def atualizar(self, id_servico, **campos):
        # o id nao pode mudar, senao podia quebrar a regra de ID unico
        servico = self.buscar_por_id(id_servico)
        if servico is None:
            return False

        # primeiro valida tudo, so depois altera (ou muda tudo ou nada)
        for nome in campos:
            if nome not in CAMPOS_EDITAVEIS:
                raise ValueError(f"Campo inexistente: {nome}")
        if "titulo" in campos:
            t = campos["titulo"]
            if t is None or not str(t).strip():
                raise ValueError("O título é obrigatório.")
        if "categoria" in campos and campos["categoria"] not in CATEGORIAS:
            raise ValueError("Categoria inválida.")

        for nome, valor in campos.items():
            setattr(servico, nome, str(valor).strip())
        return True
