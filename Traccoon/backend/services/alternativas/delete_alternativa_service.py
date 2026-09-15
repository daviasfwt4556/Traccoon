from repositories.alternativa_repository import AlternativaRepository


class DeletarAlternativaService:
    def __init__(self):
        self.repository = AlternativaRepository()

    def executar(self, alternativa_id):
        alternativa = self.repository.buscar_por_id(alternativa_id)
        if alternativa is None:
            raise ValueError("Alternativa não encontrada.")

        self.repository.deletar(alternativa)
        return True
