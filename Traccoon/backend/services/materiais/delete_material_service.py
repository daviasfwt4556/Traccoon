from repositories.material_repository import MaterialRepository


class DeletarMaterialService:
    def __init__(self):
        self.repository = MaterialRepository()

    def executar(self, material_id):
        material = self.repository.buscar_por_id(material_id)
        if material is None:
            raise ValueError("Material não encontrado.")

        self.repository.deletar(material)
        return True
