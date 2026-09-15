/**
 * Sistema global de notificações "toast".
 *
 * Carregado antes de api.js em todas as páginas. Não precisa de nenhum
 * HTML extra: o container é criado dinamicamente na primeira vez que
 * uma mensagem é mostrada.
 *
 * Uso em qualquer outro arquivo JS:
 *   mostrarToast("Usuário criado com sucesso!", "sucesso");
 *   mostrarToast("Não foi possível salvar.", "erro");
 *   mostrarToast("Verifique os campos.", "aviso");
 */

function obterContainerDeToasts() {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        container.setAttribute("aria-live", "polite");
        document.body.appendChild(container);
    }
    return container;
}

function mostrarToast(mensagem, tipo = "info", duracaoMs = 4000) {
    const container = obterContainerDeToasts();

    const toast = document.createElement("div");
    toast.className = `toast toast-${tipo}`;
    toast.setAttribute("role", "status");

    const icones = {
        sucesso: "✓",
        erro: "✕",
        aviso: "!",
        info: "i",
    };

    toast.innerHTML = `
        <span class="toast-icone">${icones[tipo] || icones.info}</span>
        <span class="toast-texto"></span>
        <button type="button" class="toast-fechar" aria-label="Fechar notificação">&times;</button>
    `;
    toast.querySelector(".toast-texto").textContent = mensagem;

    function remover() {
        toast.classList.add("toast-saindo");
        // Espera a animação de saída (250ms no CSS) antes de tirar do DOM.
        setTimeout(() => toast.remove(), 250);
    }

    toast.querySelector(".toast-fechar").addEventListener("click", remover);
    const temporizador = setTimeout(remover, duracaoMs);
    toast.addEventListener("mouseenter", () => clearTimeout(temporizador));

    container.appendChild(toast);
}

// Deixa disponível pra outros scripts (mesmo sem módulos ES, já que o
// projeto todo usa <script> simples).
window.mostrarToast = mostrarToast;
