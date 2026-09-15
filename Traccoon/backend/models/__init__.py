from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .usuario import Usuario
from .categoria import Categoria
from .material import Material
from .questao import Questao
from .alternativa import Alternativa
from .simulado import Simulado
from .item_simulado import ItemSimulado
from .resultado import Resultado

__all__ = [
    "db",
    "ModeloBase",
    "Usuario",
    "Categoria",
    "Material",
    "Questao",
    "Alternativa",
    "Simulado",
    "ItemSimulado",
    "Resultado",
]
