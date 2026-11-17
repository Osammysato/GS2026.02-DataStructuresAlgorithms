# Citizen Assist AI - Documentação técnica
GS 2026.2 - Citizen Tech | Data Structures and Algorithms | Python

## 1. Recorte

Escolhemos **Assistência social**, que é uma das sugestões do enunciado ("programas, público atendido,
requisitos e locais de atendimento").

A ideia é o cidadão conseguir ver quais serviços existem, quem tem direito, o que precisa levar e onde
ir. Deixamos as categorias fixas (são 5) pra contagem por categoria não ficar errada por causa de
digitação diferente:

1. Transferência de renda
2. Segurança alimentar
3. Habitação
4. Atendimento socioassistencial
5. Benefícios eventuais

Os 8 serviços de `dados_exemplo.py` são inventados, só pra teste e demonstração. O enunciado fala que
não precisa integrar com serviço público real.

## 2. Modelo do registro

Cada serviço é um objeto da classe `Servico` (arquivo `modelos.py`) com estes campos:

| Campo | Tipo | Regra |
|---|---|---|
| id | int | identificador único, maior que zero |
| titulo | str | obrigatório |
| categoria | str | tem que ser uma das 5 categorias |
| publico_alvo | str | quem é atendido |
| requisitos | str | documentos ou condições |
| local_atendimento | str | onde ir |

O próprio construtor já valida id, título e categoria e dá `ValueError` se tiver algo errado, então um
registro inválido não chega nem a ser criado.

## 3. Lista encadeada

Usamos uma lista simplesmente encadeada. Cada nó é um objeto `No` que guarda o serviço e a referência
pro próximo nó:

```python
class No:
    def __init__(self, servico):
        self.servico = servico
        self.proximo = None
```

A classe `ListaEncadeada` guarda três coisas:

- `cabeca`: o primeiro nó
- `cauda`: o último nó. Com ela dá pra ligar um nó novo no fim direto (`cauda.proximo = novo`), sem
  andar a lista toda.
- `tamanho`: quantidade de nós, usado no `len()` e no total da análise.

```
cabeca -> [id 7] -> [id 3] -> ... -> [id 8] -> None
                                       ^
cauda ---------------------------------+
```

Operações:

- **inserir(servico):** primeiro procura se o ID já existe (se existir, dá erro e não insere). Se a
  lista estiver vazia o nó novo vira cabeça e cauda; senão liga depois da cauda e ele vira a nova cauda.
  Soma 1 no tamanho.
- **percorrer():** começa na cabeça e vai seguindo `proximo` até chegar em `None`.
- **buscar_por_id(id):** busca sequencial, devolve o serviço ou `None`.
- **remover(id):** anda com dois ponteiros, `anterior` e `atual`. Se o nó for a cabeça, a cabeça passa
  a ser o próximo dele; se não, o anterior passa a apontar pro próximo do removido. Se o removido era a
  cauda, a cauda volta pro anterior. Se não achar o ID, devolve `None` e não mexe em nada.
- **atualizar(id, campos):** acha o serviço, valida todos os campos novos e só depois altera. Se
  algum for inválido, nada muda. O ID não pode ser alterado, assim não tem risco de duplicar.

Os casos chatos da remoção (cabeça, meio, cauda e único elemento) estão nos testes 06 e 22, que
conferem cabeça, cauda e tamanho depois de remover.

## 4. Menu

```
 1 - Cadastrar serviço           6 - Ordenar e exibir
 2 - Consultar serviço por ID    7 - Listar todos
 3 - Atualizar serviço           8 - Apresentar análise
 4 - Excluir serviço             9 - Carregar dados de exemplo
 5 - Pesquisar                   0 - Encerrar
```

O que o menu trata:

| Situação | O que acontece |
|---|---|
| opção que não existe | mostra `! Opção 'x' inexistente.` e volta pro menu |
| ID com letra (`abc`), `1_000`, `²` etc. | `não é um número inteiro`, pede de novo |
| ID 0 ou negativo | `O ID deve ser maior que zero`, pede de novo |
| ID que já existe no cadastro | `ID 7 já cadastrado. Cadastro cancelado.` (verifica antes de pedir o resto) |
| campo obrigatório vazio | `Campo obrigatório`, pede de novo |
| categoria fora de 1 a 5 | `Opção inválida. Digite de 1 a 5.` |
| consulta, pesquisa ou exclusão que não acha nada | `Nenhum serviço encontrado...` |
| qualquer operação com a lista vazia | `Nenhum serviço cadastrado.` |
| Ctrl+C ou fim da entrada | encerra normalmente |

Na atualização, apertar Enter mantém o valor que já estava.

## 5. Algoritmos

### 5.1 Busca sequencial

Usamos busca sequencial em três lugares: `buscar_por_id`, `buscar_por_titulo` e `buscar_por_categoria`.
A de título procura se o título **contém** o texto digitado, sem diferenciar maiúscula e acento (então
"orientacao" acha "Orientação").

```python
atual = self.cabeca
while atual is not None:
    if atual.servico.id == id_servico:
        return atual.servico
    atual = atual.proximo
return None
```

Quando não acha nada: a busca por ID devolve `None` e as pesquisas devolvem uma lista vazia. O menu
mostra "Nenhum serviço encontrado" e a lista continua igual.

Pensamos em usar busca binária, mas ela precisa que os dados estejam ordenados e que dê pra pular
direto pro meio. Na lista encadeada não tem índice, pra chegar no meio tem que andar n/2 nós, o que já é
O(n). Então ela perde a vantagem do O(log n). Na pesquisa por título também não serviria porque o
critério é "contém" e não "igual".

### 5.2 Merge Sort nos nós

Escolhemos o Merge Sort (dividir e conquistar), com as mesmas etapas da aula:

```python
def merge_sort(cabeca, chave):
    if cabeca is None or cabeca.proximo is None:   # [A] caso base
        return cabeca
    direita = _dividir_ao_meio(cabeca)             # [B] divisão
    esquerda = merge_sort(cabeca, chave)           # [C] recursão
    direita = merge_sort(direita, chave)
    return _intercalar(esquerda, direita, chave)   # [D] combinação
```

- **Divisão:** como não tem índice, achamos o meio com dois ponteiros. O `lento` anda 1 e o `rapido`
  anda 2; quando o rápido chega no fim, o lento está no meio e a lista é cortada ali. O `rapido` começa
  em `cabeca.proximo` de propósito: se começasse na cabeça, uma lista de 2 nós não seria dividida e a
  recursão nunca terminaria.
- **Intercalação (merge):** compara o primeiro de cada metade e liga o menor no resultado. Quando uma
  metade acaba, liga o resto da outra de uma vez. Usamos um nó sentinela pra não precisar tratar o
  primeiro nó do resultado como caso especial.
- **Diferença pra versão da aula:** na aula o Merge Sort usava listas do Python (`lista[:meio]`,
  `resultado = []`). Aqui nenhum nó novo é criado, só mudamos os `proximo`. No final a própria lista
  encadeada fica ordenada, e o `ordenar()` acha a cauda de novo.
- **Critérios:** por id, por título ou por categoria (empate por título).
- Usamos `<=` na comparação pra ele ser estável (itens com a mesma chave ficam na ordem que estavam).

Por que não o Quick Sort: por causa do risco do pivô que vimos em aula. Com pivô fixo e lista já
ordenada, as partições ficam desbalanceadas e ele vira O(n²). No nosso sistema isso acontece fácil, é
só o usuário ordenar duas vezes pelo mesmo critério. O Merge Sort divide pela posição, então é sempre
O(n log n), e encaixa bem em lista encadeada porque o merge só troca ponteiros. Selection e Insertion
Sort são O(n²) no pior caso.

### 5.3 Análise por categoria

`contar_por_categoria` passa uma vez pela lista e soma 1 na categoria de cada serviço. O menu mostra o
total, a quantidade e a porcentagem de cada categoria, com uma barrinha de `#`.

## 6. Complexidade (Big-O) do nosso código

n = quantidade de serviços na lista. C = quantidade de categorias (5, fixo).
Comparar textos depende do tamanho do texto, mas como os títulos são curtos consideramos esse custo
constante.

### 6.1 Inserção
O `inserir` chama `buscar_por_id` antes, pra não deixar ID repetido. Num cadastro que dá certo o ID não
existe, então a busca passa pelos n nós. Depois liga pela cauda, que é O(1).
Total: O(n) no melhor, médio e pior caso (quando a inserção dá certo).
Se o ID for repetido, a busca para antes: O(1) se o repetido for a cabeça, O(n) no pior caso.
Sem a checagem de ID único a inserção seria O(1) por causa da cauda. Ou seja, quem deixa O(n) é a regra
do ID único, não a ligação do nó.
Espaço: O(1) (só o nó novo).

### 6.2 Busca por ID
- Melhor caso: está na cabeça, 1 comparação, O(1).
- Pior caso: está no último ou não existe, n comparações, O(n).
- Caso médio (ID existe, em qualquer posição): (n+1)/2 comparações em média, O(n).
- Espaço O(1).

### 6.3 Pesquisa por título ou categoria
Não para no primeiro que acha, porque precisa de todos. Então sempre percorre os n nós: O(n) em
qualquer caso. Espaço O(k), onde k é a quantidade de resultados (no pior caso k = n).

### 6.4 Remoção
Achar o nó custa igual à busca: O(1) se for a cabeça, O(n) no médio e no pior (último ou não existe).
Religar os ponteiros e ajustar cauda/tamanho é O(1), não precisa deslocar nada como num vetor.
Total: O(1) melhor, O(n) médio e pior. Espaço O(1).

### 6.5 Atualização
Busca + validar e alterar no máximo 5 campos. O(1) no melhor caso (ID na cabeça) e O(n) no médio e no
pior. Espaço O(1).

### 6.6 Percorrer / listar
Visita cada nó uma vez: O(n) sempre. Espaço O(1) (é um gerador).

### 6.7 Ordenação (Merge Sort)

Tempo:
- Numa chamada com m nós, dividir anda uns m/2 passos (O(m)) e o merge faz no máximo m - 1 comparações
  (O(m)).
- Recorrência: T(n) = 2T(n/2) + cn, com T(1) constante.
- No nível 0 da recursão tem 1 lista de n, no nível 1 tem 2 de n/2, no nível i tem 2^i listas de n/2^i.
  Em todo nível o trabalho soma n.
- A lista chega em tamanho 1 quando n/2^i = 1, ou seja, depois de log2(n) níveis.
- Total: n * log2(n), O(n log n).
- Melhor, médio e pior caso são iguais (O(n log n)), porque a divisão é pela posição e a árvore sempre
  fica balanceada, não importa os valores. O que muda é só quantas comparações o merge faz.
- O `ordenar()` ainda percorre a lista mais uma vez pra achar a cauda: O(n). Continua O(n log n).

Espaço:
- Não cria nó novo. Cada merge usa 1 sentinela e uns ponteiros.
- A recursão tem profundidade log2(n), então o espaço extra é O(log n).
- A versão da aula com listas Python usa O(n) de espaço extra.

Para conferir na prática fizemos o `medir_complexidade.py`, que conta as comparações que o código faz de
verdade:

| n | n*log2(n) | MS crescente | MS aleatória | MS decrescente | busca 1º | busca último | busca inexistente |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 24 | 12 | 17 | 12 | 1 | 8 | 8 |
| 64 | 384 | 192 | 307 | 192 | 1 | 64 | 64 |
| 512 | 4608 | 2304 | 3968 | 2304 | 1 | 512 | 512 |
| 2048 | 22528 | 11264 | 19907 | 11264 | 1 | 2048 | 2048 |

O Merge Sort nunca passou de n*log2(n). Indo de 64 pra 512 (8 vezes mais dados) a lista aleatória foi de
307 pra 3968 comparações, umas 13 vezes mais, perto do que o n*log2(n) cresce (12 vezes). Se fosse
O(n²) teria crescido 64 vezes.
Com a lista crescente ou decrescente deu exatamente metade de n*log2(n). Isso acontece porque testamos
com n potência de 2: em cada merge uma metade inteira é menor que a outra, então ela acaba depois de m/2
comparações. Pra n que não é potência de 2 o número fica perto disso, mas não exato.
A busca visita 1 nó no melhor caso e n nós no pior, crescendo linear.

### 6.8 Análise por categoria
Zera C contadores e passa pelos n nós: O(n + C), que é O(n) porque C é fixo. Espaço O(C) = O(1).

### 6.9 Menu
- Cadastrar: o menu verifica o ID antes de pedir os outros campos e o `inserir` verifica de novo. São
  duas buscas O(n), então O(n).
- Carregar m exemplos numa lista que já tem n: cada inserção custa O(n + i), total O(m(n + m)).

## 7. Resumo

| Operação | Melhor | Médio | Pior | Espaço extra |
|---|---|---|---|---|
| Inserção (com checagem de ID único) | O(n)* | O(n) | O(n) | O(1) |
| Ligar o nó no fim (pela cauda) | O(1) | O(1) | O(1) | O(1) |
| Busca por ID | O(1) | O(n) | O(n) | O(1) |
| Pesquisa por título / categoria | O(n) | O(n) | O(n) | O(k), até O(n) |
| Remoção | O(1) | O(n) | O(n) | O(1) |
| Atualização | O(1) | O(n) | O(n) | O(1) |
| Percorrer / listar | O(n) | O(n) | O(n) | O(1) |
| Ordenação (Merge Sort + achar a cauda) | O(n log n) | O(n log n) | O(n log n) | O(log n) |
| Análise por categoria | O(n) | O(n) | O(n) | O(1) |

\* quando a inserção dá certo. Se o ID repetido for a cabeça, a recusa é O(1).

## 8. Testes

### 8.1 Testes automatizados
Rodar com `python -m unittest -v testes`. Resultado: 23 testes, todos OK (saída em `evidencia_testes.txt`).

| # | Tipo | Entrada | Esperado | Resultado |
|---|---|---|---|---|
| 01 | normal | inserir os 8 exemplos | ordem 7,3,12,1,9,5,15,8 e cauda/tamanho certos | OK |
| 02 | normal | buscar ID 12 | "Orientação sobre aluguel social" | OK |
| 03 | normal | pesquisar título "ORIENTACAO" | acha o ID 12 | OK |
| 04 | normal | pesquisar categoria Segurança alimentar | IDs 3 e 5 | OK |
| 05 | normal | atualizar o local do ID 5 | local alterado | OK |
| 06 | normal | remover 12 (meio), 7 (cabeça), 8 (cauda) e inserir 99 | sobra 3,1,9,5,15 e o 99 entra no fim | OK |
| 07 | normal | ordenar por ID | 1,3,5,7,8,9,12,15 | OK |
| 08 | normal | ordenar por título | primeiro "Abrigo temporário", último "Restaurante comunitário" | OK |
| 09 | normal | ordenar por categoria | primeiro Atendimento socioassistencial, último Transferência de renda | OK |
| 10 | normal | Merge Sort com n = 0, 1, 2, 3, 10, 101 e 1000 aleatórios | igual ao `sorted()` (só usado pra conferir) | OK |
| 11 | normal | análise | Seg. alimentar 2, Transf. renda 2, Habitação 1, total 8 | OK |
| 12 | inexistente | buscar ID 404 | None | OK |
| 13 | inexistente | remover ID 404 | None e a lista continua com 8 | OK |
| 14 | inexistente | atualizar ID 404 | False | OK |
| 15 | inexistente | pesquisar "vacina" | lista vazia | OK |
| 16 | inválida | inserir ID 7 de novo | ValueError, tamanho continua 8 | OK |
| 17 | inválida | ID 0, -1, "abc", 1.5, True | ValueError | OK |
| 18 | inválida | título "   " / categoria "Esportes" | ValueError | OK |
| 19 | inválida | atualizar com categoria inválida | ValueError e o título não muda | OK |
| 20 | inválida | ordenar por "preco" | ValueError | OK |
| 21 | lista vazia | buscar, remover, atualizar, pesquisar, ordenar e analisar | nada quebra; None/False/vazio/0 | OK |
| 22 | lista vazia | remover o único elemento | cabeça e cauda viram None, tamanho 0 | OK |
| 23 | inválida (menu) | categoria "²", "abc", "9"; ID "1_000", "--1", "-1", "0" | pede de novo até vir um valor válido | OK |

### 8.2 Execução do menu
Rodamos `python main.py < roteiro.txt` e salvamos a saída em `evidencia_execucao.txt`.

| Passo | Entrada | Esperado | O que apareceu |
|---|---|---|---|
| 1 | 2 com lista vazia | aviso de lista vazia | `Nenhum serviço cadastrado.` |
| 2 | 6 com lista vazia | aviso de lista vazia | `Nenhum serviço cadastrado.` |
| 3 | 8 com lista vazia | total 0 | `Total de serviços cadastrados: 0` |
| 4 | opção `x` | opção inexistente | `! Opção 'x' inexistente.` |
| 5 | 9 | carrega os exemplos | `8 serviço(s) de exemplo carregado(s).` |
| 6 | cadastrar com ID `abc` | pede de novo | `! 'abc' não é um número inteiro.` |
| 7 | ID `0` | pede de novo | `! O ID deve ser maior que zero.` |
| 8 | ID `7` | recusa duplicado | `! ID 7 já cadastrado. Cadastro cancelado.` |
| 9 | cadastrar ID 20 com título vazio e categoria 9, depois certo | pede de novo e cadastra | `! Campo obrigatório.` / `! Opção inválida. Digite de 1 a 5.` / `Serviço cadastrado com sucesso.` |
| 10 | consultar 20 | mostra o registro | `[20] Kit natalidade ...` |
| 11 | consultar 404 | não encontrado | `Nenhum serviço encontrado com o ID 404.` |
| 12 | pesquisar título "auxilio" | acha Auxílio-funeral | `1 serviço(s) encontrado(s): [9] Auxílio-funeral` |
| 13 | pesquisar título "vacina" | não encontrado | `Nenhum serviço encontrado.` |
| 14 | pesquisar categoria 2 | IDs 3 e 5 | `2 serviço(s) encontrado(s)` |
| 15 | atualizar 20, só o local | muda só o local | `Serviço atualizado.` (local vira "Unidade móvel") |
| 16 | excluir 404 | não encontrado | `Nenhum serviço encontrado com o ID 404.` |
| 17 | ordenar por ID | 1,3,5,7,8,9,12,15,20 | apareceu nessa ordem |
| 18 | ordenar por categoria | agrupado, desempate por título | Abrigo, Acompanhamento, Auxílio, Kit, ... |
| 19 | análise | total 9 | Habitação 1 (11,1%), as outras 2 (22,2%) |
| 20 | excluir 20 e listar | removido | `Serviço 'Kit natalidade' excluído.` |
| 21 | 0 | encerra | `Encerrando o Citizen Assist AI. Até logo!` |

### 8.3 Roteiro da apresentação
A ideia é mostrar a estrutura funcionando e não só as telas:
1. Com a lista vazia, usar as opções 2 e 8 e digitar uma opção que não existe.
2. Opção 9 e depois 7: aparece na ordem em que foi inserido, porque cada nó entrou no fim pela cauda.
3. Tentar cadastrar o ID 7 (é recusado) e depois um ID novo, que aparece no fim da listagem.
4. Ordenar por ID e listar de novo: a própria lista ficou ordenada, porque o Merge Sort trocou os
   ponteiros dos nós.
5. Excluir o primeiro e o último e cadastrar outro: ele entra no fim, mostrando que a cauda continua
   certa.
6. Pesquisar "auxilio" sem acento e mostrar a análise.
7. Rodar `python medir_complexidade.py` e `python -m unittest -v testes`.

## 9. Decisões e limitações

Algumas decisões que tomamos:
- Lista simples com `cauda` e `tamanho`. Não fizemos lista dupla porque nenhuma operação precisa andar
  pra trás.
- A verificação de ID único fica dentro do `inserir`, assim a própria lista garante isso mesmo que o
  menu falhe. O preço é a inserção ser O(n).
- O ID não muda na atualização, pra não correr risco de duplicar.
- Na atualização valida tudo antes de mudar qualquer coisa.
- Merge Sort em vez de Quick Sort, pelo O(n log n) garantido e por gastar O(log n) de memória.
- Categoria escolhida por número, pra evitar erro de digitação.
- Pesquisa por título com "contém" e sem acento, que é mais fácil pro cidadão usar.

Limitações:
- Os dados ficam só na memória e somem quando fecha o programa. Salvar em arquivo era opcional e não
  fizemos.
- Inserir, buscar, atualizar e remover são O(n). Com muitos dados uma árvore (BST/AVL, que vimos nas
  aulas de árvores) ou uma tabela hash seria mais rápida, mas o enunciado pede lista encadeada.
- Depois de ordenar a ordem original de cadastro se perde, porque a própria lista é reorganizada. Foi de
  propósito, pra dar pra ver os nós sendo religados.
- Usamos `list` só pra devolver os resultados da pesquisa e `dict` pros contadores da análise. Os
  registros mesmo ficam só na lista encadeada.
- A recursão do Merge Sort tem profundidade log2(n) (uns 20 níveis pra 1 milhão de registros), longe do
  limite do Python.

## 10. Onde está cada item do enunciado

| Item | Onde |
|---|---|
| 3.1 cadastro com ID único em lista encadeada própria | `Servico`, `ListaEncadeada.inserir`, menu 1 e 9 |
| 3.2 consulta por ID e pesquisa por atributo | `buscar_por_id`, `buscar_por_titulo`, `buscar_por_categoria`, menu 2 e 5, seção 5.1 |
| 3.3 ordenação com algoritmo próprio | Merge Sort em `algoritmos.py`, menu 6, seção 5.2 |
| 3.4 lista encadeada com inserção, percurso e remoção | `lista_encadeada.py`, seção 3 |
| 3.5 atualizar/excluir mantendo a lista certa e análise | `atualizar`, `remover`, menu 8, testes 06, 13, 19 e 22 |
| 3.6 menu e validação | `main.py`, seção 4, testes 12 a 20 e 23 |
| 4 complexidade | seções 6 e 7 |
| 4 testes | seção 8 |
| 6 entregáveis | `README.md`, este documento, `evidencia_*.txt`, roteiro 8.3 |
