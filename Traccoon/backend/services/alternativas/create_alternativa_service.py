from models import Alternativa
from repositories.alternativa_repository import AlternativaRepository
from repositories.questao_repository import QuestaoRepository


class CadastrarAlternativaService:
    def __init__(self):
        self.repository = AlternativaRepository()
        self.repository_questao = QuestaoRepository()

    def executar(self, questao_id, texto, correta=False):
        if not texto:
            raise ValueError("O texto da alternativa é obrigatório.")

        questao = self.repository_questao.buscar_por_id(questao_id)
        if questao is None:
            raise ValueError("Questão não encontrada.")

        alternativa = Alternativa(questao_id=questao_id, texto=texto, correta=bool(correta))
        self.repository.criar(alternativa)
        return alternativa.to_dict()
