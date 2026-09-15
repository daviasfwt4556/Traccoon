import pytest

from services.usuario.create_usuario_service import CadastrarUsuarioService
from services.usuario.delete_usuario_service import DeletarUsuarioService
from services.usuario.read_usuarios_service import ListarUsuariosService
from services.usuario.update_usuario_serivce import EditarUsuarioService


class TestCadastrarUsuarioService:
    def test_cadastra_usuario_com_sucesso(self, app_context):
        dados = CadastrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        assert dados["nome"] == "Ana"
        assert dados["email"] == "ana@exemplo.com"
        assert "senha" not in dados
        assert "senha_hash" not in dados

    def test_nao_permite_email_duplicado(self, app_context):
        CadastrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        with pytest.raises(ValueError):
            CadastrarUsuarioService().executar("Outra Ana", "ana@exemplo.com", "654321")

    def test_nao_permite_campos_obrigatorios_vazios(self, app_context):
        with pytest.raises(ValueError):
            CadastrarUsuarioService().executar("", "", "")


class TestEditarUsuarioService:
    def test_edita_nome_e_email(self, app_context):
        criado = CadastrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        editado = EditarUsuarioService().executar(
            criado["id"], nome="Ana Paula", email="ana.paula@exemplo.com"
        )

        assert editado["nome"] == "Ana Paula"
        assert editado["email"] == "ana.paula@exemplo.com"

    def test_nao_permite_trocar_para_email_de_outro_usuario(self, app_context):
        CadastrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")
        bruno = CadastrarUsuarioService().executar("Bruno", "bruno@exemplo.com", "123456")

        with pytest.raises(ValueError):
            EditarUsuarioService().executar(bruno["id"], nome="Bruno", email="ana@exemplo.com")

    def test_erro_ao_editar_usuario_inexistente(self, app_context):
        with pytest.raises(ValueError):
            EditarUsuarioService().executar(9999, nome="Ninguém", email="ninguem@exemplo.com")


class TestDeletarUsuarioService:
    def test_deleta_usuario_existente(self, app_context):
        criado = CadastrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        assert DeletarUsuarioService().executar(criado["id"]) is True
        assert ListarUsuariosService().executar() == []

    def test_erro_ao_deletar_usuario_inexistente(self, app_context):
        with pytest.raises(ValueError):
            DeletarUsuarioService().executar(9999)


class TestListarUsuariosService:
    def test_lista_todos_sem_paginacao(self, app_context):
        CadastrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")
        CadastrarUsuarioService().executar("Bruno", "bruno@exemplo.com", "123456")

        usuarios = ListarUsuariosService().executar()

        assert len(usuarios) == 2

    def test_lista_paginada_traz_metadados_corretos(self, app_context):
        for i in range(5):
            CadastrarUsuarioService().executar(f"Usuario {i}", f"user{i}@exemplo.com", "123456")

        pagina_1 = ListarUsuariosService().executar(pagina=1, por_pagina=2)

        assert len(pagina_1["itens"]) == 2
        assert pagina_1["total_itens"] == 5
        assert pagina_1["total_paginas"] == 3
        assert pagina_1["pagina_atual"] == 1
