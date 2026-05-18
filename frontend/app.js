let dadosGlobais = [];

async function carregarDados() {

    try {

        const resposta = await fetch(
            "../saida/resultados_gerais.json"
        );

        const dados = await resposta.json();

        dadosGlobais = dados.ocorrencias;

        preencherSeletor(dadosGlobais);

    } catch (erro) {

        console.error("Erro ao carregar JSON:", erro);
    }
}

/* ========================= */
/* SELETOR DE ARQUIVOS */
/* ========================= */

function preencherSeletor(ocorrencias) {

    const seletor = document.getElementById(
        "seletor-arquivo"
    );

    const arquivos = [
        ...new Set(
            ocorrencias.map(o => o.arquivo)
        )
    ];

    seletor.innerHTML = "";

    arquivos.forEach(arquivo => {

        const option = document.createElement("option");

        option.value = arquivo;
        option.textContent = arquivo;

        seletor.appendChild(option);
    });

    // render inicial com o primeiro arquivo
    renderizarPorArquivo(seletor.value);

    seletor.addEventListener(
        "change",
        (e) => renderizarPorArquivo(e.target.value)
    );
}

/* ========================= */
/* RENDER PRINCIPAL */
/* ========================= */

function renderizarPorArquivo(arquivoSelecionado) {

    const filtrados = dadosGlobais.filter(
        o => o.arquivo === arquivoSelecionado
    );

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

        if (o.classificacao === "valido") {
            validos[tipo]++;
        }

        if (o.classificacao === "invalido") {
            invalidos[tipo]++;
        }
    });

    for (const tipo in totais) {

        const card = document.createElement("div");

        card.classList.add("card");

        card.innerHTML = `
            <h3>${tipo.toUpperCase()}</h3>

            <p><strong>Total:</strong> ${totais[tipo]}</p>
            <p><strong>Válidos:</strong> ${validos[tipo]}</p>
            <p><strong>Inválidos:</strong> ${invalidos[tipo]}</p>
        `;

        container.appendChild(card);
    }
}

/* ========================= */
/* OCORRÊNCIAS */
/* ========================= */

function mostrarOcorrencias(ocorrencias) {

    const container = document.getElementById(
        "ocorrencias-container"
    );

    container.innerHTML = "";

    const agrupados = {};

    ocorrencias.forEach(o => {

        const tipo = o.tipo;

        if (
            o.classificacao !== "valido" &&
            o.classificacao !== "invalido"
        ) return;

        if (!agrupados[tipo]) {
            agrupados[tipo] = {
                validos: [],
                invalidos: []
            };
        }

        if (o.classificacao === "valido") {
            agrupados[tipo].validos.push(o);
        } else {
            agrupados[tipo].invalidos.push(o);
        }
    });

    for (const tipo in agrupados) {

        const dados = agrupados[tipo];

        const secao = document.createElement("div");

        secao.classList.add("secao-tipo");

        secao.innerHTML = `
            <h3>${tipo.toUpperCase()}</h3>

            <div class="grupo-ocorrencias">

                <div class="bloco-validos">

                    <h4>Válidos (${dados.validos.length})</h4>

                    ${gerarLista(dados.validos.slice(0, 5))}

                </div>

                <div class="bloco-invalidos">

                    <h4>Inválidos (${dados.invalidos.length})</h4>

                    ${gerarLista(dados.invalidos.slice(0, 5))}

                </div>

            </div>
        `;

        container.appendChild(secao);
    }
}

/* ========================= */
/* LISTA AUXILIAR */
/* ========================= */

function gerarLista(lista) {

    if (!lista.length) {
        return "<p>Nenhum item</p>";
    }

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

/* ========================= */

carregarDados();