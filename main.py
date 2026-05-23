"""
main.py — Orquestrador principal do sistema de análise Regex.

Fluxo:
────────────────────────────────────────────────────────

1. Leitura e inspeção
2. Detecção de tipo de conteúdo
3. Extração via Regex
4. Validação estrutural + semântica
5. Estatísticas
6. Exportação
"""

from __future__ import annotations

import os
import sys
import time
import logging

from collections import Counter


# ──────────────────────────────────────────────
# PATH ROOT
# ──────────────────────────────────────────────

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.insert(0, BASE_DIR)


# ──────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────

from src.modules.reader import (
    read_file,
    FileInspection,
)

from src.modules.detector import (
    detect_content_type,
)

from src.modules.extractor import (
    extract_all,
)

from src.modules.validator import (
    validate_occurrences,
)

from src.modules.statistics import (
    compute_statistics,
)

from src.modules.exporter import (
    export_json,
    export_csv,
    export_report,
)


# ──────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s "
        "[%(levelname)s] "
        "%(name)s: %(message)s"
    ),

    handlers=[

        logging.StreamHandler(
            sys.stdout
        ),

        logging.FileHandler(
            os.path.join(
                LOG_DIR,
                "sistema.log"
            ),
            encoding="utf-8"
        ),
    ],
)

logger = logging.getLogger("main")


# ──────────────────────────────────────────────
# ENTRADA / SAÍDA
# ──────────────────────────────────────────────

INPUT_DIR = os.path.join(
    BASE_DIR,
    "dados"
)

INPUT_FILES = [

    "01_atendimentos_bagunçados.txt",
    "02_logs_mistos.log",
    "03_mensagens_chat.txt",
    "04_exportacao_suja.csv",
]

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ──────────────────────────────────────────────
# UTIL
# ──────────────────────────────────────────────

