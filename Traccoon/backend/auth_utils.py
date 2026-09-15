"""
Autenticação baseada em token assinado (sem sessão/cookie).

Motivo de não usar `session` do Flask (como no exemplo de referência):
o front-end roda em uma origem separada do back-end (Live Server em uma
porta, API em outra), e cookies entre origens diferentes em localhost
são inconsistentes entre navegadores. Um token no cabeçalho Authorization
evita esse problema e funciona igual em qualquer navegador/porta.

A parte de hash de senha continua idêntica à referência (werkzeug.security).
"""

from functools import wraps

from flask import jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

# Em um projeto real, isso viria de uma variável de ambiente.
CHAVE_SECRETA = "autotrans-chave-secreta-dev"
TOKEN_VALIDADE_SEGUNDOS = 60 * 60 * 24 * 7  # 7 dias

_serializer = URLSafeTimedSerializer(CHAVE_SECRETA)


def gerar_token(usuario_id):
    """Cria um token assinado contendo o id do usuário."""
    return _serializer.dumps({"usuario_id": usuario_id})


def obter_usuario_id_do_token():
    """
    Lê o cabeçalho 'Authorization: Bearer <token>' da requisição e devolve
    o usuario_id contido nele, ou None se o token não existir/for inválido/expirado.
    """
    cabecalho = request.headers.get("Authorization", "")
    if not cabecalho.startswith("Bearer "):
        return None

    token = cabecalho[len("Bearer "):]
    try:
        dados = _serializer.loads(token, max_age=TOKEN_VALIDADE_SEGUNDOS)
    except (BadSignature, SignatureExpired):
        return None

    return dados.get("usuario_id")


def login_obrigatorio(funcao_view):
    """
    Decorator que protege uma rota: só executa a view se houver um token
    válido no cabeçalho Authorization. Disponibiliza o id do usuário logado
    em request.usuario_id para a view usar.
    """

    @wraps(funcao_view)
    def wrapper(*args, **kwargs):
        usuario_id = obter_usuario_id_do_token()
        if usuario_id is None:
            return jsonify({"erro": "Autenticação necessária. Faça login novamente."}), 401

        request.usuario_id = usuario_id
        return funcao_view(*args, **kwargs)

    return wrapper


def admin_obrigatorio(funcao_view):
    """
    Decorator que protege rotas administrativas (gestão de usuários,
    categorias, questões, alternativas e materiais): exige token válido
    E que o usuário logado tenha is_admin = True. Sem isso, qualquer aluno
    logado poderia alterar o banco de questões ou os dados de outro aluno.
    """

    @wraps(funcao_view)
    def wrapper(*args, **kwargs):
        # Import local para evitar import circular (models/repositories -> app -> controllers).
        from repositories.usuario_repository import UsuarioRepository

        usuario_id = obter_usuario_id_do_token()
        if usuario_id is None:
            return jsonify({"erro": "Autenticação necessária. Faça login novamente."}), 401

        usuario = UsuarioRepository().buscar_por_id(usuario_id)
        if usuario is None or not usuario.is_admin:
            return jsonify({"erro": "Apenas administradores podem realizar esta ação."}), 403

        request.usuario_id = usuario_id
        return funcao_view(*args, **kwargs)

    return wrapper
