export function renderTypeChart(data) {

    const counter = {};

    data.forEach(item => {

        counter[item.tipo] =
            (counter[item.tipo] || 0) + 1;
    });

    new Chart(

        document.getElementById("typeChart"),

        {
            type: "bar",

            data: {

                labels: Object.keys(counter),

                datasets: [
                    {
                        label: "Ocorrências",

                        data: Object.values(counter),
                    }
                ]
            }
        }
    );
}

export function renderStatusChart(data) {

    const valid = data.filter(
        item =>
            item.status_final === "valido"
    ).length;

    const invalid = data.filter(
        item =>
            item.status_final === "invalido"
    ).length;

    new Chart(

        document.getElementById("statusChart"),

        {
            type: "doughnut",

            data: {

                labels: [
                    "Válidos",
                    "Inválidos"
                ],

                datasets: [
                    {
                        data: [
                            valid,
                            invalid
                        ]
                    }
                ]
            }
        }
    );
}