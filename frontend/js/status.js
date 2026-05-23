export function getFinalStatus(item) {

    const estrutural =
        item.status_final;

    const semantica =
        item.validacao_semantica;

    // ==================================
    // INVÁLIDO ESTRUTURAL
    // ==================================

    if (estrutural === "invalido") {

        return "invalido";
    }

    // ==================================
    // INVÁLIDO SEMÂNTICO
    // ==================================

    if (semantica === "invalido") {

        return "invalido";
    }

    // ==================================
    // CASOS RESTANTES
    // ==================================

    return "valido";
}