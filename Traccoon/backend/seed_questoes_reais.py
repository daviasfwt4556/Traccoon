"""
Script de carga de conteúdo real no banco de dados.

Isso NÃO altera nenhum model — só usa as Models já existentes
(Categoria, Questao, Alternativa) para inserir linhas reais nas
tabelas do banco (autotrans.db), do mesmo jeito que o admin faria
clicando nas telas, só que em lote.

Como rodar (uma vez só, depois que o banco já existe):
    cd backend
    python seed_questoes_reais.py
"""

from app import app
from models import Alternativa, Categoria, Questao
from repositories.alternativa_repository import AlternativaRepository
from repositories.categoria_repository import CategoriaRepository
from repositories.questao_repository import QuestaoRepository

# Cada item: (nome da categoria, descrição, [ (enunciado, [ (texto, correta), ... ]), ... ])
CONTEUDO = [
    (
        "Legislação de Trânsito",
        "Regras de circulação e normas do Código de Trânsito Brasileiro.",
        [
            (
                "Segundo a Lei Seca, qual é a tolerância de álcool no sangue para dirigir?",
                [
                    ("É permitida uma taça de vinho antes de dirigir", False),
                    ("Tolerância zero: qualquer quantidade já é infração", True),
                    ("O limite é de uma dose de bebida destilada", False),
                    ("Só é infração acima de 0,6 g de álcool por litro de sangue", False),
                ],
            ),
            (
                "Em um cruzamento sem sinalização, quem tem a preferência de passagem?",
                [
                    ("Quem buzinar primeiro", False),
                    ("O veículo que vem pela via mais larga", False),
                    ("O veículo que vem pela direita do condutor", True),
                    ("Quem estiver em maior velocidade", False),
                ],
            ),
            (
                "Ao se aproximar de uma faixa de pedestres sem semáforo, o condutor deve:",
                [
                    ("Buzinar para o pedestre andar mais rápido", False),
                    ("Dar prioridade total ao pedestre que está atravessando", True),
                    ("Passar primeiro, desde que em velocidade baixa", False),
                    ("Só parar se houver um agente de trânsito no local", False),
                ],
            ),
            (
                "O uso do cinto de segurança é obrigatório para:",
                [
                    ("Somente o motorista", False),
                    ("Motorista e passageiro da frente", False),
                    ("Todos os ocupantes do veículo, em qualquer banco", True),
                    ("Apenas em viagens por rodovias", False),
                ],
            ),
            (
                "Estacionar em vaga reservada para pessoa com deficiência, sem a credencial "
                "correspondente, é classificado como:",
                [
                    ("Infração leve", False),
                    ("Infração gravíssima", True),
                    ("Apenas uma advertência verbal", False),
                    ("Permitido se a vaga estiver livre há muito tempo", False),
                ],
            ),
        ],
    ),
    (
        "Sinalização de Trânsito",
        "Significado de placas, semáforos e marcas viárias.",
        [
            (
                "A placa octogonal vermelha com a palavra 'PARE' exige que o condutor:",
                [
                    ("Reduza a velocidade e siga se não houver veículos", False),
                    ("Pare completamente o veículo antes de prosseguir", True),
                    ("Buzine antes de passar pelo cruzamento", False),
                    ("Pare apenas se houver fiscalização no local", False),
                ],
            ),
            (
                "As placas circulares com fundo branco e borda vermelha são do tipo:",
                [
                    ("Advertência", False),
                    ("Regulamentação", True),
                    ("Indicação", False),
                    ("Educativa", False),
                ],
            ),
            (
                "As placas triangulares com fundo amarelo têm a função de:",
                [
                    ("Proibir uma ação do condutor", False),
                    ("Alertar sobre um perigo ou situação especial na via", True),
                    ("Indicar serviços disponíveis nas proximidades", False),
                    ("Indicar o limite máximo de velocidade", False),
                ],
            ),
            (
                "As placas retangulares azuis (de indicação) servem para informar:",
                [
                    ("Proibições de trânsito", False),
                    ("Perigos existentes na pista", False),
                    ("Serviços, distâncias e direções", True),
                    ("Limites obrigatórios de velocidade", False),
                ],
            ),
            (
                "Um semáforo amarelo piscante indica que o condutor deve:",
                [
                    ("Parar obrigatoriamente antes de seguir", False),
                    ("Seguir em velocidade máxima", False),
                    ("Reduzir a velocidade e seguir com atenção", True),
                    ("Aguardar até que apenas pedestres atravessem", False),
                ],
            ),
        ],
    ),
    (
        "Direção Defensiva",
        "Como prever e evitar acidentes de trânsito.",
        [
            (
                "A distância de segurança em relação ao veículo da frente deve:",
                [
                    ("Ser sempre a mesma, independente da velocidade", False),
                    ("Aumentar conforme a velocidade e as condições da via", True),
                    ("Diminuir em dias de chuva, para não perder o outro carro de vista", False),
                    ("Ser ignorada dentro de vias urbanas", False),
                ],
            ),
            (
                "O principal objetivo da direção defensiva é:",
                [
                    ("Chegar mais rápido ao destino", False),
                    ("Prevenir acidentes, mesmo diante de erros de outros condutores", True),
                    ("Reduzir o consumo de combustível", False),
                    ("Evitar multas de trânsito", False),
                ],
            ),
            (
                "Ao perceber sinais de sonolência durante a direção, o condutor deve:",
                [
                    ("Abrir o vidro do carro e continuar dirigindo", False),
                    ("Aumentar o volume do som do veículo", False),
                    ("Parar em local seguro e descansar antes de continuar", True),
                    ("Dirigir mais rápido para chegar logo ao destino", False),
                ],
            ),
            (
                "Ao se aproximar de uma curva sem visibilidade, o condutor deve:",
                [
                    ("Acelerar para passar pela curva mais rápido", False),
                    ("Reduzir a velocidade antecipadamente", True),
                    ("Buzinar e manter a mesma velocidade", False),
                    ("Aproveitar para ultrapassar antes da curva", False),
                ],
            ),
            (
                "Dirigir sob forte chuva exige do condutor que ele:",
                [
                    ("Aumente a velocidade para sair da chuva mais rápido", False),
                    ("Reduza a velocidade e aumente a distância do carro à frente", True),
                    ("Desligue os faróis para economizar bateria", False),
                    ("Ignore a sinalização até a chuva passar", False),
                ],
            ),
        ],
    ),
    (
        "Primeiros Socorros",
        "Condutas básicas em caso de acidente de trânsito.",
        [
            (
                "Ao encontrar uma vítima de acidente, a primeira ação recomendada é:",
                [
                    ("Mover a vítima imediatamente para a calçada", False),
                    ("Sinalizar o local do acidente e acionar o socorro (SAMU 192)", True),
                    ("Dar água para a vítima beber", False),
                    ("Retirar o capacete da vítima em qualquer situação", False),
                ],
            ),
            (
                "Em caso de hemorragia externa visível, o procedimento recomendado é:",
                [
                    ("Aplicar torniquete imediatamente em qualquer ferimento", False),
                    ("Fazer compressão direta sobre o ferimento com um pano limpo", True),
                    ("Lavar o ferimento com álcool", False),
                    ("Não fazer nada até o socorro chegar", False),
                ],
            ),
            (
                "Qual é o número de telefone do SAMU no Brasil?",
                [
                    ("190", False),
                    ("193", False),
                    ("192", True),
                    ("199", False),
                ],
            ),
            (
                "Uma vítima consciente de acidente deve, de preferência, ser:",
                [
                    ("Movida rapidamente para outro local", False),
                    ("Mantida no local, mexida o mínimo possível, até o socorro chegar", True),
                    ("Colocada de pé imediatamente", False),
                    ("Alimentada e hidratada assim que possível", False),
                ],
            ),
            (
                "O método PAS, usado em primeiros socorros, representa:",
                [
                    ("Proteger, Alertar, Socorrer", True),
                    ("Parar, Analisar, Sair", False),
                    ("Prevenir, Agir, Salvar", False),
                    ("Parar, Avisar, Seguir", False),
                ],
            ),
        ],
    ),
    (
        "Mecânica Básica",
        "Cuidados e verificações básicas do veículo.",
        [
            (
                "A luz de óleo acesa no painel do veículo indica:",
                [
                    ("Necessidade de calibrar os pneus", False),
                    ("Problema na pressão ou no nível do óleo do motor", True),
                    ("Farol queimado", False),
                    ("Bateria descarregada", False),
                ],
            ),
            (
                "Qual equipamento é obrigatório para sinalizar o veículo em caso de pane?",
                [
                    ("Somente o extintor de incêndio", False),
                    ("Triângulo de sinalização", True),
                    ("Somente o macaco", False),
                    ("Nenhum equipamento é exigido por lei", False),
                ],
            ),
            (
                "A verificação da pressão dos pneus deve ser feita, de preferência:",
                [
                    ("Apenas quando o pneu murchar visivelmente", False),
                    ("Regularmente, com os pneus frios", True),
                    ("Somente em postos de gasolina", False),
                    ("Uma vez por ano", False),
                ],
            ),
            (
                "Se o motor do veículo superaquecer (\"ferver\"), o condutor deve:",
                [
                    ("Continuar dirigindo até o destino", False),
                    (
                        "Parar em local seguro, desligar o motor e aguardar esfriar "
                        "antes de abrir o radiador",
                        True,
                    ),
                    ("Abrir o radiador imediatamente, mesmo quente", False),
                    ("Jogar água fria diretamente no motor quente", False),
                ],
            ),
            (
                "O termo 'pane seca' se refere a:",
                [
                    ("Bateria descarregada", False),
                    ("Falta de combustível no veículo", True),
                    ("Pneu furado", False),
                    ("Superaquecimento do motor", False),
                ],
            ),
        ],
    ),
]


