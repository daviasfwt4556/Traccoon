from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from auth_utils import gerar_token, login_obrigatorio
from models import db
from repositories.usuario_repository import UsuarioRepository
from services.auth.login_service import LoginService
from services.auth.registrar_usuario_service import RegistrarUsuarioService
from services.usuario.update_usuario_serivce import EditarUsuarioService
from services.usuario.delete_usuario_service import DeletarUsuarioService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/registro")
def registro():
    try:
        dados = request.get_json() or {}
        service = RegistrarUsuarioService()
        usuario = service.executar(dados.get("nome"), dados.get("email"), dados.get("senha"))

        token = gerar_token(usuario.id)
        return jsonify({"token": token, "usuario": usuario.to_dict()}), 201

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao cadastrar usuário no banco de dados."}), 500


@auth_bp.post("/login")
def login():
    try:
        dados = request.get_json() or {}
        service = LoginService()
        usuario = service.executar(dados.get("email"), dados.get("senha"))

        token = gerar_token(usuario.id)
        return jsonify({"token": token, "usuario": usuario.to_dict()}), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 401


@auth_bp.post("/logout")
def logout():
    """
    Como a autenticação é via token (sem sessão no servidor), não há nada
    para invalidar aqui — o front-end simplesmente descarta o token salvo.
    A rota existe só para manter a simetria da API.
    """
    return "", 204


@auth_bp.get("/me")
@login_obrigatorio
def me():
    usuario = UsuarioRepository().buscar_por_id(request.usuario_id)
    if usuario is None:
        return jsonify({"erro": "Usuário não encontrado."}), 404
    return jsonify(usuario.to_dict()), 200


@auth_bp.put("/me")
@login_obrigatorio
def editar_me():
    """
    Edita os dados do PRÓPRIO usuário logado. O id vem sempre do token
    (request.usuario_id), nunca de um parâmetro na URL ou no corpo —
    assim ninguém consegue editar a conta de outra pessoa por essa rota,
    mesmo manipulando a requisição diretamente.
    """
    try:
        dados = request.get_json() or {}
        service = EditarUsuarioService()
        # is_admin nunca vem daqui: ninguém se autopromove a administrador
        # editando o próprio perfil.
        usuario = service.executar(
            request.usuario_id,
            dados.get("nome"),
            dados.get("email"),
            dados.get("senha"),
            dados.get("foto_url"),
        )
        return jsonify(usuario), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar seus dados no banco de dados."}), 500


@auth_bp.delete("/me")
@login_obrigatorio
def excluir_me():
    """
    Exclui a PRÓPRIA conta do usuário logado. Assim como em editar_me,
    o id vem sempre do token — ninguém consegue apagar a conta de outra
    pessoa por essa rota.
    """
    try:
        service = DeletarUsuarioService()
        service.executar(request.usuario_id)
        return "", 204

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"erro": "Erro ao excluir sua conta no banco de dados."}), 500
