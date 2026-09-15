from . import db
from .base import ModeloBase


class Alternativa(ModeloBase):
    __tablename__ = "alternativas"

    questao_id = db.Column(db.Integer, db.ForeignKey("questoes.id"), nullable=False)
    texto = db.Column(db.String(255), nullable=False)
    correta = db.Column(db.Boolean, nullable=False, default=False)

    questao = db.relationship("Questao", back_populates="alternativas")

    # ---------- Regras de campo (sem tocar no banco) ----------
    # Persistência mora no AlternativaRepository; este método só decide
    # quais campos mudam em memória.
    def atualizar(self, texto=None, correta=None, questao_id=None):
        """Altera em memória apenas os campos informados (não commita)."""
        if texto is not None:
            self.texto = texto
        if correta is not None:
            self.correta = correta
        if questao_id is not None:
            self.questao_id = questao_id

    def to_dict(self):
        """Converte o objeto Alternativa para dicionário/JSON."""
        return {
            "id": self.id,
            "questao_id": self.questao_id,
            "texto": self.texto,
            "correta": self.correta,
        }
