from repositories.questao_repository import QuestaoRepository


class DeletarQuestaoService:
    def __init__(self):
        self.repository = QuestaoRepository()

    def executar(self, questao_id):
        questao = self.repository.buscar_por_id(questao_id)
        if questao is None:
            raise ValueError("Questão não encontrada.")

        self.repository.deletar(questao)
        return True