def popular():
    with app.app_context():
        repository_categoria = CategoriaRepository()
        repository_questao = QuestaoRepository()
        repository_alternativa = AlternativaRepository()

        total_categorias = 0
        total_questoes = 0
        total_alternativas = 0

        for nome_categoria, descricao, questoes in CONTEUDO:
            categoria = Categoria.query.filter_by(nome=nome_categoria).first()
            if categoria is None:
                categoria = Categoria(nome=nome_categoria, descricao=descricao)
                repository_categoria.criar(categoria)
                total_categorias += 1
                print(f"Categoria criada: {nome_categoria}")
            else:
                print(f"Categoria já existia, reaproveitada: {nome_categoria}")

            for enunciado, alternativas in questoes:
                questao_existente = Questao.query.filter_by(
                    categoria_id=categoria.id, enunciado=enunciado
                ).first()
                if questao_existente is not None:
                    print(f"  Questão já existia, pulando: {enunciado[:50]}...")
                    continue

                questao = Questao(categoria_id=categoria.id, enunciado=enunciado)
                repository_questao.criar(questao)
                total_questoes += 1

                for texto, correta in alternativas:
                    alternativa = Alternativa(
                        questao_id=questao.id, texto=texto, correta=correta
                    )
                    repository_alternativa.criar(alternativa)
                    total_alternativas += 1

        print()
        print("Carga concluída:")
        print(f"  Categorias novas: {total_categorias}")
        print(f"  Questões novas: {total_questoes}")
        print(f"  Alternativas novas: {total_alternativas}")


if __name__ == "__main__":
    popular()
