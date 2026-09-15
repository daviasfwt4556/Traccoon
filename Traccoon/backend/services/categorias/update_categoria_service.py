from repositories.categoria_repository import CategoriaRepository


class EditarCategoriaService:
    def __init__(self):
        self.repository = CategoriaRepository()

    def executar(self, categoria_id, nome, descricao):
        categoria = self.repository.buscar_por_id(categoria_id)
        if categoria is None:
            raise ValueError("Categoria não encontrada.")

        if not nome or not descricao:
            raise ValueError("Nome e descrição são obrigatórios!")

        categoria.atualizar(nome=nome, descricao=descricao)
        self.repository.salvar_alteracoes()
        return categoria.to_dict()
