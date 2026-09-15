from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from auth_utils import admin_obrigatorio
from models import db
from services.questoes.create_questao_service import CadastrarQuestaoService
from services.questoes.read_questao_service import (
    BuscarQuestaoPorIdService,
    ListarQuestoesPorCategoriaService,
    ListarQuestoesService,
)
from services.questoes.update_questao_service import EditarQuestaoService
from services.questoes.delete_questao_service import DeletarQuestaoService

questao_bp = Blueprint("questao", __name__, url_prefix="/questoes")


@questao_bp.get("/")
def listar():
    categoria_id = request.args.get("categoria_id")

    if categoria_id:
        service = ListarQuestoesPorCategoriaService()
        questoes = service.executar(categoria_id)
    else:
        pagina = request.args.get("pagina", type=int)
        por_pagina = request.args.get("por_pagina", type=int)
        service = ListarQuestoesService()
        questoes = service.executar(pagina, por_pagina)

    return jsonify(questoes), 200


@questao_bp.get("/<int:id>")
def buscar(id):
    service = BuscarQuestaoPorIdService()
    questao = service.executar(id)

    if questao is None:
        return jsonify({"erro": "Questão não encontrada."}), 404

    return jsonify(questao), 200


@questao_bp.post("/")
@admin_obrigatorio
def cadastrar():
    try:
        dados = request.get_json() or {}
        service = CadastrarQuestaoService()
        questao = service.executar(dados.get("enunciado"), dados.get("categoria_id"))
        return jsonify(questao), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar questão no banco de dados."}), 500


@questao_bp.put("/<int:id>")
@admin_obrigatorio
def editar(id):
    try:
        dados = request.get_json() or {}
        service = EditarQuestaoService()
        questao = service.executar(id, dados.get("enunciado"), dados.get("categoria_id"))
        return jsonify(questao), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar questão no banco de dados."}), 500


@questao_bp.delete("/<int:id>")
@admin_obrigatorio
def deletar(id):
    try:
        service = DeletarQuestaoService()
        service.executar(id)
        return "", 204

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar questão no banco de dados."}), 500
