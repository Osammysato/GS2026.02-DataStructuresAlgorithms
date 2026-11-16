# Citizen Assist AI - Assistência social (GS 2026.2 - DSA - Python)

Sistema de terminal pra cadastrar, consultar, atualizar, excluir, pesquisar, ordenar e analisar
serviços de assistência social. Os registros ficam numa lista encadeada feita pelo grupo, e a busca e
a ordenação (Merge Sort) também foram implementadas por nós.

A documentação completa (recorte, modelo, lista encadeada, menu, Big-O e testes) está em
[DOCUMENTACAO.md](DOCUMENTACAO.md).

## Integrantes
- Gabriel Pedro de Souza - RM: 571995
- Sammy de Moura Sato - RM: 569182

## Requisitos
Python 3.8 ou mais novo. Não usa nenhuma biblioteca externa.

## Como rodar
Dentro da pasta do código:
```bash
python main.py                    # menu (a opção 9 carrega os dados de exemplo)
python -m unittest -v testes      # 23 testes automatizados
python medir_complexidade.py      # conta as comparações pra conferir o Big-O
```

Pra repetir a mesma execução que está em `evidencia_execucao.txt`:
```bash
python main.py < roteiro.txt                      # Linux, macOS ou cmd do Windows
Get-Content roteiro.txt | python main.py          # PowerShell
```

## Arquivos
| Arquivo | O que tem |
|---|---|
| `modelos.py` | classes `Servico` e `No` e a lista de categorias |
| `lista_encadeada.py` | classe `ListaEncadeada` (inserir, percorrer, buscar por ID, remover, atualizar) |
| `algoritmos.py` | busca por título/categoria, Merge Sort nos nós e análise por categoria |
| `main.py` | menu e validação das entradas |
| `dados_exemplo.py` | 8 serviços inventados pra demonstração |
| `testes.py` | testes: casos normais, inexistentes, entradas inválidas e lista vazia |
| `medir_complexidade.py` | conta comparações do Merge Sort e nós visitados na busca |
| `roteiro.txt` | entradas usadas na execução de exemplo |
| `evidencia_execucao.txt` | saída real do menu com o roteiro |
| `evidencia_testes.txt` | saída real dos testes |
