"""
Repository: usado aqui exatamente pelo motivo que o enunciado pede — uma
consulta especial (junta Simulado com Resultado, filtra por usuário,
ordena por data e calcula estatísticas), diferente do CRUD simples que já
mora nas Models.

Controller e Service nunca escrevem SQL/consulta direto: só chamam este
Repository.
"""

from statistics import mean

from models import Resultado, Simulado, db


class HistoricoSimuladoRepository:
    def buscar_por_usuario(self, usuario_id):
        """
        Consulta complexa: junta Simulado + Resultado, filtra pelo usuário
        logado e ordena do mais recente para o mais antigo.
        """
        return (
            db.session.query(Simulado)
            .join(Resultado, Resultado.simulado_id == Simulado.id)
            .filter(Simulado.usuario_id == usuario_id)
            .order_by(Simulado.data_realizacao.desc())
            .all()
        )

    def calcular_estatisticas(self, simulados):
        """
        Recebe a lista de Simulados já com resultado e calcula
        média, melhor e pior nota — outro tipo de operação que o
        enunciado cita como exemplo de uso do Repository (relatório).
        """
        notas = [s.resultado.nota for s in simulados if s.resultado]

        if not notas:
            return {"media": 0, "melhor": 0, "pior": 0, "total_simulados": 0}

        return {
            "media": round(mean(notas), 1),
            "melhor": max(notas),
            "pior": min(notas),
            "total_simulados": len(notas),
        }
