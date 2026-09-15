from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from auth_utils import admin_obrigatorio
from models import db
from services.usuario.create_usuario_service import CadastrarUsuarioService
from services.usuario.read_usuarios_service import (
    BuscarUsuarioPorIdService,
    ListarUsuariosService,
)
from services.usuario.update_usuario_serivce import EditarUsuarioService
from services.usuario.delete_usuario_service import DeletarUsuarioService

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")

# Todas as rotas abaixo são de gestão de OUTROS usuários (não do próprio
# usuário logado) — por isso exigem administrador. Para o aluno editar ou
# apagar a própria conta, use PUT/DELETE /auth/me (nunca essas rotas).


@usuario_bp.get("/")
@admin_obrigatorio
def listar():
    pagina = request.args.get("pagina", type=int)
    por_pagina = request.args.get("por_pagina", type=int)

    service = ListarUsuariosService()
    usuarios = service.executar(pagina, por_pagina)
    return jsonify(usuarios), 200


@usuario_bp.get("/<int:id>")
@admin_obrigatorio
def buscar(id):
    service = BuscarUsuarioPorIdService()
    usuario = service.executar(id)

    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    return jsonify(usuario), 200


@usuario_bp.post("/")
@admin_obrigatorio
def cadastrar():
    try:
        dados = request.get_json() or {}
        service = CadastrarUsuarioService()
        usuario = service.executar(
            dados.get("nome"), dados.get("email"), dados.get("senha"), dados.get("is_admin", False)
        )
        return jsonify(usuario), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao salvar usuário no banco de dados."}), 500


@usuario_bp.put("/<int:id>")
@admin_obrigatorio
def editar(id):
    try:
        dados = request.get_json() or {}
        service = EditarUsuarioService()
        usuario = service.executar(
            id,
            dados.get("nome"),
            dados.get("email"),
            dados.get("senha"),
            dados.get("foto_url"),
            dados.get("is_admin"),
        )
        return jsonify(usuario), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar usuário no banco de dados."}), 500


@usuario_bp.delete("/<int:id>")
@admin_obrigatorio
def deletar(id):
    try:
        service = DeletarUsuarioService()
        service.executar(id)
        return "", 204

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar usuário no banco de dados."}), 500
