from . import db
from .base import ModeloBase


class Questao(ModeloBase):
    __tablename__ = "questoes"

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    enunciado = db.Column(db.Text, nullable=False)

    categoria = db.relationship("Categoria", back_populates="questoes")
    alternativas = db.relationship("Alternativa", back_populates="questao")

    # ---------- Regras de campo (sem tocar no banco) ----------
    # Persistência (incluindo a exclusão em cascata das alternativas) mora
    # no QuestaoRepository; este método só decide quais campos mudam.
    def atualizar(self, enunciado=None, categoria_id=None):
        """Altera em memória apenas os campos informados (não commita)."""
        if enunciado is not None:
            self.enunciado = enunciado
        if categoria_id is not None:
            self.categoria_id = categoria_id

    def alternativa_correta(self):
        for alternativa in self.alternativas:
            if alternativa.correta:
                return alternativa
        return None

    def to_dict(self, incluir_alternativas=True):
        """Converte o objeto Questao para dicionário/JSON."""
        dados = {
            "id": self.id,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
            "enunciado": self.enunciado,
        }
        if incluir_alternativas:
            dados["alternativas"] = [a.to_dict() for a in self.alternativas]
        return dados
