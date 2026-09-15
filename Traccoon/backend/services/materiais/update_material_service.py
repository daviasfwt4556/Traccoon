from repositories.material_repository import MaterialRepository


class EditarMaterialService:
    def __init__(self):
        self.repository = MaterialRepository()

    def executar(self, material_id, conteudo, url):
        material = self.repository.buscar_por_id(material_id)
        if material is None:
            raise ValueError("Material não encontrado.")

        if not conteudo:
            raise ValueError("O conteúdo é obrigatório.")

        material.atualizar(conteudo=conteudo, url=url)
        self.repository.salvar_alteracoes()
        return material.to_dict()
