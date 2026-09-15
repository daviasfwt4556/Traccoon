import pytest

from services.categorias.create_categoria_service import CadastrarCategoriaService
from services.materiais.create_material_service import CadastrarMaterialService
from services.materiais.delete_material_service import DeletarMaterialService
from services.materiais.read_material_service import ListarMateriaisPorCategoriaService
from services.materiais.update_material_service import EditarMaterialService


def _criar_categoria(app_context):
    return CadastrarCategoriaService().executar("Direção Defensiva", "Boas práticas ao volante")


class TestCadastrarMaterialService:
    def test_cadastra_material_em_categoria_existente(self, app_context):
        categoria = _criar_categoria(app_context)

        dados = CadastrarMaterialService().executar(
            categoria["id"], conteudo="Mantenha distância do carro da frente.", url="https://exemplo.com"
        )

        assert dados["categoria_id"] == categoria["id"]
        assert dados["categoria_nome"] == categoria["nome"]

    def test_nao_permite_categoria_inexistente(self, app_context):
        with pytest.raises(ValueError):
            CadastrarMaterialService().executar(9999, conteudo="Conteúdo qualquer")

    def test_nao_permite_conteudo_vazio(self, app_context):
        categoria = _criar_categoria(app_context)

        with pytest.raises(ValueError):
            CadastrarMaterialService().executar(categoria["id"], conteudo="")


class TestEditarMaterialService:
    def test_edita_conteudo(self, app_context):
        categoria = _criar_categoria(app_context)
        material = CadastrarMaterialService().executar(categoria["id"], conteudo="Texto original")

        editado = EditarMaterialService().executar(material["id"], conteudo="Texto revisado", url=None)

        assert editado["conteudo"] == "Texto revisado"

    def test_erro_ao_editar_material_inexistente(self, app_context):
        with pytest.raises(ValueError):
            EditarMaterialService().executar(9999, conteudo="Texto", url=None)


class TestDeletarMaterialService:
    def test_deleta_material_existente(self, app_context):
        categoria = _criar_categoria(app_context)
        material = CadastrarMaterialService().executar(categoria["id"], conteudo="Texto original")

        assert DeletarMaterialService().executar(material["id"]) is True
        assert ListarMateriaisPorCategoriaService().executar(categoria["id"]) == []

    def test_erro_ao_deletar_material_inexistente(self, app_context):
        with pytest.raises(ValueError):
            DeletarMaterialService().executar(9999)
