from .auth_controller import auth_bp
from .simulado_controller import simulado_bp
from .usuario_controller import usuario_bp
from .categoria_controller import categoria_bp
from .material_controller import material_bp
from .questao_controller import questao_bp
from .alternativa_controller import alternativa_bp

__all__ = [
    "auth_bp",
    "simulado_bp",
    "usuario_bp",
    "categoria_bp",
    "material_bp",
    "questao_bp",
    "alternativa_bp",
]
