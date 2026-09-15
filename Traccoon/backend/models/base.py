from . import db


class ModeloBase(db.Model):
    """
    Superclasse abstrata — não vira tabela no banco.
    Todas as classes herdam só o id; quem precisar de data de criação
    declara essa coluna na própria classe (Simulado e Resultado, por agora).
    """

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
