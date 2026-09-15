"""
Fixtures compartilhadas por todos os testes.

Cada teste roda contra um banco SQLite em memória (criado do zero e
descartado ao final de cada teste), então os testes nunca leem nem
escrevem no autotrans.db de verdade e podem ser rodados quantas vezes
quiser, em qualquer ordem, sem "sujar" dados de um teste no outro.
"""

import os
import sys

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import pytest

from app import criar_app
from models import db as _db


@pytest.fixture()
def app():
    """Cria uma instância da aplicação Flask com banco em memória."""
    aplicativo = criar_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "TESTING": True,
    })
    yield aplicativo


@pytest.fixture()
def app_context(app):
    """Empurra o contexto da aplicação, necessário pra services/repositories
    acessarem o banco (eles usam db.session por baixo do Flask-SQLAlchemy)."""
    with app.app_context():
        yield app
        _db.session.remove()


@pytest.fixture()
def client(app):
    """Cliente de teste, para os testes que exercitam a API HTTP inteira
    (rotas + controllers), não só a regra de negócio isolada de um service."""
    return app.test_client()
