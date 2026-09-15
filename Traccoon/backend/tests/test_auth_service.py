import pytest

from services.auth.login_service import LoginService
from services.auth.registrar_usuario_service import RegistrarUsuarioService


class TestRegistrarUsuarioService:
    def test_primeiro_usuario_cadastrado_vira_admin(self, app_context):
        usuario = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        assert usuario.id is not None
        assert usuario.is_admin is True

    def test_segundo_usuario_cadastrado_nao_vira_admin(self, app_context):
        RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")
        segundo = RegistrarUsuarioService().executar("Bruno", "bruno@exemplo.com", "123456")

        assert segundo.is_admin is False

    def test_senha_e_guardada_com_hash_e_nao_em_texto_puro(self, app_context):
        usuario = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        assert usuario.senha_hash != "123456"
        assert usuario.verificar_senha("123456") is True

    def test_nao_permite_email_duplicado(self, app_context):
        RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        with pytest.raises(ValueError):
            RegistrarUsuarioService().executar("Ana da Silva", "ana@exemplo.com", "outrasenha")

    def test_nao_permite_senha_curta(self, app_context):
        with pytest.raises(ValueError):
            RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "12")

    def test_nao_permite_campos_vazios(self, app_context):
        with pytest.raises(ValueError):
            RegistrarUsuarioService().executar("", "ana@exemplo.com", "123456")


class TestLoginService:
    def test_login_com_credenciais_corretas(self, app_context):
        RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        usuario = LoginService().executar("ana@exemplo.com", "123456")

        assert usuario.email == "ana@exemplo.com"

    def test_login_com_senha_errada(self, app_context):
        RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        with pytest.raises(ValueError):
            LoginService().executar("ana@exemplo.com", "senhaerrada")

    def test_login_com_email_inexistente(self, app_context):
        with pytest.raises(ValueError):
            LoginService().executar("naoexiste@exemplo.com", "123456")
