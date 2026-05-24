export function renderTypeChart(data) {

    const counter = {};

    data.forEach(item => {
        counter[item.tipo] = (counter[item.tipo] || 0) + 1;
    });

    new Chart(document.getElementById("typeChart"), {

        type: "bar",

        data: {

            labels: Object.keys(counter),

            datasets: [{

                data: Object.values(counter),

                backgroundColor: [
                    "#0ea5e9",
                    "#eab308",
                    "#9333ea",
                    "#14b8a6",
                    "#f97316",
                    "#8b5cf6",
                    "#ec4899",
                    "#a5704b"
                ]
            }],
        },

        options: {
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

export function renderStatusChart(data) {

    const valid =
        data.filter(d => d.status_final === "valido").length;

    const invalid =
        data.filter(d => d.status_final === "invalido").length;

    new Chart(document.getElementById("statusChart"), {

        type: "doughnut",

        data: {

            labels: ["Válidos", "Inválidos"],

            datasets: [{

                data: [valid, invalid],

                backgroundColor: [
                    "#42d392",
                    "#ff6b6b"
                ]
            }],
        },
    });
}