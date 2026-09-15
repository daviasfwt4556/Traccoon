"""
Repository de Categoria: concentra toda consulta e persistência desta
entidade. Ver o comentário em usuario_repository.py sobre o motivo dessa
camada existir mesmo para CRUD simples.
"""

from models import Categoria, db


class CategoriaRepository:
    def listar_todos(self):
        return Categoria.query.order_by(Categoria.nome.asc()).all()

    def listar_paginado(self, pagina, por_pagina):
        return Categoria.query.order_by(Categoria.nome.asc()).paginate(
            page=pagina, per_page=por_pagina, error_out=False
        )

    def buscar_por_id(self, id):
        return Categoria.query.get(id)

    def criar(self, categoria):
        db.session.add(categoria)
        db.session.commit()
        return categoria

    def salvar_alteracoes(self):
        db.session.commit()

    def deletar(self, categoria):
        db.session.delete(categoria)
        db.session.commit()
