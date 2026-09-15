async function carregarCategoriasParaMaterial() {
    const container = document.getElementById("lista-categorias-material");
    try {
        const categorias = await api.get("/categorias/");
        container.innerHTML = "";
        categorias.forEach((categoria) => {
            const btn = document.createElement("button");
            btn.className = "menu-btn";
            btn.style.marginRight = "8px";
            btn.style.marginBottom = "8px";
            btn.textContent = categoria.nome;
            btn.onclick = () => carregarMateriaisDaCategoria(categoria.id, categoria.nome);
            container.appendChild(btn);
        });
    } catch (erro) {
        container.innerHTML = `<p style="color:#e53e3e;">${erro.message}</p>`;
    }
}

async function carregarMateriaisDaCategoria(categoriaId, nomeCategoria) {
    const container = document.getElementById("conteudo-materiais");
    container.innerHTML = "<p>Carregando...</p>";

    try {
        const materiais = await api.get(`/materiais/?categoria_id=${categoriaId}`);

        if (materiais.length === 0) {
            container.innerHTML = `<p>Nenhum material cadastrado para <strong>${nomeCategoria}</strong> ainda.</p>`;
            return;
        }

        container.innerHTML = `<h3 style="text-align:left;">${nomeCategoria}</h3>`;
        materiais.forEach((material) => {
            const div = document.createElement("div");
            div.className = "card";
            div.style.textAlign = "left";
            div.style.marginBottom = "15px";
            div.innerHTML = `
                <p style="text-align:left;">${material.conteudo}</p>
                ${material.url ? `<a href="${material.url}" target="_blank" rel="noopener">Saiba mais →</a>` : ""}
            `;
            container.appendChild(div);
        });
    } catch (erro) {
        container.innerHTML = `<p style="color:#e53e3e;">${erro.message}</p>`;
    }
}

document.addEventListener("DOMContentLoaded", carregarCategoriasParaMaterial);
