from repositories.alternativa_repository import AlternativaRepository


class EditarAlternativaService:
    def __init__(self):
        self.repository = AlternativaRepository()

    def executar(self, alternativa_id, texto, correta):
        alternativa = self.repository.buscar_por_id(alternativa_id)
        if alternativa is None:
            raise ValueError("Alternativa não encontrada.")

        if not texto:
            raise ValueError("O texto da alternativa é obrigatório.")

        alternativa.atualizar(texto=texto, correta=correta)
        self.repository.salvar_alteracoes()
        return alternativa.to_dict()
