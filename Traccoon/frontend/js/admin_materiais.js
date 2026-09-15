const formMaterial = document.querySelector("#form-material");
const materialIdCampo = document.querySelector("#material-id");
const campoCategoria = document.querySelector("#categoria_id");
const campoConteudo = document.querySelector("#conteudo");
const campoUrl = document.querySelector("#url");
const tabelaMateriais = document.querySelector("#tabela-materiais");
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
    materialIdCampo.value = "";
    campoConteudo.value = "";
    campoUrl.value = "";
    tituloFormulario.textContent = "Cadastrar Material";
    botaoSalvar.textContent = "Salvar";
}

async function carregarCategoriasNoSelect() {
    const categorias = await api.get("/categorias/");
    campoCategoria.innerHTML = categorias
        .map((c) => `<option value="${c.id}">${c.nome}</option>`)
        .join("");
}

function renderizarMateriais(materiais) {
    tabelaMateriais.innerHTML = "";
    if (materiais.length === 0) {
        tabelaMateriais.innerHTML = `<tr><td colspan="4">Nenhum material cadastrado.</td></tr>`;
        return;
    }
    materiais.forEach((m) => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${m.id}</td><td>${m.categoria_nome || "—"}</td><td>${m.conteudo.substring(0, 80)}...</td>
            <td>
                <a href="#" onclick='prepararEdicao(${JSON.stringify(m)}); return false;'>Editar</a>
                &nbsp;|&nbsp;
                <a href="#" style="color:#e53e3e;" onclick="deletarMaterial(${m.id}); return false;">Excluir</a>
            </td>`;
        tabelaMateriais.appendChild(linha);
    });
}

async function listarMateriais(pagina = 1) {
    try {
        const dados = await api.get(`/materiais/?pagina=${pagina}&por_pagina=${POR_PAGINA}`);

        if (dados.itens.length === 0 && dados.pagina_atual > 1) {
            return listarMateriais(dados.pagina_atual - 1);
        }

        paginaAtual = dados.pagina_atual;
        renderizarMateriais(dados.itens);
        renderizarPaginacao("paginacao-materiais", dados, listarMateriais);
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

function prepararEdicao(material) {
    materialIdCampo.value = material.id;
    campoCategoria.value = material.categoria_id;
    campoConteudo.value = material.conteudo;
    campoUrl.value = material.url || "";
    tituloFormulario.textContent = "Editar Material";
    botaoSalvar.textContent = "Atualizar";
}

async function salvarMaterial(evento) {
    evento.preventDefault();
    const id = materialIdCampo.value;

    try {
        if (id) {
            await api.put(`/materiais/${id}`, { conteudo: campoConteudo.value, url: campoUrl.value });
            mostrarMensagem("Material atualizado com sucesso.", "sucesso");
            limparFormulario();
            listarMateriais(paginaAtual);
        } else {
            await api.post("/materiais/", {
                categoria_id: campoCategoria.value,
                conteudo: campoConteudo.value,
                url: campoUrl.value,
            });
            mostrarMensagem("Material cadastrado com sucesso.", "sucesso");
            limparFormulario();
            listarMateriais(1);
        }
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

async function deletarMaterial(id) {
    if (!confirm("Deseja realmente excluir este material?")) return;
    try {
        await api.delete(`/materiais/${id}`);
        mostrarMensagem("Material excluído.", "sucesso");
        listarMateriais(paginaAtual);
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

formMaterial.addEventListener("submit", salvarMaterial);
botaoCancelar.addEventListener("click", limparFormulario);

(async () => {
    await carregarCategoriasNoSelect();
    await listarMateriais(1);
})();
