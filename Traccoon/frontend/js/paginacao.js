/**
 * Helper compartilhado pelas telas de administração para desenhar os
 * controles de "página anterior / próxima página" a partir da resposta
 * paginada da API (formato: { itens, pagina_atual, total_paginas, total_itens }).
 *
 * Uso típico em um admin_*.js:
 *
 *   let paginaAtual = 1;
 *   const POR_PAGINA = 20;
 *
 *   async function carregar(pagina = 1) {
 *       const dados = await api.get(`/usuarios/?pagina=${pagina}&por_pagina=${POR_PAGINA}`);
 *       renderizarLinhas(dados.itens);
 *       paginaAtual = dados.pagina_atual;
 *       renderizarPaginacao("paginacao-usuarios", dados, carregar);
 *   }
 */
function renderizarPaginacao(idContainer, dadosPaginados, aoMudarPagina) {
    const container = document.getElementById(idContainer);
    if (!container) return;

    const { pagina_atual, total_paginas, total_itens } = dadosPaginados;

    if (!total_paginas || total_paginas <= 1) {
        container.innerHTML = "";
        return;
    }

    container.innerHTML = "";
    container.className = "paginacao";

    const botaoAnterior = document.createElement("button");
    botaoAnterior.type = "button";
    botaoAnterior.textContent = "‹ Anterior";
    botaoAnterior.disabled = pagina_atual <= 1;
    botaoAnterior.addEventListener("click", () => aoMudarPagina(pagina_atual - 1));

    const info = document.createElement("span");
    info.className = "paginacao-info";
    info.textContent = `Página ${pagina_atual} de ${total_paginas} (${total_itens} no total)`;

    const botaoProxima = document.createElement("button");
    botaoProxima.type = "button";
    botaoProxima.textContent = "Próxima ›";
    botaoProxima.disabled = pagina_atual >= total_paginas;
    botaoProxima.addEventListener("click", () => aoMudarPagina(pagina_atual + 1));

    container.appendChild(botaoAnterior);
    container.appendChild(info);
    container.appendChild(botaoProxima);
}
