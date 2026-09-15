from repositories.usuario_repository import UsuarioRepository


class LoginService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def executar(self, email, senha):
        if not email or not senha:
            raise ValueError("E-mail e senha são obrigatórios.")

        usuario = self.repository.buscar_por_email(email)

        # Mensagem genérica de propósito: não revela se o e-mail existe ou não.
        if usuario is None or not usuario.verificar_senha(senha):
            raise ValueError("E-mail ou senha inválidos.")

        return usuario
