"""
exporter.py — Exportação e consolidação final do pipeline Regex.

Responsabilidades:
──────────────────────────────────────────────
- Exportação JSON
- Exportação CSV
- Relatório TXT consolidado
- Consolidação estatística
- Persistência dos resultados

Objetivo:
──────────────────────────────────────────────
Transformar os resultados do pipeline Regex
em artefatos finais de análise.
"""

from __future__ import annotations

import os
import csv
import json
import logging

from datetime import datetime

from src.modules.extractor import Occurrence
from src.modules.statistics import Statistics
from src.modules.reader import FileInspection

logger = logging.getLogger("exporter")


# ──────────────────────────────────────────────
# TIMESTAMP GLOBAL
# ──────────────────────────────────────────────

TIMESTAMP = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)


# ──────────────────────────────────────────────
# JSON
# ──────────────────────────────────────────────

def export_json(
    occurrences: list[Occurrence],
    output_dir: str,
) -> str:
    """
    Exporta ocorrências completas em JSON.
    """

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    path = os.path.join(output_dir, "resultados.json")

    data = []

    for occ in occurrences:

        data.append({

            # ==============================
            # IDENTIFICAÇÃO
            # ==============================

            "tipo": occ.pattern_name,
            "label": occ.pattern_label,

            # ==============================
            # VALORES
            # ==============================

            "valor_bruto": occ.raw_value,
            "valor_normalizado": (
                occ.normalized_value
            ),

            # ==============================
            # ORIGEM
            # ==============================

            "arquivo": occ.filename,
            "linha": occ.line_number,

            # ==============================
            # CONTEXTO
            # ==============================

            "contexto_detectado": (
                occ.detected_context
            ),

            "trecho_contexto": (
                occ.context_excerpt
            ),

            # ==============================
            # VALIDAÇÃO
            # ==============================

            "validacao_estrutural": (
                occ.structural_status
            ),

            "validacao_semantica": (
                occ.semantic_status
            ),

            "status_final": (
                "invalido"
                if (
                    occ.structural_status == "invalido"
                    or
                    occ.semantic_status == "invalido"
                )
                else "valido"
            ),

            # ==============================
            # REGEX
            # ==============================

            "regex_extracao": (
                occ.extract_regex
            ),

            "regex_validacao": (
                occ.validation_regex
            ),

            # ==============================
            # SCORE
            # ==============================

            "confianca": occ.confidence,
        })

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    logger.info(
        "JSON exportado: %s",
        path
    )

    return path


# ──────────────────────────────────────────────
# CSV
# ──────────────────────────────────────────────

def export_csv(
    occurrences: list[Occurrence],
    output_dir: str,
) -> str:
    """
    Exporta ocorrências em CSV.
    """

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    path = os.path.join(
        output_dir,
        f"resultados_{TIMESTAMP}.csv"
    )

    fields = [

        "tipo",
        "label",

        "valor_bruto",
        "valor_normalizado",

        "arquivo",
        "linha",

        "contexto_detectado",

        "validacao_estrutural",
        "validacao_semantica",

        "confianca",
    ]

    with open(
        path,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
            delimiter=";"
        )

        writer.writeheader()

        for occ in occurrences:

            writer.writerow({

                "tipo": occ.pattern_name,
                "label": occ.pattern_label,

                "valor_bruto": occ.raw_value,

                "valor_normalizado": (
                    occ.normalized_value
                ),

                "arquivo": occ.filename,
                "linha": occ.line_number,

                "contexto_detectado": (
                    occ.detected_context
                ),

                "validacao_estrutural": (
                    occ.structural_status
                ),

                "validacao_semantica": (
                    occ.semantic_status
                ),

                "confianca": occ.confidence,
            })

    logger.info(
        "CSV exportado: %s",
        path
    )

    return path


# ──────────────────────────────────────────────
# RELATÓRIO TXT
# ──────────────────────────────────────────────

