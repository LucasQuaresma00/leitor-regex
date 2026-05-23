export function renderTable(data) {
    const tbody = document.getElementById("occurrences-table");
    tbody.innerHTML = "";

    data.slice(0, 300).forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.tipo}</td>
            <td>${item.valor_normalizado}</td>
            <td>${item.arquivo}</td>
            <td class="${item.status_final}">${item.status_final}</td>
            <td>${item.confianca}</td>
        `;
        tbody.appendChild(tr);
    });
}
