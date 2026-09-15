from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .base import ModeloBase


class Usuario(ModeloBase):
    __tablename__ = "usuarios"

    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    foto_url = db.Column(db.String(500), nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now, nullable=False)
    data_atualizacao = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )

    simulados = db.relationship("Simulado", back_populates="usuario")

    # ---------- Senha ----------
    def definir_senha(self, senha):
        """Nunca guardamos a senha em texto puro — só o hash dela."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    # ---------- Regras de campo (sem tocar no banco) ----------
    # Persistência (add/commit/delete/query) não mora mais aqui: isso é
    # responsabilidade do UsuarioRepository. Este método só decide QUAIS
    # campos mudam — quem salva a mudança é sempre o repository.
    def atualizar(self, nome=None, email=None, senha=None, foto_url=None, is_admin=None):
        """Altera em memória apenas os campos informados (não commita)."""
        if nome is not None:
            self.nome = nome
        if email is not None:
            self.email = email
        if senha:
            self.definir_senha(senha)
        if foto_url is not None:
            self.foto_url = foto_url
        if is_admin is not None:
            self.is_admin = is_admin

    def to_dict(self):
        """Converte o objeto Usuario para dicionário/JSON (nunca inclui a senha)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "foto_url": self.foto_url,
            "is_admin": self.is_admin,
        }
