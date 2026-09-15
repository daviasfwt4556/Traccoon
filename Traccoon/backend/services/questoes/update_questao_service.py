from repositories.categoria_repository import CategoriaRepository
from repositories.questao_repository import QuestaoRepository


class EditarQuestaoService:
    def __init__(self):
        self.repository = QuestaoRepository()
        self.repository_categoria = CategoriaRepository()

    def executar(self, questao_id, enunciado, categoria_id):
        questao = self.repository.buscar_por_id(questao_id)
        if questao is None:
            raise ValueError("Questão não encontrada.")

        if not enunciado:
            raise ValueError("O enunciado é obrigatório.")

        if categoria_id and self.repository_categoria.buscar_por_id(categoria_id) is None:
            raise ValueError("Categoria não encontrada.")

        questao.atualizar(enunciado=enunciado, categoria_id=categoria_id)
        self.repository.salvar_alteracoes()
        return questao.to_dict()
