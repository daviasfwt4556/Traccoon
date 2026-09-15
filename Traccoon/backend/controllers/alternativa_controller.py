from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from auth_utils import admin_obrigatorio
from models import db
from services.alternativas.create_alternativa_service import CadastrarAlternativaService
from services.alternativas.read_alternativa_service import (
    BuscarAlternativaPorIdService,
    ListarAlternativasPorQuestaoService,
    ListarAlternativasService,
)
from services.alternativas.update_alternativa_service import EditarAlternativaService
from services.alternativas.delete_alternativa_service import DeletarAlternativaService

alternativa_bp = Blueprint("alternativa", __name__, url_prefix="/alternativas")


@alternativa_bp.get("/")
def listar():
    questao_id = request.args.get("questao_id")

    if questao_id:
        service = ListarAlternativasPorQuestaoService()
        alternativas = service.executar(questao_id)
    else:
        pagina = request.args.get("pagina", type=int)
        por_pagina = request.args.get("por_pagina", type=int)
        service = ListarAlternativasService()
        alternativas = service.executar(pagina, por_pagina)

    return jsonify(alternativas), 200


@alternativa_bp.get("/<int:id>")
def buscar(id):
    service = BuscarAlternativaPorIdService()
    alternativa = service.executar(id)

    if alternativa is None:
        return jsonify({"erro": "Alternativa não encontrada."}), 404

    return jsonify(alternativa), 200


@alternativa_bp.post("/")
@admin_obrigatorio
def cadastrar():
    try:
        dados = request.get_json() or {}
        service = CadastrarAlternativaService()
        alternativa = service.executar(
            dados.get("questao_id"), dados.get("texto"), dados.get("correta", False)
        )
        return jsonify(alternativa), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar alternativa no banco de dados."}), 500


@alternativa_bp.put("/<int:id>")
@admin_obrigatorio
def editar(id):
    try:
        dados = request.get_json() or {}
        service = EditarAlternativaService()
        alternativa = service.executar(id, dados.get("texto"), dados.get("correta"))
        return jsonify(alternativa), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar alternativa no banco de dados."}), 500


@alternativa_bp.delete("/<int:id>")
@admin_obrigatorio
def deletar(id):
    try:
        service = DeletarAlternativaService()
        service.executar(id)
        return "", 204

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar alternativa no banco de dados."}), 500
