import pytest

from services.alternativas.create_alternativa_service import CadastrarAlternativaService
from services.alternativas.read_alternativa_service import ListarAlternativasPorQuestaoService
from services.categorias.create_categoria_service import CadastrarCategoriaService
from services.questoes.create_questao_service import CadastrarQuestaoService
from services.questoes.delete_questao_service import DeletarQuestaoService
from services.questoes.update_questao_service import EditarQuestaoService


def _criar_categoria(app_context):
    return CadastrarCategoriaService().executar("Legislação", "Regras de trânsito")


class TestCadastrarQuestaoService:
    def test_cadastra_questao_em_categoria_existente(self, app_context):
        categoria = _criar_categoria(app_context)

        dados = CadastrarQuestaoService().executar("Qual a velocidade máxima na via?", categoria["id"])

        assert dados["categoria_id"] == categoria["id"]
        assert dados["alternativas"] == []

    def test_nao_permite_categoria_inexistente(self, app_context):
        with pytest.raises(ValueError):
            CadastrarQuestaoService().executar("Enunciado qualquer", 9999)

    def test_nao_permite_enunciado_vazio(self, app_context):
        categoria = _criar_categoria(app_context)

        with pytest.raises(ValueError):
            CadastrarQuestaoService().executar("", categoria["id"])


class TestEditarQuestaoService:
    def test_edita_enunciado(self, app_context):
        categoria = _criar_categoria(app_context)
        questao = CadastrarQuestaoService().executar("Enunciado original", categoria["id"])

        editada = EditarQuestaoService().executar(
            questao["id"], enunciado="Enunciado corrigido", categoria_id=None
        )

        assert editada["enunciado"] == "Enunciado corrigido"

    def test_nao_permite_mover_para_categoria_inexistente(self, app_context):
        categoria = _criar_categoria(app_context)
        questao = CadastrarQuestaoService().executar("Enunciado original", categoria["id"])

        with pytest.raises(ValueError):
            EditarQuestaoService().executar(questao["id"], enunciado="Enunciado", categoria_id=9999)


class TestDeletarQuestaoService:
    def test_deletar_questao_remove_alternativas_junto(self, app_context):
        categoria = _criar_categoria(app_context)
        questao = CadastrarQuestaoService().executar("Enunciado", categoria["id"])
        CadastrarAlternativaService().executar(questao["id"], "Alternativa A", correta=True)
        CadastrarAlternativaService().executar(questao["id"], "Alternativa B", correta=False)

        DeletarQuestaoService().executar(questao["id"])

        restantes = ListarAlternativasPorQuestaoService().executar(questao["id"])
        assert restantes == []

    def test_erro_ao_deletar_questao_inexistente(self, app_context):
        with pytest.raises(ValueError):
            DeletarQuestaoService().executar(9999)
