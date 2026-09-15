from repositories.categoria_repository import CategoriaRepository


class ListarCategoriasService:
    """
    Sem argumentos: retorna todas (usado nos <select> de outras telas).
    Com pagina/por_pagina: retorna um dicionário paginado, usado pela
    tela de administração.
    """

    def __init__(self):
        self.repository = CategoriaRepository()

    def executar(self, pagina=None, por_pagina=None):
        if pagina and por_pagina:
            paginacao = self.repository.listar_paginado(pagina, por_pagina)
            return {
                "itens": [categoria.to_dict() for categoria in paginacao.items],
                "pagina_atual": paginacao.page,
                "por_pagina": paginacao.per_page,
                "total_paginas": paginacao.pages,
                "total_itens": paginacao.total,
            }

        categorias = self.repository.listar_todos()
        return [categoria.to_dict() for categoria in categorias]


class BuscarCategoriaPorIdService:
    def __init__(self):
        self.repository = CategoriaRepository()

    def executar(self, categoria_id):
        categoria = self.repository.buscar_por_id(categoria_id)
        if categoria is None:
            return None
        return categoria.to_dict()
