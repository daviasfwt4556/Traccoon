from models import ItemSimulado, Simulado
from repositories.categoria_repository import CategoriaRepository
from repositories.usuario_repository import UsuarioRepository


class IniciarSimuladoService:
    def __init__(self):
        self.repository_usuario = UsuarioRepository()
        self.repository_categoria = CategoriaRepository()

    def executar(self, usuario_id, categoria_id):
        usuario = self.repository_usuario.buscar_por_id(usuario_id)
        if usuario is None:
            raise ValueError("Usuário não encontrado.")

        categoria = self.repository_categoria.buscar_por_id(categoria_id)
        if categoria is None:
            raise ValueError("Categoria não encontrada.")

        if not categoria.questoes:
            raise ValueError("Esta categoria ainda não tem questões cadastradas.")

        simulado = Simulado(
            usuario_id=usuario.id,
            categoria_id=categoria.id,
            titulo=f"Simulado - {categoria.nome}",
        )
        simulado.salvar()

        for questao in categoria.questoes:
            item = ItemSimulado(simulado_id=simulado.id, questao_id=questao.id)
            item.salvar()

        return simulado.to_dict()
