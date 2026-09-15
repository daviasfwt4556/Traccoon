// ==========================================
// Proteção de tela para as páginas "Gerir ..." (admin_*.html).
// O backend já bloqueia essas rotas para quem não é administrador
// (retorna 403); este script só evita que a pessoa fique presa numa
// tela cujos botões nunca vão funcionar para ela — redireciona de volta
// ao painel com um aviso.
// ==========================================
(async function protegerPaginaAdmin() {
    if (!estaLogado()) {
        window.location.href = "../index.html";
        return;
    }

    try {
        const usuario = await api.get("/auth/me");
        if (!usuario.is_admin) {
            alert("Esta área é restrita a administradores.");
            window.location.href = "painel.html";
        }
    } catch (erro) {
        removerToken();
        window.location.href = "../index.html";
    }
})();
