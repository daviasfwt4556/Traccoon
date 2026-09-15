from repositories.historico_simulado_repository import HistoricoSimuladoRepository


class ConsultarHistoricoSimuladosService:
    def __init__(self):
        self.repository = HistoricoSimuladoRepository()

    def executar(self, usuario_id):
        simulados = self.repository.buscar_por_usuario(usuario_id)
        estatisticas = self.repository.calcular_estatisticas(simulados)

        return {
            "estatisticas": estatisticas,
            "simulados": [s.to_dict(incluir_itens=False) for s in simulados],
        }
