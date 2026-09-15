from models import Simulado


class BuscarSimuladoService:
    def executar(self, simulado_id, usuario_id_logado):
        simulado = Simulado.buscar_por_id(simulado_id)
        if simulado is None:
            return None

        if simulado.usuario_id != usuario_id_logado:
            raise PermissionError("Você não tem permissão para ver este simulado.")

        return simulado.to_dict()
