const formQuestao = document.querySelector("#form-questao");
const questaoIdCampo = document.querySelector("#questao-id");
const campoEnunciado = document.querySelector("#enunciado");
const campoCategoria = document.querySelector("#categoria_id");
const tabelaQuestoes = document.querySelector("#tabela-questoes");
const mensagem = document.querySelector("#mensagem");
const tituloFormulario = document.querySelector("#titulo-formulario");
const botaoSalvar = document.querySelector("#botao-salvar");
const botaoCancelar = document.querySelector("#botao-cancelar");

const POR_PAGINA = 20;
let paginaAtual = 1;

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.style.color = tipo === "erro" ? "#e53e3e" : "#38a169";
    if (typeof mostrarToast === "function") {
        mostrarToast(texto, tipo === "erro" ? "erro" : "sucesso");
    }
}

function limparFormulario() {
    questaoIdCampo.value = "";
    campoEnunciado.value = "";
    tituloFormulario.textContent = "Cadastrar Questão";
    botaoSalvar.textContent = "Salvar";
}

async function carregarCategoriasNoSelect() {
    // Sem pagina/por_pagina: a API devolve a lista inteira, certo pra um <select>.
    const categorias = await api.get("/categorias/");
    campoCategoria.innerHTML = categorias
        .map((c) => `<option value="${c.id}">${c.nome}</option>`)
        .join("");
}

function renderizarQuestoes(questoes) {
    tabelaQuestoes.innerHTML = "";
    if (questoes.length === 0) {
        tabelaQuestoes.innerHTML = `<tr><td colspan="4">Nenhuma questão cadastrada.</td></tr>`;
        return;
    }
    questoes.forEach((q) => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${q.id}</td><td>${q.enunciado}</td><td>${q.categoria_nome || "—"}</td>
            <td>
                <a href="#" onclick='prepararEdicao(${JSON.stringify(q)}); return false;'>Editar</a>
                &nbsp;|&nbsp;
                <a href="#" style="color:#e53e3e;" onclick="deletarQuestao(${q.id}); return false;">Excluir</a>
            </td>`;
        tabelaQuestoes.appendChild(linha);
    });
}

async function listarQuestoes(pagina = 1) {
    try {
        const dados = await api.get(`/questoes/?pagina=${pagina}&por_pagina=${POR_PAGINA}`);

        if (dados.itens.length === 0 && dados.pagina_atual > 1) {
            return listarQuestoes(dados.pagina_atual - 1);
        }

        paginaAtual = dados.pagina_atual;
        renderizarQuestoes(dados.itens);
        renderizarPaginacao("paginacao-questoes", dados, listarQuestoes);
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

function prepararEdicao(questao) {
    questaoIdCampo.value = questao.id;
    campoEnunciado.value = questao.enunciado;
    campoCategoria.value = questao.categoria_id;
    tituloFormulario.textContent = "Editar Questão";
    botaoSalvar.textContent = "Atualizar";
}

async function salvarQuestao(evento) {
    evento.preventDefault();
    const dados = { enunciado: campoEnunciado.value, categoria_id: campoCategoria.value };
    const id = questaoIdCampo.value;

    try {
        if (id) {
            await api.put(`/questoes/${id}`, dados);
            mostrarMensagem("Questão atualizada com sucesso.", "sucesso");
            limparFormulario();
            listarQuestoes(paginaAtual);
        } else {
            await api.post("/questoes/", dados);
            mostrarMensagem("Questão cadastrada com sucesso.", "sucesso");
            limparFormulario();
            listarQuestoes(1);
        }
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

async function deletarQuestao(id) {
    if (!confirm("Deseja realmente excluir esta questão? As alternativas dela também serão apagadas.")) return;
    try {
        await api.delete(`/questoes/${id}`);
        mostrarMensagem("Questão excluída.", "sucesso");
        listarQuestoes(paginaAtual);
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

formQuestao.addEventListener("submit", salvarQuestao);
botaoCancelar.addEventListener("click", limparFormulario);

(async () => {
    await carregarCategoriasNoSelect();
    await listarQuestoes(1);
})();
