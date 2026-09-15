from repositories.usuario_repository import UsuarioRepository


class EditarUsuarioService:
    def __init__(self):
        self.repository = UsuarioRepository()

    def executar(self, usuario_id, nome, email, senha=None, foto_url=None, is_admin=None):
        usuario = self.repository.buscar_por_id(usuario_id)
        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        if email:
            outro = self.repository.buscar_por_email(email)
            if outro and outro.id != usuario.id:
                raise ValueError("Já existe outro usuário cadastrado com este e-mail.")

        if senha and len(senha) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")

        usuario.atualizar(nome=nome, email=email, senha=senha, foto_url=foto_url, is_admin=is_admin)
        self.repository.salvar_alteracoes()
        return usuario.to_dict()
