from datetime import datetime

from . import db
from .base import ModeloBase


class Resultado(ModeloBase):
    __tablename__ = "resultados"

    simulado_id = db.Column(db.Integer, db.ForeignKey("simulados.id"), nullable=False)
    nota = db.Column(db.Float, nullable=False, default=0.0)
    data_resultado = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # ---------- CRUD (Active Record) ----------
    def salvar(self):
        """CREATE: salva um novo resultado no banco."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def buscar_por_simulado(simulado_id):
        """READ: busca o resultado de um simulado específico."""
        return Resultado.query.filter_by(simulado_id=simulado_id).first()

    def aprovado(self, pontuacao_max):
        """Aprovado = nota igual ou maior que 70% da pontuação máxima."""
        return self.nota >= pontuacao_max * 0.7

    def to_dict(self):
        """Converte o objeto Resultado para dicionário/JSON."""
        return {
            "id": self.id,
            "simulado_id": self.simulado_id,
            "nota": self.nota,
            "data_resultado": self.data_resultado.isoformat(),
        }