def banner(title: str) -> None:

    print(f"\n{'═' * 70}")
    print(f"  {title}")
    print(f"{'═' * 70}")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():

    start_time = time.time()

    banner(
        "SISTEMA DE ANÁLISE REGEX — INICIALIZANDO"
    )

    # ==================================================
    # ETAPA 1 — LEITURA
    # ==================================================

    banner(
        "1. LEITURA E INSPEÇÃO DOS ARQUIVOS"
    )

    inspections: list[FileInspection] = []

    files_lines: dict[str, list[str]] = {}

    for filename in INPUT_FILES:

        file_path = os.path.join(
            INPUT_DIR,
            filename
        )

        if not os.path.exists(file_path):

            logger.warning(
                "Arquivo não encontrado: %s",
                file_path
            )

            continue

        inspection = read_file(
            file_path
        )

        inspections.append(
            inspection
        )

        files_lines[
            inspection.filename
        ] = inspection.lines

        print(f"  ✔ {inspection.filename}")

        print(
            f"    Linhas: "
            f"{inspection.total_lines:,}"
        )

        print(
            f"    Encoding: "
            f"{inspection.encoding}"
        )

        if inspection.inconsistencies:

            for issue in (
                inspection.inconsistencies
            ):

                print(f"    ⚠ {issue}")

        if inspection.sample_lines:

            print(
                f"    Amostra: "
                f"{inspection.sample_lines[0][:80]}..."
            )

    if not files_lines:

        logger.error(
            "Nenhum arquivo carregado."
        )

        sys.exit(1)

    # ==================================================
    # ETAPA 2 — DETECÇÃO
    # ==================================================

    banner(
        "2. DETECÇÃO DE TIPO DE CONTEÚDO"
    )

    file_types: dict[str, str] = {}

    for inspection in inspections:

        detected_type = detect_content_type(

            filename=inspection.filename,

            lines=inspection.lines
        )

        file_types[
            inspection.filename
        ] = detected_type

        print(
            f"  {inspection.filename:<42} "
            f"→ {detected_type}"
        )

    # ==================================================
    # ETAPA 3 — EXTRAÇÃO REGEX
    # ==================================================

    banner(
        "3. EXTRAÇÃO VIA EXPRESSÕES REGULARES"
    )

    print(
        "  Executando padrões regex..."
    )

    occurrences = extract_all(
        files_lines
    )

    print(
        f"  → {len(occurrences):,} "
        f"ocorrências extraídas"
    )

    # ------------------------------------------
    # RESUMO POR TIPO
    # ------------------------------------------

    by_type = Counter(

        occurrence.pattern_name

        for occurrence in occurrences
    )

    print()

    for pattern_name, total in sorted(
        by_type.items()
    ):

        print(
            f"     "
            f"{pattern_name:<22}: "
            f"{total:>6}"
        )

    # ==================================================
    # ETAPA 4 — VALIDAÇÃO
    # ==================================================

    banner(
        "4. VALIDAÇÃO ESTRUTURAL + SEMÂNTICA"
    )

    occurrences = validate_occurrences(
        occurrences
    )

    # ------------------------------------------
    # ESTRUTURAL
    # ------------------------------------------

    structural_valid = sum(

        1

        for occurrence in occurrences

        if (
            occurrence.structural_status
            == "valido"
        )
    )

    structural_invalid = sum(

        1

        for occurrence in occurrences

        if (
            occurrence.structural_status
            == "invalido"
        )
    )

    # ------------------------------------------
    # SEMÂNTICA
    # ------------------------------------------

    semantic_invalid = sum(

        1

        for occurrence in occurrences

        if (
            occurrence.semantic_status
            == "invalido"
        )
    )

    # ------------------------------------------
    # STATUS FINAL
    # ------------------------------------------

    final_valid = sum(

        1

        for occurrence in occurrences

        if (
            occurrence.final_status
            == "valido"
        )
    )

    final_invalid = sum(

        1

        for occurrence in occurrences

        if (
            occurrence.final_status
            == "invalido"
        )
    )

    print()

    print(
        f"  Estruturalmente válidos : "
        f"{structural_valid:,}"
    )

    print(
        f"  Estruturalmente inválidos : "
        f"{structural_invalid:,}"
    )

    print(
        f"  Semanticamente inválidos : "
        f"{semantic_invalid:,}"
    )

    print()

    print(
        f"  Total válidos : "
        f"{final_valid:,}"
    )

    print(
        f"  Total inválidos : "
        f"{final_invalid:,}"
    )

    if occurrences:

        invalid_rate = (
            final_invalid
            / len(occurrences)
        ) * 100

        print(
            f"  Taxa de inconsistência : "
            f"{invalid_rate:.2f}%"
        )

    # ==================================================
    # ETAPA 5 — ESTATÍSTICAS
    # ==================================================

    banner(
        "5. CÁLCULO DE ESTATÍSTICAS"
    )

    stats = compute_statistics(

        occurrences=occurrences,

        files_lines=files_lines
    )

    print(
        f"  Total de ocorrências : "
        f"{stats.total_occurrences:,}"
    )

    print(
        f"  Taxa geral de inconsistência : "
        f"{stats.inconsistency_rate:.2f}%"
    )

    # ==================================================
    # ETAPA 6 — EXPORTAÇÃO
    # ==================================================

    banner(
        "6. EXPORTAÇÃO DE RESULTADOS"
    )

    json_path = export_json(
        occurrences,
        OUTPUT_DIR
    )

    csv_path = export_csv(
        occurrences,
        OUTPUT_DIR
    )

    report_path = export_report(

        stats=stats,

        file_inspections=inspections,

        file_types=file_types,

        output_dir=OUTPUT_DIR,
    )

    print(f"  JSON      : {json_path}")
    print(f"  CSV       : {csv_path}")
    print(f"  Relatório : {report_path}")

    # ==================================================
    # FINALIZAÇÃO
    # ==================================================

    elapsed = (
        time.time()
        - start_time
    )

    banner(
        f"CONCLUÍDO EM {elapsed:.1f}s"
    )

    print(
        f"  {len(occurrences):,} ocorrências "
        f"| {final_valid:,} válidas "
        f"| {final_invalid:,} inválidas"
    )

    print()

    return (

        occurrences,

        stats,

        file_types,

        inspections
    )


# ──────────────────────────────────────────────
# ENTRYPOINT
# ──────────────────────────────────────────────

if __name__ == "__main__":

    main()