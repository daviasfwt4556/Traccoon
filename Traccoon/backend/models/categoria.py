from . import db
from .base import ModeloBase


class Categoria(ModeloBase):
    __tablename__ = "categorias"

    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))

    questoes = db.relationship("Questao", back_populates="categoria")
    materiais = db.relationship("Material", back_populates="categoria")

    # ---------- Regras de campo (sem tocar no banco) ----------
    # Persistência mora no CategoriaRepository; este método só decide
    # quais campos mudam em memória.
    def atualizar(self, nome=None, descricao=None):
        """Altera em memória apenas os campos informados (não commita)."""
        if nome is not None:
            self.nome = nome
        if descricao is not None:
            self.descricao = descricao

    def to_dict(self):
        """Converte o objeto Categoria para dicionário/JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "total_questoes": len(self.questoes),
        }