def export_report(
    stats: Statistics,
    file_inspections: list[FileInspection],
    file_types: dict[str, str],
    output_dir: str,
) -> str:
    """
    Gera relatório consolidado TXT.
    """

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    path = os.path.join(
        output_dir,
        f"relatorio_{TIMESTAMP}.txt"
    )

    separator = "─" * 70

    lines = [

        "╔════════════════════════════════════════════════════════════╗",
        "║          SISTEMA DE ANÁLISE REGEX — RELATÓRIO            ║",
        "╚════════════════════════════════════════════════════════════╝",

        "",

        f"Gerado em: "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",

        "",

        separator,
        "1. ARQUIVOS PROCESSADOS",
        separator,
    ]

    # ======================================================
    # ARQUIVOS
    # ======================================================

    for inspection in file_inspections:

        lines.extend([

            f"Arquivo: {inspection.filename}",
            f"Tipo detectado: "
            f"{file_types.get(inspection.filename, '?')}",

            f"Encoding: {inspection.encoding}",

            f"Linhas: {inspection.total_lines}",
            f"Linhas vazias: {inspection.blank_lines}",

            f"Caracteres: {inspection.total_chars}",

        ])

        if inspection.inconsistencies:

            lines.append(
                "Inconsistências:"
            )

            for issue in inspection.inconsistencies:

                lines.append(
                    f"  - {issue}"
                )

        lines.append("")

    # ======================================================
    # ESTATÍSTICAS
    # ======================================================

    lines.extend([

        separator,
        "2. ESTATÍSTICAS GERAIS",
        separator,

        f"Total de ocorrências: "
        f"{stats.total_occurrences}",

        f"Linhas processadas: "
        f"{stats.total_lines_processed}",

        f"Taxa de inconsistência: "
        f"{stats.inconsistency_rate:.2f}%",

        f"Taxa estrutural válida: "
        f"{stats.structural_valid_rate:.2f}%",

        f"Taxa semântica válida: "
        f"{stats.semantic_valid_rate:.2f}%",

        f"Confiança média: "
        f"{stats.average_confidence:.2f}",

        "",
    ])

    # ======================================================
    # POR TIPO
    # ======================================================

    lines.extend([

        separator,
        "3. OCORRÊNCIAS POR TIPO",
        separator,
    ])

    for pattern_name, total in sorted(
        stats.by_type.items()
    ):

        valid = stats.valid_by_type.get(
            pattern_name,
            0
        )

        invalid = stats.invalid_by_type.get(
            pattern_name,
            0
        )

        semantic_invalid = (
            stats.semantic_invalid_by_type.get(
                pattern_name,
                0
            )
        )

        lines.extend([

            f"{pattern_name}",

            f"  Total: {total}",
            f"  Estruturalmente válidos: {valid}",
            f"  Estruturalmente inválidos: {invalid}",
            f"  Semânticamente inválidos: "
            f"{semantic_invalid}",

            "",
        ])

    # ======================================================
    # CONTEXTO
    # ======================================================

    lines.extend([

        separator,
        "4. DISTRIBUIÇÃO CONTEXTUAL",
        separator,
    ])

    for context, total in sorted(
        stats.by_context.items(),
        key=lambda item: item[1],
        reverse=True
    ):

        lines.append(
            f"{context}: {total}"
        )

    lines.append("")

    # ======================================================
    # DISTRIBUIÇÃO POR ARQUIVO
    # ======================================================

    lines.extend([

        separator,
        "5. DISTRIBUIÇÃO POR ARQUIVO",
        separator,
    ])

    for filename, values in (
        stats.by_file.items()
    ):

        lines.append(f"{filename}")

        for pattern_name, total in (
            sorted(values.items())
        ):

            lines.append(
                f"  {pattern_name}: {total}"
            )

        lines.append("")

    # ======================================================
    # TOP VALORES
    # ======================================================

    lines.extend([

        separator,
        "6. TOP VALORES",
        separator,
    ])

    for pattern_name, values in (
        stats.top_values.items()
    ):

        lines.append(f"{pattern_name}")

        for value, total in values:

            lines.append(
                f"  {total}x -> {value[:60]}"
            )

        lines.append("")

    # ======================================================
    # LINHAS
    # ======================================================

    lines.extend([

        separator,
        "7. DISTRIBUIÇÃO DE LINHAS",
        separator,
    ])

    for line_type, total in sorted(
        stats.line_type_distribution.items(),
        key=lambda item: item[1],
        reverse=True
    ):

        lines.append(
            f"{line_type}: {total}"
        )

    lines.extend([

        "",
        separator,
        "PROCESSAMENTO FINALIZADO COM SUCESSO",
        separator,
    ])

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(lines)
        )

    logger.info(
        "Relatório exportado: %s",
        path
    )

    return path