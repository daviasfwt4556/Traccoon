from . import db
from .base import ModeloBase


class ItemSimulado(ModeloBase):
    """Cada questão de um Simulado, junto com a resposta marcada pelo usuário."""

    __tablename__ = "itens_simulado"

    simulado_id = db.Column(db.Integer, db.ForeignKey("simulados.id"), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey("questoes.id"), nullable=False)
    alternativa_escolhida_id = db.Column(db.Integer, db.ForeignKey("alternativas.id"))
    acerto = db.Column(db.Boolean, nullable=False, default=False)

    simulado = db.relationship("Simulado", back_populates="itens")
    questao = db.relationship("Questao")
    alternativa_escolhida = db.relationship("Alternativa")

    # ---------- CRUD (Active Record) ----------
    def salvar(self):
        """CREATE: salva um novo item de simulado no banco."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id):
        """READ: busca um item de simulado pelo id."""
        return ItemSimulado.query.get(id)

    # ---------- Regra própria do item ----------
    def verificar(self):
        """Compara a alternativa escolhida com a alternativa correta da questão."""
        correta = self.questao.alternativa_correta()
        self.acerto = bool(correta and self.alternativa_escolhida_id == correta.id)
        db.session.commit()
        return self.acerto

    def to_dict(self):
        """Converte o objeto ItemSimulado para dicionário/JSON."""
        return {
            "id": self.id,
            "simulado_id": self.simulado_id,
            "questao": self.questao.to_dict() if self.questao else None,
            "alternativa_escolhida_id": self.alternativa_escolhida_id,
            "alternativa_escolhida_texto": (
                self.alternativa_escolhida.texto if self.alternativa_escolhida else None
            ),
            "acerto": self.acerto,
        }
