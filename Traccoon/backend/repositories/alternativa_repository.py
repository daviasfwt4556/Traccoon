"""
Repository de Alternativa: concentra toda consulta e persistência desta
entidade. Ver o comentário em usuario_repository.py sobre o motivo dessa
camada existir mesmo para CRUD simples.
"""

from models import Alternativa, db


class AlternativaRepository:
    def listar_todos(self):
        return Alternativa.query.order_by(Alternativa.id.asc()).all()

    def listar_paginado(self, pagina, por_pagina):
        return Alternativa.query.order_by(Alternativa.id.asc()).paginate(
            page=pagina, per_page=por_pagina, error_out=False
        )

    def buscar_por_id(self, id):
        return Alternativa.query.get(id)

    def listar_por_questao(self, questao_id):
        """Usado ao montar/corrigir um simulado, sem paginação."""
        return Alternativa.query.filter_by(questao_id=questao_id).all()

    def criar(self, alternativa):
        db.session.add(alternativa)
        db.session.commit()
        return alternativa

    def salvar_alteracoes(self):
        db.session.commit()

    def deletar(self, alternativa):
        db.session.delete(alternativa)
        db.session.commit()
