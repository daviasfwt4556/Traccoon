from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from auth_utils import admin_obrigatorio
from models import db
from services.materiais.create_material_service import CadastrarMaterialService
from services.materiais.read_material_service import (
    BuscarMaterialPorIdService,
    ListarMateriaisPorCategoriaService,
    ListarMateriaisService,
)
from services.materiais.update_material_service import EditarMaterialService
from services.materiais.delete_material_service import DeletarMaterialService

material_bp = Blueprint("material", __name__, url_prefix="/materiais")


@material_bp.get("/")
def listar():
    categoria_id = request.args.get("categoria_id")

    if categoria_id:
        service = ListarMateriaisPorCategoriaService()
        materiais = service.executar(categoria_id)
    else:
        pagina = request.args.get("pagina", type=int)
        por_pagina = request.args.get("por_pagina", type=int)
        service = ListarMateriaisService()
        materiais = service.executar(pagina, por_pagina)

    return jsonify(materiais), 200


@material_bp.get("/<int:id>")
def buscar(id):
    service = BuscarMaterialPorIdService()
    material = service.executar(id)

    if material is None:
        return jsonify({"erro": "Material não encontrado."}), 404

    return jsonify(material), 200


@material_bp.post("/")
@admin_obrigatorio
def cadastrar():
    try:
        dados = request.get_json() or {}
        service = CadastrarMaterialService()
        material = service.executar(
            dados.get("categoria_id"), dados.get("conteudo"), dados.get("url")
        )
        return jsonify(material), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar material no banco de dados."}), 500


@material_bp.put("/<int:id>")
@admin_obrigatorio
def editar(id):
    try:
        dados = request.get_json() or {}
        service = EditarMaterialService()
        material = service.executar(id, dados.get("conteudo"), dados.get("url"))
        return jsonify(material), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar material no banco de dados."}), 500


@material_bp.delete("/<int:id>")
@admin_obrigatorio
def deletar(id):
    try:
        service = DeletarMaterialService()
        service.executar(id)
        return "", 204

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar material no banco de dados."}), 500
