from repositories.categoria_repository import CategoriaRepository


class DeletarCategoriaService:
    def __init__(self):
        self.repository = CategoriaRepository()

    def executar(self, categoria_id):
        categoria = self.repository.buscar_por_id(categoria_id)
        if categoria is None:
            raise ValueError("Categoria não encontrada.")

        self.repository.deletar(categoria)
        return True
