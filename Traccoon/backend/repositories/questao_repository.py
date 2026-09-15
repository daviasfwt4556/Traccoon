"""
Repository de Questao: concentra toda consulta e persistência desta
entidade, incluindo a exclusão em cascata das alternativas (antes isso
ficava dentro de Questao.deletar(), no Model — mover pra cá é o que
completa o padrão Repository pedido: nenhuma orquestração de banco fica
no Model nem no Service, só aqui).
"""

from models import Questao, db


class QuestaoRepository:
    def listar_todos(self):
        return Questao.query.order_by(Questao.id.asc()).all()

    def listar_paginado(self, pagina, por_pagina):
        return Questao.query.order_by(Questao.id.asc()).paginate(
            page=pagina, per_page=por_pagina, error_out=False
        )

    def buscar_por_id(self, id):
        return Questao.query.get(id)

    def listar_por_categoria(self, categoria_id):
        """Usado ao montar um simulado (todas as questões da trilha), sem paginação."""
        return Questao.query.filter_by(categoria_id=categoria_id).all()

    def criar(self, questao):
        db.session.add(questao)
        db.session.commit()
        return questao

    def salvar_alteracoes(self):
        db.session.commit()

    def deletar(self, questao):
        """DELETE: remove a questão e suas alternativas (cascata manual)."""
        for alternativa in list(questao.alternativas):
            db.session.delete(alternativa)
        db.session.delete(questao)
        db.session.commit()
