"""
statistics.py — Consolidação estatística do pipeline Regex.

Responsabilidades:
──────────────────────────────────────────────
- Estatísticas gerais de extração
- Distribuição por tipo
- Distribuição por arquivo
- Taxa de inconsistência
- Frequência de valores
- Distribuição contextual
- Distribuição estrutural das linhas
- Métricas de qualidade

Baseado nos pontos fortes:
──────────────────────────────────────────────
Projeto A:
✅ Dataclasses
✅ Estatísticas avançadas
✅ Top valores
✅ Distribuição estrutural

Projeto B:
✅ Simplicidade
✅ Estrutura clara
✅ Boa organização quantitativa

Objetivo:
──────────────────────────────────────────────
Fornecer observabilidade do pipeline Regex
sem fugir do escopo do trabalho.
"""

from __future__ import annotations

import re
import logging

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from src.modules.extractor import Occurrence

logger = logging.getLogger("statistics")


# ──────────────────────────────────────────────
# CLASSIFICAÇÃO ESTRUTURAL DE LINHAS
# ──────────────────────────────────────────────

LINE_TYPE_PATTERNS = {

    # ==========================================
    # LOGS
    # ==========================================

    "log_entry": re.compile(
        r"\[(INFO|WARN|ERROR|DEBUG)\]"
    ),

    # ==========================================
    # CHAT
    # ==========================================

    "chat_message": re.compile(
        r"^\[\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}"
    ),

    # ==========================================
    # CSV
    # ==========================================

    "csv_row": re.compile(
        r"^[^;,\n]+[;,][^;,\n]+[;,]"
    ),

    # ==========================================
    # URL / ACESSO
    # ==========================================

    "access_line": re.compile(
        r"https?://|login|acesso"
    ),

    # ==========================================
    # CONTATO
    # ==========================================

    "contact_line": re.compile(
        r"email|telefone|celular|fone"
    ),

    # ==========================================
    # CLIENTE
    # ==========================================

    "client_line": re.compile(
        r"cpf|cliente|cadastro"
    ),

    # ==========================================
    # LINHA EM BRANCO
    # ==========================================

    "blank": re.compile(
        r"^\s*$"
    ),
}


def classify_line(line: str) -> str:
    """
    Classifica estruturalmente uma linha.

    Utilizado apenas para estatísticas
    e análise quantitativa.
    """

    for line_type, pattern in LINE_TYPE_PATTERNS.items():

        if pattern.search(line):
            return line_type

    return "outros"


# ──────────────────────────────────────────────
# MODELO DE ESTATÍSTICAS
# ──────────────────────────────────────────────

@dataclass(slots=True)
class Statistics:

    # ==========================================
    # GERAIS
    # ==========================================

    total_occurrences: int = 0
    total_lines_processed: int = 0

    # ==========================================
    # DISTRIBUIÇÕES
    # ==========================================

    by_type: dict[str, int] = field(
        default_factory=dict
    )

    by_context: dict[str, int] = field(
        default_factory=dict
    )

    by_file: dict[str, dict[str, int]] = field(
        default_factory=dict
    )

    line_type_distribution: dict[str, int] = field(
        default_factory=dict
    )

    # ==========================================
    # VALIDAÇÃO
    # ==========================================

    valid_by_type: dict[str, int] = field(
        default_factory=dict
    )

    invalid_by_type: dict[str, int] = field(
        default_factory=dict
    )

    semantic_invalid_by_type: dict[str, int] = field(
        default_factory=dict
    )

    # ==========================================
    # QUALIDADE
    # ==========================================

    inconsistency_rate: float = 0.0
    structural_valid_rate: float = 0.0
    semantic_valid_rate: float = 0.0

    # ==========================================
    # FREQUÊNCIA
    # ==========================================

    top_values: dict[
        str,
        list[tuple[str, int]]
    ] = field(default_factory=dict)

    # ==========================================
    # CONFIANÇA
    # ==========================================

    average_confidence: float = 0.0


# ──────────────────────────────────────────────
# ESTATÍSTICAS PRINCIPAIS
# ──────────────────────────────────────────────

