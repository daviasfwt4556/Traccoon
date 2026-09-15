from models import Questao
from repositories.categoria_repository import CategoriaRepository
from repositories.questao_repository import QuestaoRepository


class CadastrarQuestaoService:
    def __init__(self):
        self.repository = QuestaoRepository()
        self.repository_categoria = CategoriaRepository()

    def executar(self, enunciado, categoria_id):
        if not enunciado:
            raise ValueError("O enunciado da questão é obrigatório.")

        categoria = self.repository_categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise ValueError("Categoria não encontrada.")

        questao = Questao(enunciado=enunciado, categoria_id=categoria_id)
        self.repository.criar(questao)
        return questao.to_dict()
