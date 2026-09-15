from repositories.material_repository import MaterialRepository


class ListarMateriaisService:
    """
    Sem argumentos: retorna todos.
    Com pagina/por_pagina: retorna um dicionário paginado, usado pela
    tela de administração.
    """

    def __init__(self):
        self.repository = MaterialRepository()

    def executar(self, pagina=None, por_pagina=None):
        if pagina and por_pagina:
            paginacao = self.repository.listar_paginado(pagina, por_pagina)
            return {
                "itens": [material.to_dict() for material in paginacao.items],
                "pagina_atual": paginacao.page,
                "por_pagina": paginacao.per_page,
                "total_paginas": paginacao.pages,
                "total_itens": paginacao.total,
            }

        materiais = self.repository.listar_todos()
        return [material.to_dict() for material in materiais]


class BuscarMaterialPorIdService:
    def __init__(self):
        self.repository = MaterialRepository()

    def executar(self, material_id):
        material = self.repository.buscar_por_id(material_id)
        if material is None:
            return None
        return material.to_dict()


class ListarMateriaisPorCategoriaService:
    def __init__(self):
        self.repository = MaterialRepository()

    def executar(self, categoria_id):
        materiais = self.repository.listar_por_categoria(categoria_id)
        return [material.to_dict() for material in materiais]
