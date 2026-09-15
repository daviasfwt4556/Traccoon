import pytest

from services.alternativas.create_alternativa_service import CadastrarAlternativaService
from services.auth.registrar_usuario_service import RegistrarUsuarioService
from services.categorias.create_categoria_service import CadastrarCategoriaService
from services.questoes.create_questao_service import CadastrarQuestaoService
from services.simulados.buscar_simulado_service import BuscarSimuladoService
from services.simulados.finalizar_simulado_service import FinalizarSimuladoService
from services.simulados.iniciar_simulado_service import IniciarSimuladoService


def _preparar_categoria_com_duas_questoes(app_context):
    """
    Monta uma categoria com 2 questões, cada uma com 2 alternativas
    (uma certa e uma errada), pra poder testar o cálculo de nota.
    """
    categoria = CadastrarCategoriaService().executar("Legislação", "Regras de trânsito")

    questao1 = CadastrarQuestaoService().executar("Pergunta 1", categoria["id"])
    certa1 = CadastrarAlternativaService().executar(questao1["id"], "Certa 1", correta=True)
    CadastrarAlternativaService().executar(questao1["id"], "Errada 1", correta=False)

    questao2 = CadastrarQuestaoService().executar("Pergunta 2", categoria["id"])
    certa2 = CadastrarAlternativaService().executar(questao2["id"], "Certa 2", correta=True)
    CadastrarAlternativaService().executar(questao2["id"], "Errada 2", correta=False)

    return categoria, [certa1, certa2]


class TestIniciarSimuladoService:
    def test_cria_um_item_por_questao_da_categoria(self, app_context):
        usuario = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")
        categoria, _ = _preparar_categoria_com_duas_questoes(app_context)

        simulado = IniciarSimuladoService().executar(usuario.id, categoria["id"])

        assert len(simulado["itens"]) == 2
        assert simulado["usuario_id"] == usuario.id

    def test_nao_permite_categoria_sem_questoes(self, app_context):
        usuario = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")
        categoria = CadastrarCategoriaService().executar("Vazia", "Sem questões ainda")

        with pytest.raises(ValueError):
            IniciarSimuladoService().executar(usuario.id, categoria["id"])

    def test_nao_permite_usuario_inexistente(self, app_context):
        categoria, _ = _preparar_categoria_com_duas_questoes(app_context)

        with pytest.raises(ValueError):
            IniciarSimuladoService().executar(9999, categoria["id"])


class TestFinalizarSimuladoService:
    def test_acertar_tudo_da_nota_maxima(self, app_context):
        usuario = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")
        categoria, alternativas_corretas = _preparar_categoria_com_duas_questoes(app_context)
        simulado = IniciarSimuladoService().executar(usuario.id, categoria["id"])

        respostas = [
            {"item_id": item["id"], "alternativa_id": alternativas_corretas[i]["id"]}
            for i, item in enumerate(simulado["itens"])
        ]

        resultado = FinalizarSimuladoService().executar(simulado["id"], respostas, usuario.id)

        assert resultado["resultado"]["nota"] == 100.0

    def test_acertar_metade_da_metade_da_nota(self, app_context):
        usuario = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")
        categoria, alternativas_corretas = _preparar_categoria_com_duas_questoes(app_context)
        simulado = IniciarSimuladoService().executar(usuario.id, categoria["id"])

        # Acerta só o primeiro item, erra o segundo de propósito.
        respostas = [
            {"item_id": simulado["itens"][0]["id"], "alternativa_id": alternativas_corretas[0]["id"]},
            {"item_id": simulado["itens"][1]["id"], "alternativa_id": 999999},
        ]

        resultado = FinalizarSimuladoService().executar(simulado["id"], respostas, usuario.id)

        assert resultado["resultado"]["nota"] == 50.0

    def test_nao_permite_finalizar_simulado_de_outro_usuario(self, app_context):
        dono = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")
        outro_usuario = RegistrarUsuarioService().executar("Bruno", "bruno@exemplo.com", "123456")
        categoria, _ = _preparar_categoria_com_duas_questoes(app_context)
        simulado = IniciarSimuladoService().executar(dono.id, categoria["id"])

        with pytest.raises(PermissionError):
            FinalizarSimuladoService().executar(simulado["id"], [], outro_usuario.id)

    def test_erro_ao_finalizar_simulado_inexistente(self, app_context):
        usuario = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        with pytest.raises(ValueError):
            FinalizarSimuladoService().executar(9999, [], usuario.id)


class TestBuscarSimuladoService:
    def test_nao_permite_ver_simulado_de_outro_usuario(self, app_context):
        dono = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")
        outro_usuario = RegistrarUsuarioService().executar("Bruno", "bruno@exemplo.com", "123456")
        categoria, _ = _preparar_categoria_com_duas_questoes(app_context)
        simulado = IniciarSimuladoService().executar(dono.id, categoria["id"])

        with pytest.raises(PermissionError):
            BuscarSimuladoService().executar(simulado["id"], outro_usuario.id)

    def test_retorna_none_para_simulado_inexistente(self, app_context):
        usuario = RegistrarUsuarioService().executar("Ana", "ana@exemplo.com", "123456")

        assert BuscarSimuladoService().executar(9999, usuario.id) is None
