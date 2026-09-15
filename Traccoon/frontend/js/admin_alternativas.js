const formAlternativa = document.querySelector("#form-alternativa");
const alternativaIdCampo = document.querySelector("#alternativa-id");
const campoQuestao = document.querySelector("#questao_id");
const campoTexto = document.querySelector("#texto");
const campoCorreta = document.querySelector("#correta");
const tabelaAlternativas = document.querySelector("#tabela-alternativas");
const mensagem = document.querySelector("#mensagem");
const tituloFormulario = document.querySelector("#titulo-formulario");
const botaoSalvar = document.querySelector("#botao-salvar");
const botaoCancelar = document.querySelector("#botao-cancelar");

const POR_PAGINA = 20;
let paginaAtual = 1;
let questoesCache = [];

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.style.color = tipo === "erro" ? "#e53e3e" : "#38a169";
    if (typeof mostrarToast === "function") {
        mostrarToast(texto, tipo === "erro" ? "erro" : "sucesso");
    }
}

function limparFormulario() {
    alternativaIdCampo.value = "";
    campoTexto.value = "";
    campoCorreta.checked = false;
    tituloFormulario.textContent = "Cadastrar Alternativa";
    botaoSalvar.textContent = "Salvar";
}

async function carregarQuestoesNoSelect() {
    questoesCache = await api.get("/questoes/");
    campoQuestao.innerHTML = questoesCache
        .map((q) => `<option value="${q.id}">#${q.id} — ${q.enunciado.substring(0, 60)}</option>`)
        .join("");
}

function renderizarAlternativas(alternativas) {
    tabelaAlternativas.innerHTML = "";
    if (alternativas.length === 0) {
        tabelaAlternativas.innerHTML = `<tr><td colspan="5">Nenhuma alternativa cadastrada.</td></tr>`;
        return;
    }
    alternativas.forEach((a) => {
        const questao = questoesCache.find((q) => q.id === a.questao_id);
        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${a.id}</td>
            <td>${questao ? "#" + questao.id : a.questao_id}</td>
            <td>${a.texto}</td>
            <td>${a.correta ? "✅" : ""}</td>
            <td>
                <a href="#" onclick='prepararEdicao(${JSON.stringify(a)}); return false;'>Editar</a>
                &nbsp;|&nbsp;
                <a href="#" style="color:#e53e3e;" onclick="deletarAlternativa(${a.id}); return false;">Excluir</a>
            </td>`;
        tabelaAlternativas.appendChild(linha);
    });
}

async function listarAlternativas(pagina = 1) {
    try {
        const dados = await api.get(`/alternativas/?pagina=${pagina}&por_pagina=${POR_PAGINA}`);

        if (dados.itens.length === 0 && dados.pagina_atual > 1) {
            return listarAlternativas(dados.pagina_atual - 1);
        }

        paginaAtual = dados.pagina_atual;
        renderizarAlternativas(dados.itens);
        renderizarPaginacao("paginacao-alternativas", dados, listarAlternativas);
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

function prepararEdicao(alternativa) {
    alternativaIdCampo.value = alternativa.id;
    campoQuestao.value = alternativa.questao_id;
    campoTexto.value = alternativa.texto;
    campoCorreta.checked = alternativa.correta;
    tituloFormulario.textContent = "Editar Alternativa";
    botaoSalvar.textContent = "Atualizar";
}

async function salvarAlternativa(evento) {
    evento.preventDefault();
    const id = alternativaIdCampo.value;

    try {
        if (id) {
            await api.put(`/alternativas/${id}`, {
                texto: campoTexto.value,
                correta: campoCorreta.checked,
            });
            mostrarMensagem("Alternativa atualizada com sucesso.", "sucesso");
            limparFormulario();
            listarAlternativas(paginaAtual);
        } else {
            await api.post("/alternativas/", {
                questao_id: campoQuestao.value,
                texto: campoTexto.value,
                correta: campoCorreta.checked,
            });
            mostrarMensagem("Alternativa cadastrada com sucesso.", "sucesso");
            limparFormulario();
            listarAlternativas(1);
        }
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

async function deletarAlternativa(id) {
    if (!confirm("Deseja realmente excluir esta alternativa?")) return;
    try {
        await api.delete(`/alternativas/${id}`);
        mostrarMensagem("Alternativa excluída.", "sucesso");
        listarAlternativas(paginaAtual);
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

formAlternativa.addEventListener("submit", salvarAlternativa);
botaoCancelar.addEventListener("click", limparFormulario);

(async () => {
    await carregarQuestoesNoSelect();
    await listarAlternativas(1);
})();
