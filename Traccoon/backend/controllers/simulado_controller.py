from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from auth_utils import login_obrigatorio
from models import db
from services.simulados.iniciar_simulado_service import IniciarSimuladoService
from services.simulados.buscar_simulado_service import BuscarSimuladoService
from services.simulados.finalizar_simulado_service import FinalizarSimuladoService
from services.simulados.consultar_historico_service import ConsultarHistoricoSimuladosService

simulado_bp = Blueprint("simulado", __name__, url_prefix="/simulados")


@simulado_bp.get("/historico")
@login_obrigatorio
def historico():
    """
    Lista os simulados já finalizados do usuário logado, com estatísticas
    (média, melhor e pior nota). A consulta complexa (join Simulado+Resultado)
    fica no Repository — este controller só chama o Service.
    """
    service = ConsultarHistoricoSimuladosService()
    resultado = service.executar(request.usuario_id)
    return jsonify(resultado), 200


@simulado_bp.get("/<int:id>")
@login_obrigatorio
def buscar(id):
    try:
        service = BuscarSimuladoService()
        simulado = service.executar(id, request.usuario_id)

        if simulado is None:
            return jsonify({"erro": "Simulado não encontrado."}), 404

        return jsonify(simulado), 200

    except PermissionError as erro:
        return jsonify({"erro": str(erro)}), 403


@simulado_bp.post("/")
@login_obrigatorio
def iniciar():
    try:
        dados = request.get_json() or {}
        service = IniciarSimuladoService()
        # usuario_id vem do token (usuário logado), nunca do corpo da requisição —
        # assim ninguém consegue criar um simulado "em nome" de outra pessoa.
        simulado = service.executar(request.usuario_id, dados.get("categoria_id"))
        return jsonify(simulado), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao criar simulado no banco de dados."}), 500


@simulado_bp.post("/<int:id>/finalizar")
@login_obrigatorio
def finalizar(id):
    try:
        dados = request.get_json() or {}
        service = FinalizarSimuladoService()
        simulado = service.executar(id, dados.get("respostas", []), request.usuario_id)
        return jsonify(simulado), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except PermissionError as erro:
        return jsonify({"erro": str(erro)}), 403

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao finalizar simulado no banco de dados."}), 500
