from repositories.questao_repository import QuestaoRepository


class ListarQuestoesService:
    """
    Sem argumentos: retorna todas (usado ao montar um simulado e nos
    <select> de outras telas).
    Com pagina/por_pagina: retorna um dicionário paginado, usado pela
    tela de administração.
    """

    def __init__(self):
        self.repository = QuestaoRepository()

    def executar(self, pagina=None, por_pagina=None):
        if pagina and por_pagina:
            paginacao = self.repository.listar_paginado(pagina, por_pagina)
            return {
                "itens": [questao.to_dict() for questao in paginacao.items],
                "pagina_atual": paginacao.page,
                "por_pagina": paginacao.per_page,
                "total_paginas": paginacao.pages,
                "total_itens": paginacao.total,
            }

        questoes = self.repository.listar_todos()
        return [questao.to_dict() for questao in questoes]


class BuscarQuestaoPorIdService:
    def __init__(self):
        self.repository = QuestaoRepository()

    def executar(self, questao_id):
        questao = self.repository.buscar_por_id(questao_id)
        if questao is None:
            return None
        return questao.to_dict()


class ListarQuestoesPorCategoriaService:
    def __init__(self):
        self.repository = QuestaoRepository()

    def executar(self, categoria_id):
        questoes = self.repository.listar_por_categoria(categoria_id)
        return [questao.to_dict() for questao in questoes]
