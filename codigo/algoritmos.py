import unicodedata

from modelos import CATEGORIAS, No


def normalizar(texto):
    # tira acento e deixa minusculo ("Habitação" vira "habitacao")
    decomposto = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return sem_acento.lower().strip()


# ---------------- busca ----------------

def buscar_por_titulo(lista, termo):
    """Busca sequencial: passa por todos os nos e guarda os que tem o termo
    no titulo. Se nao achar nada devolve lista vazia."""
    termo = normalizar(termo)
    if termo == "":
        return []
    encontrados = []
    atual = lista.cabeca
    while atual is not None:
        if termo in normalizar(atual.servico.titulo):
            encontrados.append(atual.servico)
        atual = atual.proximo
    return encontrados


def buscar_por_categoria(lista, categoria):
    encontrados = []
    atual = lista.cabeca
    while atual is not None:
        if atual.servico.categoria == categoria:
            encontrados.append(atual.servico)
        atual = atual.proximo
    return encontrados


# ---------------- ordenacao ----------------

CRITERIOS = {
    "id": lambda s: s.id,
    "titulo": lambda s: normalizar(s.titulo),
    # categoria e, empatou, titulo
    "categoria": lambda s: (normalizar(s.categoria), normalizar(s.titulo)),
}


def _dividir_ao_meio(cabeca):
    # lento anda 1, rapido anda 2. quando o rapido chega no fim o lento ta no meio.
    # rapido comeca em cabeca.proximo pra lista de 2 nos dividir em 1 + 1
    # (se comecasse em cabeca, a esquerda ficava com os 2 e a recursao nao parava)
    lento = cabeca
    rapido = cabeca.proximo
    while rapido is not None and rapido.proximo is not None:
        lento = lento.proximo
        rapido = rapido.proximo.proximo
    direita = lento.proximo
    lento.proximo = None
    return direita


def _intercalar(esquerda, direita, chave):
    # merge: pega sempre o menor dos dois inicios e liga no resultado.
    # nao cria no novo, so troca os "proximo".
    # o sentinela e so pra nao ter que tratar o primeiro no separado
    sentinela = No(None)
    ultimo = sentinela
    while esquerda is not None and direita is not None:
        if chave(esquerda.servico) <= chave(direita.servico):   # <= deixa estavel
            ultimo.proximo = esquerda
            esquerda = esquerda.proximo
        else:
            ultimo.proximo = direita
            direita = direita.proximo
        ultimo = ultimo.proximo
    # o que sobrou ja esta em ordem, so liga
    if esquerda is not None:
        ultimo.proximo = esquerda
    else:
        ultimo.proximo = direita
    return sentinela.proximo


def merge_sort(cabeca, chave):
    # [A] caso base: 0 ou 1 no
    if cabeca is None or cabeca.proximo is None:
        return cabeca
    # [B] divisao
    direita = _dividir_ao_meio(cabeca)
    # [C] recursao
    esquerda = merge_sort(cabeca, chave)
    direita = merge_sort(direita, chave)
    # [D] combinacao
    return _intercalar(esquerda, direita, chave)


def ordenar(lista, criterio):
    if criterio not in CRITERIOS:
        raise ValueError("Critério de ordenação inválido.")
    lista.cabeca = merge_sort(lista.cabeca, CRITERIOS[criterio])
    # depois de ordenar o ultimo no mudou, entao acha a cauda de novo
    atual = lista.cabeca
    while atual is not None and atual.proximo is not None:
        atual = atual.proximo
    lista.cauda = atual


# ---------------- analise ----------------

def contar_por_categoria(lista):
    contagem = {}
    for c in CATEGORIAS:
        contagem[c] = 0
    atual = lista.cabeca
    while atual is not None:
        contagem[atual.servico.categoria] += 1
        atual = atual.proximo
    return contagem
