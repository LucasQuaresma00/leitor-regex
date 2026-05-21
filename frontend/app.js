// app.js - Versão Melhorada
let dadosGlobais = [];

async function carregarDados() {
    try {
        const resposta = await fetch("../saida/resultados_gerais.json");
        const dados = await resposta.json();

        dadosGlobais = dados.ocorrencias || [];
        
        preencherSeletorArquivos();
        preencherSeletorTipos();
        renderizarDashboard();

    } catch (erro) {
        console.error("Erro ao carregar JSON:", erro);
        document.getElementById("cards-container").innerHTML = 
            `<p style="color:red;">Erro ao carregar dados. Verifique se o arquivo resultados_gerais.json existe na pasta 'saida'.</p>`;
    }
}

/* ========================= */
/* FILTROS */
/* ========================= */

function preencherSeletorArquivos() {
    const seletor = document.getElementById("seletor-arquivo");
    const arquivos = [...new Set(dadosGlobais.map(o => o.arquivo))];

    seletor.innerHTML = '<option value="">Todos os arquivos</option>';
    
    arquivos.forEach(arquivo => {
        const option = document.createElement("option");
        option.value = arquivo;
        option.textContent = arquivo;
        seletor.appendChild(option);
    });

    seletor.addEventListener("change", renderizarDashboard);
}

function preencherSeletorTipos() {
    const seletor = document.getElementById("seletor-tipo");
    const tipos = [...new Set(dadosGlobais.map(o => o.tipo))];

    seletor.innerHTML = '<option value="">Todos os tipos</option>';
    
    tipos.forEach(tipo => {
        const option = document.createElement("option");
        option.value = tipo;
        option.textContent = tipo.toUpperCase();
        seletor.appendChild(option);
    });

    seletor.addEventListener("change", renderizarDashboard);
}

/* ========================= */
/* RENDERIZAÇÃO PRINCIPAL */
/* ========================= */

function renderizarDashboard() {
    const arquivoSelecionado = document.getElementById("seletor-arquivo").value;
    const tipoSelecionado = document.getElementById("seletor-tipo").value;

    let filtrados = dadosGlobais;

    if (arquivoSelecionado) {
        filtrados = filtrados.filter(o => o.arquivo === arquivoSelecionado);
    }
    if (tipoSelecionado) {
        filtrados = filtrados.filter(o => o.tipo === tipoSelecionado);
    }

    mostrarEstatisticas(filtrados);
    mostrarOcorrencias(filtrados);
}

/* ========================= */
/* ESTATÍSTICAS */
/* ========================= */

function mostrarEstatisticas(ocorrencias) {
    const container = document.getElementById("cards-container");
    container.innerHTML = "";

    const totais = {};
    const validos = {};
    const invalidos = {};

    ocorrencias.forEach(o => {
        const tipo = o.tipo;
        if (!totais[tipo]) {
            totais[tipo] = 0;
            validos[tipo] = 0;
            invalidos[tipo] = 0;
        }
        totais[tipo]++;
        if (o.classificacao === "valido") validos[tipo]++;
        if (o.classificacao === "invalido") invalidos[tipo]++;
    });

    for (const tipo in totais) {
        const card = document.createElement("div");
        card.classList.add("card");
        card.innerHTML = `
            <h3>${tipo.toUpperCase()}</h3>
            <p><strong>Total:</strong> ${totais[tipo]}</p>
            <p class="valido"><strong>Válidos:</strong> ${validos[tipo]}</p>
            <p class="invalido"><strong>Inválidos:</strong> ${invalidos[tipo]}</p>
        `;
        container.appendChild(card);
    }
}

/* ========================= */
/* OCORRÊNCIAS */
/* ========================= */

function mostrarOcorrencias(ocorrencias) {
    const container = document.getElementById("ocorrencias-container");
    container.innerHTML = "";

    const agrupados = {};

    ocorrencias.forEach(o => {
        const tipo = o.tipo;
        if (!agrupados[tipo]) {
            agrupados[tipo] = { validos: [], invalidos: [], outros: [] };
        }

        if (o.classificacao === "valido") {
            agrupados[tipo].validos.push(o);
        } else if (o.classificacao === "invalido") {
            agrupados[tipo].invalidos.push(o);
        } else {
            agrupados[tipo].outros.push(o);
        }
    });

    for (const tipo in agrupados) {
        const dados = agrupados[tipo];
        const secao = document.createElement("div");
        secao.classList.add("secao-tipo");

        secao.innerHTML = `
            <h3>${tipo.toUpperCase()} 
                <span class="contagem">(${dados.validos.length + dados.invalidos.length + dados.outros.length})</span>
            </h3>
            <div class="grupo-ocorrencias">
                <div class="bloco-validos">
                    <h4>Válidos (${dados.validos.length})</h4>
                    ${gerarLista(dados.validos.slice(0, 6))}
                </div>
                <div class="bloco-invalidos">
                    <h4>Inválidos (${dados.invalidos.length})</h4>
                    ${gerarLista(dados.invalidos.slice(0, 6))}
                </div>
            </div>
        `;
        container.appendChild(secao);
    }
}

function gerarLista(lista) {
    if (!lista.length) return "<p class='sem-dados'>Nenhum item</p>";

    return `
        <ul>
            ${lista.map(item => `
                <li>
                    <strong>${item.valor}</strong><br>
                    <small>${item.arquivo}</small>
                </li>
            `).join("")}
        </ul>
    `;
}

// Inicialização
carregarDados();
