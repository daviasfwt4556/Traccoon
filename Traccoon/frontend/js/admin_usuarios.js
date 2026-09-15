const formUsuario = document.querySelector("#form-usuario");
const usuarioIdCampo = document.querySelector("#usuario-id");
const campoNome = document.querySelector("#nome");
const campoEmail = document.querySelector("#email");
const campoSenha = document.querySelector("#senha");
const campoIsAdmin = document.querySelector("#is-admin");
const dicaSenha = document.querySelector("#dica-senha");
const tabelaUsuarios = document.querySelector("#tabela-usuarios");
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
    usuarioIdCampo.value = "";
    campoNome.value = "";
    campoEmail.value = "";
    campoSenha.value = "";
    campoIsAdmin.checked = false;
    campoSenha.placeholder = "Mínimo 4 caracteres";
    dicaSenha.style.display = "none";
    tituloFormulario.textContent = "Cadastrar Usuário";
    botaoSalvar.textContent = "Salvar";
}

function renderizarUsuarios(usuarios) {
    tabelaUsuarios.innerHTML = "";
    if (usuarios.length === 0) {
        tabelaUsuarios.innerHTML = `<tr><td colspan="5">Nenhum usuário cadastrado.</td></tr>`;
        return;
    }
    usuarios.forEach((u) => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${u.id}</td><td>${u.nome}</td><td>${u.email}</td><td>${u.is_admin ? "Sim" : "Não"}</td>
            <td>
                <a href="#" onclick='prepararEdicao(${JSON.stringify(u)}); return false;'>Editar</a>
                &nbsp;|&nbsp;
                <a href="#" style="color:#e53e3e;" onclick="deletarUsuario(${u.id}); return false;">Excluir</a>
            </td>`;
        tabelaUsuarios.appendChild(linha);
    });
}

async function listarUsuarios(pagina = 1) {
    try {
        const dados = await api.get(`/usuarios/?pagina=${pagina}&por_pagina=${POR_PAGINA}`);

        // Se a página pedida ficou vazia (ex: excluiu o último item de uma
        // página maior que 1), volta uma página em vez de mostrar vazio.
        if (dados.itens.length === 0 && dados.pagina_atual > 1) {
            return listarUsuarios(dados.pagina_atual - 1);
        }

        paginaAtual = dados.pagina_atual;
        renderizarUsuarios(dados.itens);
        renderizarPaginacao("paginacao-usuarios", dados, listarUsuarios);
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

function prepararEdicao(usuario) {
    usuarioIdCampo.value = usuario.id;
    campoNome.value = usuario.nome;
    campoEmail.value = usuario.email;
    campoSenha.value = "";
    campoIsAdmin.checked = !!usuario.is_admin;
    campoSenha.placeholder = "Deixe em branco para manter a senha atual";
    dicaSenha.style.display = "block";
    tituloFormulario.textContent = "Editar Usuário";
    botaoSalvar.textContent = "Atualizar";
}

async function salvarUsuario(evento) {
    evento.preventDefault();
    const id = usuarioIdCampo.value;
    const dados = { nome: campoNome.value, email: campoEmail.value, is_admin: campoIsAdmin.checked };
    if (campoSenha.value) dados.senha = campoSenha.value;

    try {
        if (id) {
            await api.put(`/usuarios/${id}`, dados);
            mostrarMensagem("Usuário atualizado com sucesso.", "sucesso");
            limparFormulario();
            listarUsuarios(paginaAtual);
        } else {
            if (!campoSenha.value) {
                mostrarMensagem("Informe uma senha para o novo usuário.", "erro");
                return;
            }
            await api.post("/usuarios/", dados);
            mostrarMensagem("Usuário cadastrado com sucesso.", "sucesso");
            limparFormulario();
            listarUsuarios(1);
        }
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

async function deletarUsuario(id) {
    if (!confirm("Deseja realmente excluir este usuário?")) return;
    try {
        await api.delete(`/usuarios/${id}`);
        mostrarMensagem("Usuário excluído.", "sucesso");
        listarUsuarios(paginaAtual);
    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}

formUsuario.addEventListener("submit", salvarUsuario);
botaoCancelar.addEventListener("click", limparFormulario);
listarUsuarios(1);
