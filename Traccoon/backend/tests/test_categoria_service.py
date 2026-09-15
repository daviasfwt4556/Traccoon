import pytest

from services.categorias.create_categoria_service import CadastrarCategoriaService
from services.categorias.delete_categoria_service import DeletarCategoriaService
from services.categorias.update_categoria_service import EditarCategoriaService


class TestCadastrarCategoriaService:
    def test_cadastra_categoria_com_sucesso(self, app_context):
        dados = CadastrarCategoriaService().executar("Legislação", "Regras de trânsito")

        assert dados["nome"] == "Legislação"
        assert dados["total_questoes"] == 0

    def test_nao_permite_nome_vazio(self, app_context):
        with pytest.raises(ValueError):
            CadastrarCategoriaService().executar("", "Alguma descrição")


class TestEditarCategoriaService:
    def test_edita_categoria_existente(self, app_context):
        criada = CadastrarCategoriaService().executar("Legislação", "Regras de trânsito")

        editada = EditarCategoriaService().executar(
            criada["id"], nome="Legislação de Trânsito", descricao="Nova descrição"
        )

        assert editada["nome"] == "Legislação de Trânsito"
        assert editada["descricao"] == "Nova descrição"

    def test_erro_ao_editar_categoria_inexistente(self, app_context):
        with pytest.raises(ValueError):
            EditarCategoriaService().executar(9999, nome="X", descricao="Y")


class TestDeletarCategoriaService:
    def test_deleta_categoria_existente(self, app_context):
        criada = CadastrarCategoriaService().executar("Legislação", "Regras de trânsito")

        assert DeletarCategoriaService().executar(criada["id"]) is True

    def test_erro_ao_deletar_categoria_inexistente(self, app_context):
        with pytest.raises(ValueError):
            DeletarCategoriaService().executar(9999)
