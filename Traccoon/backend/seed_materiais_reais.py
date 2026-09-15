"""
Script de carga de conteúdo real no banco de dados.

Igual ao seed_questoes_reais.py: NÃO altera nenhum model — só usa a
Model Material já existente para inserir linhas reais na tabela
'materiais' do banco (autotrans.db), ligadas às categorias já cadastradas.

Como rodar (depois que as categorias já existem, via seed_questoes_reais.py
ou pelo admin):
    cd backend
    python seed_materiais_reais.py
"""

from app import app
from models import Categoria, Material
from repositories.material_repository import MaterialRepository

# Cada item: (nome da categoria já cadastrada, url oficial de referência, [ texto1, texto2, ... ])
CONTEUDO = {
    "Legislação de Trânsito": {
        "url": "https://www.planalto.gov.br/ccivil_03/leis/l9503compilado.htm",
        "textos": [
            "A Lei Seca adota tolerância zero: qualquer concentração de álcool no "
            "organismo do condutor já é considerada infração, independentemente da "
            "quantidade ingerida. Não existe uma 'dose permitida' antes de dirigir.",
            "Em cruzamentos sem sinalização (sem placa ou semáforo), a regra geral de "
            "preferência é: tem prioridade de passagem o veículo que vier pela direita "
            "do condutor. Essa regra vale para a maioria dos cruzamentos comuns em "
            "áreas urbanas.",
            "O uso do cinto de segurança é obrigatório para todos os ocupantes do "
            "veículo, em qualquer banco — motorista, passageiro da frente e "
            "passageiros de trás. Trafegar sem o cinto é considerado infração grave.",
        ],
    },
    "Sinalização de Trânsito": {
        "url": "https://www.gov.br/transportes/pt-br/assuntos/transito/senatran/manuais-brasileiros-de-sinalizacao-de-transito",
        "textos": [
            "As placas de trânsito são divididas em três grandes grupos, cada um com "
            "uma cor e formato próprios: REGULAMENTAÇÃO (circulares, fundo branco, "
            "borda vermelha) impõem uma obrigação, proibição ou restrição — como "
            "'Pare' ou 'Proibido Estacionar'. ADVERTÊNCIA (triangulares, fundo "
            "amarelo) alertam sobre um perigo à frente, como uma curva ou pista "
            "escorregadia. INDICAÇÃO (retangulares, fundo azul ou verde) informam "
            "direções, distâncias e serviços disponíveis.",
            "A placa 'PARE' (octogonal, vermelha) é a única que exige parada "
            "completa e obrigatória do veículo antes de prosseguir, mesmo que a via "
            "esteja livre no momento.",
            "Semáforos amarelos piscantes (intermitentes) indicam que o condutor "
            "deve reduzir a velocidade e seguir com atenção redobrada — é diferente "
            "do amarelo fixo, que antecede o vermelho e pede que o condutor pare, "
            "caso ainda seja possível fazê-lo com segurança.",
        ],
    },
    "Direção Defensiva": {
        "url": "https://www.detraneduca.pr.gov.br/Pagina/Direcao-defensiva",
        "textos": [
            "Direção defensiva é a forma de dirigir que busca prevenir acidentes, "
            "mesmo diante de condições adversas ou de erros cometidos por outros "
            "condutores, pedestres ou ciclistas. Não basta seguir as regras: é "
            "preciso antecipar riscos.",
            "A distância de segurança em relação ao veículo da frente não deve ser "
            "fixa — ela precisa aumentar conforme a velocidade do trânsito e as "
            "condições da via (chuva, pista molhada, pouca visibilidade). Quanto "
            "maior a velocidade, maior o espaço necessário para frear com segurança.",
            "Cansaço e sono são fatores de risco tão sérios quanto o álcool na "
            "direção. Ao sentir sinais de sonolência, a orientação é parar em local "
            "seguro e descansar — abrir o vidro ou aumentar o som não resolvem o "
            "problema, só mascaram os sintomas por pouco tempo.",
        ],
    },
    "Primeiros Socorros": {
        "url": "https://bvsms.saude.gov.br/bvs/publicacoes/manual_primeiros_socorros.pdf",
        "textos": [
            "Ao se deparar com um acidente de trânsito, a primeira atitude não é "
            "mover a vítima, e sim sinalizar o local (para evitar novos acidentes) "
            "e acionar o socorro especializado pelo número 192 (SAMU).",
            "Vítimas conscientes devem, sempre que possível, ser mantidas no local "
            "onde foram encontradas, com o mínimo de movimentação, até a chegada do "
            "socorro — mover uma vítima de forma incorreta pode agravar lesões na "
            "coluna que não são visíveis a olho nu.",
            "O método PAS resume a sequência básica de atendimento em uma emergência: "
            "Proteger (sinalizar o local e evitar novos acidentes), Alertar "
            "(acionar o socorro) e Socorrer (prestar os primeiros cuidados dentro "
            "do que o condutor souber fazer com segurança, sem se colocar em risco).",
        ],
    },
    "Mecânica Básica": {
        "url": "https://escola.detran.rs.gov.br/wp-content/uploads/2022/11/funcionamento_veiculo.pdf",
        "textos": [
            "O painel do veículo tem luzes indicadoras que avisam sobre problemas "
            "antes que eles se tornem graves. A luz de óleo, por exemplo, indica "
            "problema na pressão ou no nível do óleo do motor e não deve ser "
            "ignorada.",
            "Pane seca é o termo usado quando o veículo para de funcionar por falta "
            "de combustível — é uma das causas mais comuns (e mais evitáveis) de "
            "veículos parados no acostamento.",
            "Se o motor superaquecer ('ferver'), o procedimento correto é parar em "
            "local seguro, desligar o motor e aguardar esfriar antes de sequer "
            "tentar abrir o radiador — abrir um radiador quente pode causar "
            "queimaduras sérias pela pressão e pelo vapor liberado.",
        ],
    },
}


def popular():
    with app.app_context():
        repository = MaterialRepository()
        total_materiais = 0

        for nome_categoria, dados in CONTEUDO.items():
            categoria = Categoria.query.filter_by(nome=nome_categoria).first()

            if categoria is None:
                print(
                    f"Categoria '{nome_categoria}' não encontrada — rode "
                    f"seed_questoes_reais.py primeiro, ou cadastre essa categoria "
                    f"pelo admin antes de rodar este script."
                )
                continue

            url = dados["url"]
            for texto in dados["textos"]:
                material_existente = Material.query.filter_by(
                    categoria_id=categoria.id, conteudo=texto
                ).first()
                if material_existente is not None:
                    print(f"  Material já existia, pulando ({nome_categoria})")
                    continue

                material = Material(categoria_id=categoria.id, conteudo=texto, url=url)
                repository.criar(material)
                total_materiais += 1
                print(f"Material criado em '{nome_categoria}' (com link: {url})")

        print()
        print("Carga concluída:")
        print(f"  Materiais novos: {total_materiais}")


if __name__ == "__main__":
    popular()
