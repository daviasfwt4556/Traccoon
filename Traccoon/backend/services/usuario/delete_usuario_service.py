from repositories.usuario_repository import UsuarioRepository


class DeletarUsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def executar(self, usuario_id):
        usuario = self.repository.buscar_por_id(usuario_id)
        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        self.repository.deletar(usuario)
        return True
