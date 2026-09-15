// ==========================================
// PAINEL — carrega dados reais da API
// ==========================================

let simuladoAtual = null;
let indiceQuestaoAtual = 0;
let alternativaEscolhida = null;
let respostasDoUsuario = []; // [{item_id, alternativa_id}]
let usuarioAtual = null;

function sair() {
    removerToken();
    window.location.href = "../index.html";
}

// Preenche a tela "Meu Perfil" (foto, nome, e-mail e os campos do formulário
// de edição) a partir dos dados do usuário logado.
function renderizarPerfil(usuario) {
    document.getElementById("perfil-nome").textContent = usuario.nome;
    document.getElementById("perfil-email").textContent = usuario.email;
    document.getElementById("perfil-input-nome").value = usuario.nome;
    document.getElementById("perfil-input-foto").value = usuario.foto_url || "";

    const fotoContainer = document.getElementById("perfil-foto-container");
    if (usuario.foto_url) {
        fotoContainer.innerHTML = `<img src="${usuario.foto_url}" alt="Foto de perfil" style="width:100%; height:100%; object-fit: cover; border-radius: 50%;">`;
    } else {
        fotoContainer.innerHTML = "🦝";
    }
}

// Mostra os links "Gerir ..." do menu lateral só para administradores —
// o backend também bloqueia essas rotas, isso aqui é só pra não exibir
// um link que o aluno não tem permissão de usar.
function aplicarVisibilidadeAdmin(usuario) {
    document.querySelectorAll(".admin-only").forEach((el) => {
        el.style.display = usuario.is_admin ? "" : "none";
    });
}

async function carregarUsuario() {
    if (!estaLogado()) {
        window.location.href = "../index.html";
        return null;
    }

    try {
        const usuario = await api.get("/auth/me");
        usuarioAtual = usuario;
        document.getElementById("saudacao-usuario").textContent = `Olá, ${usuario.nome}!`;
        renderizarPerfil(usuario);
        aplicarVisibilidadeAdmin(usuario);
        return usuario;
    } catch (erro) {
        // Token inválido/expirado: limpa antes de voltar, senão a tela de
        // boas-vindas tentaria redirecionar de volta pra cá (loop infinito).
        removerToken();
        window.location.href = "../index.html";
        return null;
    }
}

// ==========================================
// PERFIL — editar (nome, foto, senha) ou excluir a própria conta
// ==========================================
async function salvarPerfil(evento) {
    evento.preventDefault();
    const msg = document.getElementById("perfil-mensagem");
    msg.textContent = "";
    msg.style.color = "";

    const dados = {
        nome: document.getElementById("perfil-input-nome").value.trim(),
        foto_url: document.getElementById("perfil-input-foto").value.trim(),
    };
    const senha = document.getElementById("perfil-input-senha").value;
    if (senha) dados.senha = senha;

    try {
        const usuario = await api.put("/auth/me", dados);
        usuarioAtual = usuario;
        renderizarPerfil(usuario);
        document.getElementById("saudacao-usuario").textContent = `Olá, ${usuario.nome}!`;
        document.getElementById("perfil-input-senha").value = "";
        msg.style.color = "#38a169";
        msg.textContent = "Dados atualizados com sucesso.";
    } catch (erro) {
        msg.style.color = "#e53e3e";
        msg.textContent = erro.message;
    }
}

async function excluirConta() {
    if (!confirm("Tem certeza que deseja excluir sua conta? Essa ação não pode ser desfeita.")) return;
    try {
        await api.delete("/auth/me");
        removerToken();
        window.location.href = "../index.html";
    } catch (erro) {
        alert(erro.message);
    }
}

