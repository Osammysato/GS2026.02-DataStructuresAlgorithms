"""Classes do projeto (recorte: Assistencia social).

Servico -> um registro (servico ou orientacao para o cidadao)
No      -> no da lista encadeada, guarda o Servico e aponta pro proximo
"""

# categorias fixas, assim a analise por categoria nao fica baguncada
CATEGORIAS = [
    "Transferência de renda",
    "Segurança alimentar",
    "Habitação",
    "Atendimento socioassistencial",
    "Benefícios eventuais",
]


class Servico:

    def __init__(self, id_servico, titulo, categoria, publico_alvo,
                 requisitos, local_atendimento):
        # bool tambem e int no Python, entao precisa barrar separado
        if type(id_servico) is not int or id_servico <= 0:
            raise ValueError("O identificador deve ser um inteiro positivo.")
        if titulo is None or not str(titulo).strip():
            raise ValueError("O título é obrigatório.")
        if categoria not in CATEGORIAS:
            raise ValueError("Categoria inválida.")

        self.id = id_servico
        self.titulo = str(titulo).strip()
        self.categoria = categoria
        self.publico_alvo = str(publico_alvo).strip()
        self.requisitos = str(requisitos).strip()
        self.local_atendimento = str(local_atendimento).strip()

    def __str__(self):
        return (f"[{self.id}] {self.titulo}\n"
                f"    Categoria ........: {self.categoria}\n"
                f"    Público atendido .: {self.publico_alvo}\n"
                f"    Requisitos .......: {self.requisitos}\n"
                f"    Local ............: {self.local_atendimento}")


class No:
    def __init__(self, servico):
        self.servico = servico
        self.proximo = None
