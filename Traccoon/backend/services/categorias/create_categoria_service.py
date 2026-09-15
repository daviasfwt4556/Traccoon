from models import Categoria
from repositories.categoria_repository import CategoriaRepository


class CadastrarCategoriaService:
    def __init__(self):
        self.repository = CategoriaRepository()

    def executar(self, nome, descricao=None):
        if not nome:
            raise ValueError("O nome da categoria é obrigatório.")

        categoria = Categoria(nome=nome, descricao=descricao)
        self.repository.criar(categoria)
        return categoria.to_dict()
