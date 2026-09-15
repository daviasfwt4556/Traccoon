from repositories.usuario_repository import UsuarioRepository


class ListarUsuariosService:
    """
    Sem argumentos: retorna todos (uso interno/compatibilidade).
    Com pagina/por_pagina: retorna um dicionário paginado, usado pela
    tela de administração para não carregar a base inteira de uma vez.
    """

    def __init__(self):
        self.repository = UsuarioRepository()

    def executar(self, pagina=None, por_pagina=None):
        if pagina and por_pagina:
            paginacao = self.repository.listar_paginado(pagina, por_pagina)
            return {
                "itens": [usuario.to_dict() for usuario in paginacao.items],
                "pagina_atual": paginacao.page,
                "por_pagina": paginacao.per_page,
                "total_paginas": paginacao.pages,
                "total_itens": paginacao.total,
            }

        usuarios = self.repository.listar_todos()
        return [usuario.to_dict() for usuario in usuarios]


class BuscarUsuarioPorIdService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def executar(self, usuario_id):
        usuario = self.repository.buscar_por_id(usuario_id)
        if usuario is None:
            return None
        return usuario.to_dict()
