import { renderTypeChart, renderStatusChart } from "./js/charts.js";
import { renderTable }                        from "./js/table.js";
import { initializeFilters }                  from "./js/filters.js";

const response    = await fetch("../output/resultados.json");
const occurrences = await response.json();

updateCards(occurrences);
renderTypeChart(occurrences);
renderStatusChart(occurrences);
renderTable(occurrences);
initializeFilters(occurrences);

function updateCards(data) {
    const total   = data.length;
    const valid   = data.filter(d => d.status_final === "valido").length;
    const invalid = data.filter(d => d.status_final === "invalido").length;
    const rate    = total ? ((invalid / total) * 100).toFixed(2) : "0.00";

    document.getElementById("total-occurrences").textContent = total.toLocaleString();
    document.getElementById("valid-count").textContent       = valid.toLocaleString();
    document.getElementById("invalid-count").textContent     = invalid.toLocaleString();
    document.getElementById("inconsistency-rate").textContent = `${rate}%`;
}
