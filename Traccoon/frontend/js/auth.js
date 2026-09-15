// ==========================================
// Cadastro e login reais (senha com hash no backend,
// token de autenticação salvo no localStorage)
// ==========================================

async function cadastrarUsuario() {
    const nome = document.getElementById("cadastro-nome").value.trim();
    const email = document.getElementById("cadastro-email").value.trim();
    const senha = document.getElementById("cadastro-senha").value;
    const msg = document.getElementById("cadastro-mensagem");
    msg.textContent = "";

    try {
        const resposta = await api.post("/auth/registro", { nome, email, senha });
        definirToken(resposta.token);
        window.location.href = "paginas/painel.html";
    } catch (erro) {
        msg.textContent = erro.message;
    }
}

async function entrar() {
    const email = document.getElementById("login-email").value.trim();
    const senha = document.getElementById("login-senha").value;
    const msg = document.getElementById("login-mensagem");
    msg.textContent = "";

    try {
        const resposta = await api.post("/auth/login", { email, senha });
        definirToken(resposta.token);
        window.location.href = "paginas/painel.html";
    } catch (erro) {
        msg.textContent = erro.message;
    }
}

// Se a pessoa já estiver logada e abrir a tela de boas-vindas de novo,
// manda ela direto pro painel em vez de mostrar login/cadastro.
document.addEventListener("DOMContentLoaded", () => {
    if (estaLogado()) {
        window.location.href = "paginas/painel.html";
    }
});
