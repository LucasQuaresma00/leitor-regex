import {
    renderTypeChart,
    renderStatusChart
} from "./js/charts.js";

import {
    renderTable
} from "./js/table.js";

import {
    initializeFilters
} from "./js/filters.js";

const response = await fetch(
    "../output/resultados.json"
);

const occurrences = await response.json();

initializeDashboard(occurrences);

function initializeDashboard(data) {

    updateCards(data);

    renderTypeChart(data);

    renderStatusChart(data);

    renderTable(data);

    initializeFilters(data);
}

function updateCards(data) {

    const total = data.length;

    const valid = data.filter(
        item =>
            item.status_final === "valido"
    ).length;

    const invalid = data.filter(
        item =>
            item.status_final === "invalido"
    ).length;

    const rate =
        ((invalid / total) * 100).toFixed(2);

    document.getElementById(
        "total-occurrences"
    ).textContent = total.toLocaleString();

    document.getElementById(
        "valid-count"
    ).textContent = valid.toLocaleString();

    document.getElementById(
        "invalid-count"
    ).textContent = invalid.toLocaleString();

    document.getElementById(
        "inconsistency-rate"
    ).textContent = `${rate}%`;
}