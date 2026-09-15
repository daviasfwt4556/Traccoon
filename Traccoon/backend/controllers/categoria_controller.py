from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from auth_utils import admin_obrigatorio
from models import db
from services.categorias.create_categoria_service import CadastrarCategoriaService
from services.categorias.read_categoria_service import (
    BuscarCategoriaPorIdService,
    ListarCategoriasService,
)
from services.categorias.update_categoria_service import EditarCategoriaService
from services.categorias.delete_categoria_service import DeletarCategoriaService

categoria_bp = Blueprint("categoria", __name__, url_prefix="/categorias")

# Listar/buscar categorias continua público (todo aluno precisa ver as
# trilhas). Só cadastrar/editar/apagar exige administrador.


@categoria_bp.get("/")
def listar():
    pagina = request.args.get("pagina", type=int)
    por_pagina = request.args.get("por_pagina", type=int)

    service = ListarCategoriasService()
    categorias = service.executar(pagina, por_pagina)
    return jsonify(categorias), 200


@categoria_bp.get("/<int:id>")
def buscar(id):
    service = BuscarCategoriaPorIdService()
    categoria = service.executar(id)

    if categoria is None:
        return jsonify({"erro": "Categoria não encontrada."}), 404

    return jsonify(categoria), 200


@categoria_bp.post("/")
@admin_obrigatorio
def cadastrar():
    try:
        dados = request.get_json() or {}
        service = CadastrarCategoriaService()
        categoria = service.executar(dados.get("nome"), dados.get("descricao"))
        return jsonify(categoria), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar categoria no banco de dados."}), 500


@categoria_bp.put("/<int:id>")
@admin_obrigatorio
def editar(id):
    try:
        dados = request.get_json() or {}
        service = EditarCategoriaService()
        categoria = service.executar(id, dados.get("nome"), dados.get("descricao"))
        return jsonify(categoria), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar categoria no banco de dados."}), 500


@categoria_bp.delete("/<int:id>")
@admin_obrigatorio
def deletar(id):
    try:
        service = DeletarCategoriaService()
        service.executar(id)
        return "", 204

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar categoria no banco de dados."}), 500