def compute_statistics(
    occurrences: list[Occurrence],
    files_lines: dict[str, list[str]],
) -> Statistics:
    """
    Calcula estatísticas completas do pipeline.
    """

    stats = Statistics()

    # ==========================================
    # GERAIS
    # ==========================================

    stats.total_occurrences = len(
        occurrences
    )

    stats.total_lines_processed = sum(
        len(lines)
        for lines in files_lines.values()
    )

    # ==========================================
    # TOTAL POR TIPO
    # ==========================================

    type_counter = Counter(
        occ.pattern_name
        for occ in occurrences
    )

    stats.by_type = dict(
        type_counter
    )

    # ==========================================
    # TOTAL POR CONTEXTO
    # ==========================================

    context_counter = Counter(
        occ.detected_context
        for occ in occurrences
    )

    stats.by_context = dict(
        context_counter
    )

    # ==========================================
    # VALIDAÇÕES
    # ==========================================

    for occ in occurrences:

        pattern_name = occ.pattern_name

        # --------------------------------------
        # Status estrutural
        # --------------------------------------

        if occ.structural_status == "valido":

            stats.valid_by_type[
                pattern_name
            ] = (
                stats.valid_by_type.get(
                    pattern_name,
                    0
                ) + 1
            )

        elif occ.structural_status == "invalido":

            stats.invalid_by_type[
                pattern_name
            ] = (
                stats.invalid_by_type.get(
                    pattern_name,
                    0
                ) + 1
            )

        # --------------------------------------
        # Status semântico
        # --------------------------------------

        if occ.semantic_status == "invalido":

            stats.semantic_invalid_by_type[
                pattern_name
            ] = (
                stats.semantic_invalid_by_type.get(
                    pattern_name,
                    0
                ) + 1
            )

            # ==================================
            # INVALIDAÇÃO FINAL
            # ==================================

            stats.valid_by_type[
                pattern_name
            ] -= 1

            stats.invalid_by_type[
                pattern_name
            ] = (
                stats.invalid_by_type.get(
                    pattern_name,
                    0
                ) + 1
            )

    # ==========================================
    # DISTRIBUIÇÃO POR ARQUIVO
    # ==========================================

    by_file = defaultdict(Counter)

    for occ in occurrences:

        by_file[
            occ.filename
        ][
            occ.pattern_name
        ] += 1

    stats.by_file = {

        filename: dict(counter)

        for filename, counter in (
            by_file.items()
        )
    }

    # ==========================================
    # TOP VALORES
    # ==========================================

    value_counter = defaultdict(Counter)

    for occ in occurrences:

        value_counter[
            occ.pattern_name
        ][
            occ.normalized_value
        ] += 1

    stats.top_values = {

        pattern_name: counter.most_common(10)

        for pattern_name, counter in (
            value_counter.items()
        )
    }

    # ==========================================
    # TAXA DE INCONSISTÊNCIA
    # ==========================================

    total_invalid = sum(
        stats.invalid_by_type.values()
    )

    if stats.total_occurrences > 0:

        stats.inconsistency_rate = round(
            (
                total_invalid
                / stats.total_occurrences
            ) * 100,
            2
        )

    # ==========================================
    # TAXA ESTRUTURAL
    # ==========================================

    total_valid_structural = sum(
        stats.valid_by_type.values()
    )

    if stats.total_occurrences > 0:

        stats.structural_valid_rate = round(
            (
                total_valid_structural
                / stats.total_occurrences
            ) * 100,
            2
        )

    # ==========================================
    # TAXA SEMÂNTICA
    # ==========================================

    semantic_invalid = sum(
        stats.semantic_invalid_by_type.values()
    )

    semantic_valid = (
        stats.total_occurrences
        - semantic_invalid
    )

    if stats.total_occurrences > 0:

        stats.semantic_valid_rate = round(
            (
                semantic_valid
                / stats.total_occurrences
            ) * 100,
            2
        )

    # ==========================================
    # CONFIANÇA MÉDIA
    # ==========================================

    if occurrences:

        stats.average_confidence = round(

            sum(
                occ.confidence
                for occ in occurrences
            )
            /
            len(occurrences),

            2
        )

    # ==========================================
    # DISTRIBUIÇÃO DE LINHAS
    # ==========================================

    line_distribution = Counter()

    for lines in files_lines.values():

        for line in lines:

            line_type = classify_line(
                line
            )

            line_distribution[
                line_type
            ] += 1

    stats.line_type_distribution = dict(
        line_distribution
    )

    logger.info(
        (
            "Estatísticas calculadas | "
            "ocorrências=%d | "
            "inconsistência=%.2f%% | "
            "confiança=%.2f"
        ),
        stats.total_occurrences,
        stats.inconsistency_rate,
        stats.average_confidence,
    )

    return stats