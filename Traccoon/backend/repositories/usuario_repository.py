"""
Repository de Usuario: concentra toda consulta e persistência desta
entidade (Usuario.query, db.session.add/commit/delete). Services nunca
acessam isso diretamente — só chamam os métodos daqui.

Nota: para o CRUD simples de Usuario isso substitui os métodos estáticos
que antes ficavam na própria classe Model (padrão Active Record). A
lógica que pertence de fato ao objeto (definir_senha, verificar_senha,
to_dict) continua no Model — só o acesso ao banco migrou pra cá.
"""

from models import Usuario, db


class UsuarioRepository:
    def listar_todos(self):
        """READ: retorna todos os usuários, sem paginação (uso interno)."""
        return Usuario.query.order_by(Usuario.id.asc()).all()

    def listar_paginado(self, pagina, por_pagina):
        """READ paginado: usado pela tela de administração."""
        return Usuario.query.order_by(Usuario.id.asc()).paginate(
            page=pagina, per_page=por_pagina, error_out=False
        )

    def buscar_por_id(self, id):
        return Usuario.query.get(id)

    def buscar_por_email(self, email):
        return Usuario.query.filter_by(email=email).first()

    def contar_todos(self):
        """Usado pela regra 'primeiro usuário cadastrado vira admin'."""
        return Usuario.query.count()

    def criar(self, usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    def salvar_alteracoes(self):
        """Persiste alterações feitas em um usuário já existente (UPDATE)."""
        db.session.commit()

    def deletar(self, usuario):
        db.session.delete(usuario)
        db.session.commit()