async function carregarTrilhas() {
    const lista = document.getElementById("lista-trilhas");
    try {
        const categorias = await api.get("/categorias/");

        if (categorias.length === 0) {
            lista.innerHTML = "<p>Nenhuma categoria cadastrada ainda. Peça a um administrador para cadastrar em 'Gerir Categorias'.</p>";
            return;
        }

        lista.innerHTML = "";
        categorias.forEach((categoria) => {
            const div = document.createElement("div");
            div.className = "trail-card";
            div.onclick = () => iniciarSimulado(categoria.id);
            div.innerHTML = `
                <div class="trail-info">
                    <h4>${categoria.nome}</h4>
                    <p>${categoria.total_questoes} questões</p>
                </div>
                <div class="progress-bg"><div class="progress-fill" style="width: 0%;"></div></div>
            `;
            lista.appendChild(div);
        });
    } catch (erro) {
        lista.innerHTML = `<p style="color:#e53e3e;">${erro.message}</p>`;
    }
}

async function iniciarSimulado(categoriaId) {
    const divErro = document.getElementById("trilhas-erro");
    if (divErro) divErro.textContent = "";

    try {
        console.log("Iniciando simulado para categoria", categoriaId);
        simuladoAtual = await api.post("/simulados/", { categoria_id: categoriaId });
        console.log("Simulado criado:", simuladoAtual);
        indiceQuestaoAtual = 0;
        alternativaEscolhida = null;
        respostasDoUsuario = [];
        carregarQuestaoAtual();
        navigateTo("screen-quiz");
    } catch (erro) {
        console.error("Erro ao iniciar simulado:", erro);
        if (divErro) {
            divErro.textContent = erro.message;
        } else {
            alert(erro.message);
        }
    }
}

function carregarQuestaoAtual() {
    alternativaEscolhida = null;
    const item = simuladoAtual.itens[indiceQuestaoAtual];
    const total = simuladoAtual.itens.length;

    document.getElementById("quiz-contador").textContent = `Questão ${indiceQuestaoAtual + 1}/${total}`;
    document.getElementById("quiz-pergunta").textContent = item.questao.enunciado;
    document.getElementById("quiz-mensagem-erro").textContent = "";

    const container = document.getElementById("quiz-alternativas");
    container.innerHTML = "";
    item.questao.alternativas.forEach((alt, i) => {
        const btn = document.createElement("button");
        btn.className = "quiz-option";
        btn.id = `btn-alt-${i}`;
        btn.textContent = alt.texto;
        btn.onclick = () => selecionarAlternativa(alt.id, i);
        container.appendChild(btn);
    });

    const btnConfirmar = document.getElementById("btn-confirmar");
    const ultima = indiceQuestaoAtual === total - 1;
    btnConfirmar.textContent = ultima ? "Finalizar Simulado" : "Próxima Questão";
}

function selecionarAlternativa(alternativaId, indice) {
    alternativaEscolhida = alternativaId;
    document.querySelectorAll(".quiz-option").forEach((b) => b.classList.remove("selected"));
    document.getElementById(`btn-alt-${indice}`).classList.add("selected");
}

async function proximaQuestao() {
    if (alternativaEscolhida === null) {
        document.getElementById("quiz-mensagem-erro").textContent = "Selecione uma alternativa!";
        return;
    }

    const item = simuladoAtual.itens[indiceQuestaoAtual];
    respostasDoUsuario.push({ item_id: item.id, alternativa_id: alternativaEscolhida });

    if (indiceQuestaoAtual === simuladoAtual.itens.length - 1) {
        await finalizarSimulado();
    } else {
        indiceQuestaoAtual++;
        carregarQuestaoAtual();
    }
}

async function finalizarSimulado() {
    try {
        console.log("Finalizando simulado", simuladoAtual.id, respostasDoUsuario);
        const resultadoSimulado = await api.post(`/simulados/${simuladoAtual.id}/finalizar`, {
            respostas: respostasDoUsuario,
        });

        const acertos = resultadoSimulado.itens.filter((i) => i.acerto).length;
        const total = resultadoSimulado.itens.length;
        const nota = resultadoSimulado.resultado.nota;

        document.getElementById("resultado-nota").textContent = nota;
        document.getElementById("resultado-acertos").textContent = `${acertos}/${total}`;
        document.getElementById("resultado-titulo").textContent =
            nota >= resultadoSimulado.pontuacao_max * 0.7 ? "Aprovado! 🎉" : "Continue estudando";

        navigateTo("screen-result");
    } catch (erro) {
        console.error("Erro ao finalizar simulado:", erro);
        const divErroQuiz = document.getElementById("quiz-mensagem-erro");
        if (divErroQuiz) {
            divErroQuiz.textContent = erro.message;
        } else {
            alert(erro.message);
        }
    }
}

