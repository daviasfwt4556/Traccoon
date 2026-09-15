from models import ItemSimulado, Resultado, Simulado


class FinalizarSimuladoService:
    def executar(self, simulado_id, respostas, usuario_id_logado):
        """
        respostas: lista de dicts [{"item_id": 1, "alternativa_id": 5}, ...]
        """
        simulado = Simulado.buscar_por_id(simulado_id)
        if simulado is None:
            raise ValueError("Simulado não encontrado.")

        if simulado.usuario_id != usuario_id_logado:
            raise PermissionError("Você não tem permissão para finalizar este simulado.")

        respostas_por_item = {r["item_id"]: r.get("alternativa_id") for r in respostas}

        for item in simulado.itens:
            alternativa_id = respostas_por_item.get(item.id)
            if alternativa_id:
                item.alternativa_escolhida_id = alternativa_id
            item.verificar()

        nota = simulado.calcular_pontuacao()
        resultado = Resultado(simulado_id=simulado.id, nota=nota)
        resultado.salvar()

        return simulado.to_dict()
