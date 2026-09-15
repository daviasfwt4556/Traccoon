import pytest

from services.alternativas.create_alternativa_service import CadastrarAlternativaService
from services.alternativas.delete_alternativa_service import DeletarAlternativaService
from services.alternativas.update_alternativa_service import EditarAlternativaService
from services.categorias.create_categoria_service import CadastrarCategoriaService
from services.questoes.create_questao_service import CadastrarQuestaoService


def _criar_questao(app_context):
    categoria = CadastrarCategoriaService().executar("Legislação", "Regras de trânsito")
    return CadastrarQuestaoService().executar("Enunciado de teste", categoria["id"])


class TestCadastrarAlternativaService:
    def test_cadastra_alternativa_em_questao_existente(self, app_context):
        questao = _criar_questao(app_context)

        dados = CadastrarAlternativaService().executar(questao["id"], "Resposta A", correta=True)

        assert dados["questao_id"] == questao["id"]
        assert dados["correta"] is True

    def test_nao_permite_questao_inexistente(self, app_context):
        with pytest.raises(ValueError):
            CadastrarAlternativaService().executar(9999, "Resposta A", correta=True)

    def test_nao_permite_texto_vazio(self, app_context):
        questao = _criar_questao(app_context)

        with pytest.raises(ValueError):
            CadastrarAlternativaService().executar(questao["id"], "", correta=False)


class TestEditarAlternativaService:
    def test_edita_texto_e_marca_como_correta(self, app_context):
        questao = _criar_questao(app_context)
        alternativa = CadastrarAlternativaService().executar(questao["id"], "Resposta A", correta=False)

        editada = EditarAlternativaService().executar(alternativa["id"], texto="Resposta A revisada", correta=True)

        assert editada["texto"] == "Resposta A revisada"
        assert editada["correta"] is True

    def test_erro_ao_editar_alternativa_inexistente(self, app_context):
        with pytest.raises(ValueError):
            EditarAlternativaService().executar(9999, texto="Texto", correta=True)


class TestDeletarAlternativaService:
    def test_deleta_alternativa_existente(self, app_context):
        questao = _criar_questao(app_context)
        alternativa = CadastrarAlternativaService().executar(questao["id"], "Resposta A", correta=True)

        assert DeletarAlternativaService().executar(alternativa["id"]) is True

    def test_erro_ao_deletar_alternativa_inexistente(self, app_context):
        with pytest.raises(ValueError):
            DeletarAlternativaService().executar(9999)
