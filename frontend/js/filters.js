import {
    renderTable
} from "./table.js";

export function initializeFilters(data) {

    const typeFilter = document.getElementById(
        "type-filter"
    );

    const searchInput = document.getElementById(
        "search-input"
    );

    const statusFilter = document.getElementById(
        "status-filter"
    );

    const types = [
        ...new Set(
            data.map(item => item.tipo)
        )
    ];

    types.forEach(type => {

        const option =
            document.createElement("option");

        option.value = type;

        option.textContent = type;

        typeFilter.appendChild(option);
    });

    function applyFilters() {

        const search =
            searchInput.value.toLowerCase();

        const type =
            typeFilter.value;

        const status =
            statusFilter.value;

        const filtered = data.filter(item => {

            const matchesSearch =
                item.valor_normalizado
                    .toLowerCase()
                    .includes(search);

            const matchesType =
                !type ||
                item.tipo === type;

            const matchesStatus =
                !status ||
                item.status_final === status;

            return (
                matchesSearch &&
                matchesType &&
                matchesStatus
            );
        });

        renderTable(filtered);
    }

    searchInput.addEventListener(
        "input",
        applyFilters
    );

    typeFilter.addEventListener(
        "change",
        applyFilters
    );

    statusFilter.addEventListener(
        "change",
        applyFilters
    );
}