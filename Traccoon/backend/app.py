import os

from flask import Flask, jsonify
from flask_cors import CORS

from controllers import (
    alternativa_bp,
    auth_bp,
    categoria_bp,
    material_bp,
    questao_bp,
    simulado_bp,
    usuario_bp,
)
from models import db


def criar_app(config_teste=None):
    """
    config_teste: dicionário opcional pra sobrescrever configurações do
    Flask (usado pelos testes automatizados em tests/, que rodam a API
    inteira contra um banco SQLite em memória, sem tocar no
    autotrans.db de verdade).
    """
    pasta = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__)
    CORS(app)  # libera o acesso da API para o frontend estático (outra origem/porta)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "autotrans.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if config_teste:
        app.config.update(config_teste)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(material_bp)
    app.register_blueprint(questao_bp)
    app.register_blueprint(alternativa_bp)
    app.register_blueprint(simulado_bp)

    @app.get("/")
    def home():
        return jsonify({
            "mensagem": "API do AutoTrans (Flask + SQLAlchemy) funcionando.",
            "rotas": {
                "registro": "POST /auth/registro (nome, email, senha)",
                "login": "POST /auth/login (email, senha)",
                "logout": "POST /auth/logout",
                "usuario_logado": "GET /auth/me (requer token)",
                "usuarios": "/usuarios",
                "categorias": "/categorias",
                "materiais": "/materiais?categoria_id=<id>",
                "questoes": "/questoes?categoria_id=<id>",
                "alternativas": "/alternativas?questao_id=<id>",
                "iniciar_simulado": "POST /simulados (categoria_id) - requer token",
                "buscar_simulado": "GET /simulados/<id> - requer token",
                "finalizar_simulado": "POST /simulados/<id>/finalizar (respostas) - requer token",
            },
        })

    with app.app_context():
        db.create_all()

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