// ==========================================
// HISTÓRICO DE SIMULADOS (GET /simulados/historico)
// ==========================================
async function carregarHistorico() {
    const divEstatisticas = document.getElementById("historico-estatisticas");
    const divLista = document.getElementById("historico-lista");

    try {
        const dados = await api.get("/simulados/historico");
        const est = dados.estatisticas;

        divEstatisticas.innerHTML = `
            <div class="stat-box">
                <span class="stat-value">${est.media}</span>
                <span class="stat-label">Média</span>
            </div>
            <div class="stat-box">
                <span class="stat-value">${est.melhor}</span>
                <span class="stat-label">Melhor nota</span>
            </div>
            <div class="stat-box">
                <span class="stat-value">${est.total_simulados}</span>
                <span class="stat-label">Simulados feitos</span>
            </div>
        `;

        if (dados.simulados.length === 0) {
            divLista.innerHTML = "<p>Você ainda não finalizou nenhum simulado.</p>";
            return;
        }

        divLista.innerHTML = "";
        dados.simulados.forEach((sim) => {
            const data = new Date(sim.data_realizacao).toLocaleDateString("pt-BR");
            const div = document.createElement("div");
            div.className = "trail-card";
            div.onclick = () => verDetalhesSimulado(sim.id);
            div.innerHTML = `
                <div class="trail-info">
                    <h4>${sim.titulo}</h4>
                    <p>${data} — Nota: ${sim.resultado ? sim.resultado.nota : "-"}</p>
                </div>
            `;
            divLista.appendChild(div);
        });
    } catch (erro) {
        divLista.innerHTML = `<p style="color:#e53e3e;">${erro.message}</p>`;
    }
}

// ==========================================
// DETALHES DE UM SIMULADO (GET /simulados/<id>)
// Cada simulado só pode ser visto pelo próprio dono — se o token for
// de outro usuário, a API responde 403 e mostramos "Acesso negado".
// ==========================================
async function verDetalhesSimulado(simuladoId) {
    const divTitulo = document.getElementById("detalhe-titulo");
    const divConteudo = document.getElementById("detalhe-conteudo");

    divTitulo.textContent = "Carregando...";
    divConteudo.innerHTML = "";
    navigateTo("screen-detalhe-simulado");

    try {
        const sim = await api.get(`/simulados/${simuladoId}`);
        const data = new Date(sim.data_realizacao).toLocaleDateString("pt-BR");

        divTitulo.textContent = sim.titulo;
        divConteudo.innerHTML = `
            <p><strong>Data:</strong> ${data}</p>
            <p><strong>Nota:</strong> ${sim.resultado ? sim.resultado.nota : "-"} / ${sim.pontuacao_max}</p>
            <p><strong>Questões respondidas:</strong> ${sim.itens.length}</p>
        `;
    } catch (erro) {
        if (erro.message.includes("permissão")) {
            divTitulo.textContent = "🚫 Acesso negado";
            divConteudo.innerHTML = `
                <p style="color:#e53e3e; font-weight:600;">
                    Este simulado não pertence à sua conta.<br>
                    Cada aluno só pode ver os próprios simulados.
                </p>
            `;
        } else {
            divTitulo.textContent = "Erro";
            divConteudo.innerHTML = `<p style="color:#e53e3e;">${erro.message}</p>`;
        }
    }
}

// ==========================================
// Inicialização da página
// ==========================================
document.addEventListener("DOMContentLoaded", async () => {
    const formPerfil = document.getElementById("form-perfil");
    if (formPerfil) formPerfil.addEventListener("submit", salvarPerfil);

    await carregarUsuario();
    await carregarTrilhas();
    await carregarHistorico();
});
