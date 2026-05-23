import { renderTable } from "./table.js";

export function initializeFilters(data) {
    const searchInput  = document.getElementById("search-input");
    const typeFilter   = document.getElementById("type-filter");
    const statusFilter = document.getElementById("status-filter");

    // Popula o select de tipos dinamicamente
    [...new Set(data.map(d => d.tipo))].forEach(tipo => {
        const opt = document.createElement("option");
        opt.value = opt.textContent = tipo;
        typeFilter.appendChild(opt);
    });

    function applyFilters() {
        const search = searchInput.value.toLowerCase();
        const type   = typeFilter.value;
        const status = statusFilter.value;

        const filtered = data.filter(item =>
            item.valor_normalizado.toLowerCase().includes(search) &&
            (!type   || item.tipo        === type)   &&
            (!status || item.status_final === status)
        );

        renderTable(filtered);
    }

    searchInput.addEventListener("input",  applyFilters);
    typeFilter.addEventListener("change",  applyFilters);
    statusFilter.addEventListener("change", applyFilters);
}
