from . import db
from .base import ModeloBase


class Material(ModeloBase):
    __tablename__ = "materiais"

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255))

    categoria = db.relationship("Categoria", back_populates="materiais")

    # ---------- Regras de campo (sem tocar no banco) ----------
    # Persistência mora no MaterialRepository; este método só decide
    # quais campos mudam em memória.
    def atualizar(self, conteudo=None, url=None, categoria_id=None):
        """Altera em memória apenas os campos informados (não commita)."""
        if conteudo is not None:
            self.conteudo = conteudo
        if url is not None:
            self.url = url
        if categoria_id is not None:
            self.categoria_id = categoria_id

    def to_dict(self):
        """Converte o objeto Material para dicionário/JSON."""
        return {
            "id": self.id,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "conteudo": self.conteudo,
            "url": self.url,
        }
