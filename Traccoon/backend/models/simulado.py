from datetime import datetime

from . import db
from .base import ModeloBase


class Simulado(ModeloBase):
    __tablename__ = "simulados"

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    pontuacao_max = db.Column(db.Float, nullable=False, default=100.0)
    data_realizacao = db.Column(db.DateTime, default=datetime.now, nullable=False)

    usuario = db.relationship("Usuario", back_populates="simulados")
    categoria = db.relationship("Categoria")
    itens = db.relationship("ItemSimulado", back_populates="simulado")
    resultado = db.relationship("Resultado", uselist=False)

    # ---------- CRUD (Active Record) ----------
    def salvar(self):
        """CREATE: salva um novo simulado no banco."""
        db.session.add(self)
        db.session.commit()

    def deletar(self):
        """DELETE: remove o simulado (e seus itens) do banco."""
        for item in list(self.itens):
            db.session.delete(item)
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id):
        """READ: busca um simulado pelo id."""
        return Simulado.query.get(id)

    # ---------- Regras próprias do simulado ----------
    def calcular_pontuacao(self):
        total = len(self.itens)
        if total == 0:
            return 0.0
        acertos = sum(1 for item in self.itens if item.acerto)
        return round((acertos / total) * self.pontuacao_max, 1)

    def to_dict(self, incluir_itens=True):
        """Converte o objeto Simulado para dicionário/JSON."""
        dados = {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "categoria_id": self.categoria_id,
            "titulo": self.titulo,
            "pontuacao_max": self.pontuacao_max,
            "data_realizacao": self.data_realizacao.isoformat(),
            "resultado": self.resultado.to_dict() if self.resultado else None,
        }
        if incluir_itens:
            dados["itens"] = [item.to_dict() for item in self.itens]
        return dados
