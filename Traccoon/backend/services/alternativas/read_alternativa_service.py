from repositories.alternativa_repository import AlternativaRepository


class ListarAlternativasService:
    """
    Sem argumentos: retorna todas.
    Com pagina/por_pagina: retorna um dicionário paginado, usado pela
    tela de administração.
    """

    def __init__(self):
        self.repository = AlternativaRepository()

    def executar(self, pagina=None, por_pagina=None):
        if pagina and por_pagina:
            paginacao = self.repository.listar_paginado(pagina, por_pagina)
            return {
                "itens": [alternativa.to_dict() for alternativa in paginacao.items],
                "pagina_atual": paginacao.page,
                "por_pagina": paginacao.per_page,
                "total_paginas": paginacao.pages,
                "total_itens": paginacao.total,
            }

        alternativas = self.repository.listar_todos()
        return [alternativa.to_dict() for alternativa in alternativas]


class BuscarAlternativaPorIdService:
    def __init__(self):
        self.repository = AlternativaRepository()

    def executar(self, alternativa_id):
        alternativa = self.repository.buscar_por_id(alternativa_id)
        if alternativa is None:
            return None
        return alternativa.to_dict()


class ListarAlternativasPorQuestaoService:
    def __init__(self):
        self.repository = AlternativaRepository()

    def executar(self, questao_id):
        alternativas = self.repository.listar_por_questao(questao_id)
        return [alternativa.to_dict() for alternativa in alternativas]
