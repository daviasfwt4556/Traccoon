// ==========================================
// Configuração central da API
// A API roda separada do frontend (Flask + CORS),
// por isso toda chamada usa a URL completa.
// ==========================================
const API_URL = "http://127.0.0.1:5000";

// Wrapper simples em volta do fetch: já monta a URL, já manda o token
// de autenticação (se existir) e já lança erro com a mensagem da API.
async function apiRequest(caminho, opcoes = {}) {
    const cabecalhos = { "Content-Type": "application/json" };
    const token = obterToken();
    if (token) cabecalhos["Authorization"] = `Bearer ${token}`;

    let resposta;
    try {
        resposta = await fetch(`${API_URL}${caminho}`, {
            headers: cabecalhos,
            ...opcoes,
        });
    } catch (erroDeRede) {
        // O fetch só cai aqui quando a requisição nem chega a acontecer de
        // verdade: sem internet, servidor fora do ar, DNS falhou, etc.
        // Qualquer erro de validação normal da API (400, 401, 404...) NÃO
        // passa por aqui — só entra no catch(!resposta.ok) lá embaixo.
        if (typeof mostrarToast === "function") {
            mostrarToast(
                "Não foi possível conectar ao servidor. Verifique sua internet.",
                "erro"
            );
        }
        throw new Error("Falha de conexão com o servidor.");
    }

    if (resposta.status === 204) return null;

    const dados = await resposta.json().catch(() => null);

    if (!resposta.ok) {
        const mensagem = (dados && dados.erro) || "Erro ao comunicar com a API.";

        // Sessão expirada/token inválido: avisa com um toast específico,
        // já que isso costuma pegar o usuário de surpresa no meio de uma ação.
        if (resposta.status === 401 && typeof mostrarToast === "function") {
            mostrarToast("Sua sessão expirou. Faça login novamente.", "aviso");
        }

        throw new Error(mensagem);
    }

    return dados;
}

const api = {
    get: (caminho) => apiRequest(caminho),
    post: (caminho, corpo) => apiRequest(caminho, { method: "POST", body: JSON.stringify(corpo) }),
    put: (caminho, corpo) => apiRequest(caminho, { method: "PUT", body: JSON.stringify(corpo) }),
    delete: (caminho) => apiRequest(caminho, { method: "DELETE" }),
};

// ==========================================
// Autenticação: token guardado no localStorage do navegador.
// O backend nunca usa cookie/sessão — cada requisição manda o token
// no cabeçalho Authorization (feito automaticamente acima).
// ==========================================
function obterToken() {
    return localStorage.getItem("autotrans-token");
}

function definirToken(token) {
    localStorage.setItem("autotrans-token", token);
}

function removerToken() {
    localStorage.removeItem("autotrans-token");
}

function estaLogado() {
    return !!obterToken();
}
