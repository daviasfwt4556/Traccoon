"""
Repository de Material: concentra toda consulta e persistência desta
entidade. Ver o comentário em usuario_repository.py sobre o motivo dessa
camada existir mesmo para CRUD simples.
"""

from models import Material, db


class MaterialRepository:
    def listar_todos(self):
        return Material.query.order_by(Material.id.asc()).all()

    def listar_paginado(self, pagina, por_pagina):
        return Material.query.order_by(Material.id.asc()).paginate(
            page=pagina, per_page=por_pagina, error_out=False
        )

    def buscar_por_id(self, id):
        return Material.query.get(id)

    def listar_por_categoria(self, categoria_id):
        """Usado pela tela de estudo (materiais de uma trilha), sem paginação."""
        return Material.query.filter_by(categoria_id=categoria_id).all()

    def criar(self, material):
        db.session.add(material)
        db.session.commit()
        return material

    def salvar_alteracoes(self):
        db.session.commit()

    def deletar(self, material):
        db.session.delete(material)
        db.session.commit()
