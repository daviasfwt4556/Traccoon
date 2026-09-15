from models import Material
from repositories.categoria_repository import CategoriaRepository
from repositories.material_repository import MaterialRepository


class CadastrarMaterialService:
    def __init__(self):
        self.repository = MaterialRepository()
        self.repository_categoria = CategoriaRepository()

    def executar(self, categoria_id, conteudo, url=None):
        if not conteudo:
            raise ValueError("O conteúdo do material é obrigatório.")

        categoria = self.repository_categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise ValueError("Categoria não encontrada.")

        material = Material(categoria_id=categoria_id, conteudo=conteudo, url=url)
        self.repository.criar(material)
        return material.to_dict()
