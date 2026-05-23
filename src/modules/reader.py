"""
reader.py — Leitura e inspeção inteligente de arquivos.

OBJETIVOS:
────────────────────────────────────────────────────────

✅ Detectar encoding automaticamente
✅ Ler arquivos com fallback seguro
✅ Detectar inconsistências estruturais
✅ Melhorar robustez de CSV
✅ NÃO tirar o foco do Regex
✅ Preparar corretamente os dados
✅ Melhor observabilidade
✅ Arquitetura desacoplada

IMPORTANTE:
────────────────────────────────────────────────────────

Este módulo NÃO faz parsing complexo.

O foco do projeto continua sendo:
    EXTRAÇÃO E VALIDAÇÃO VIA REGEX

O reader apenas:
- prepara os dados;
- evita corrupção;
- melhora confiabilidade.
"""

from __future__ import annotations

import os
import re
import csv
import logging

from dataclasses import dataclass, field

logger = logging.getLogger("reader")


# ──────────────────────────────────────────────
# MODELO DE INSPEÇÃO
# ──────────────────────────────────────────────

@dataclass(slots=True)
class FileInspection:
    """
    Resultado da inspeção de um arquivo.
    """

    # Arquivo
    path: str
    filename: str

    # Leitura
    encoding: str

    # Estatísticas
    total_lines: int
    total_chars: int
    blank_lines: int

    # Amostragem
    sample_lines: list[str]

    # Diagnóstico
    inconsistencies: list[str]

    # Conteúdo
    lines: list[str] = field(
        default_factory=list,
        repr=False
    )


# ──────────────────────────────────────────────
# DETECÇÃO DE ENCODING
# ──────────────────────────────────────────────

def detect_encoding(path: str) -> str:
    """
    Detecta encoding automaticamente.

    Estratégia:
    - chardet
    - fallback utf-8
    """

    try:

        import chardet

        with open(path, "rb") as f:
            raw = f.read(
                min(
                    32768,
                    os.path.getsize(path)
                )
            )

        result = chardet.detect(raw)

        encoding = (
            result.get("encoding")
            or "utf-8"
        )

        confidence = (
            result.get("confidence", 0)
        )

        logger.debug(
            "Encoding detectado: %s (conf=%.2f)",
            encoding,
            confidence
        )

        return encoding

    except ImportError:

        logger.warning(
            "chardet não instalado. "
            "Usando utf-8."
        )

        return "utf-8"

    except Exception as exc:

        logger.exception(
            "Erro detectando encoding: %s",
            exc
        )

        return "utf-8"


# ──────────────────────────────────────────────
# LEITURA PRINCIPAL
# ──────────────────────────────────────────────

def read_file(
    path: str,
    sample_size: int = 10
) -> FileInspection:
    """
    Lê e inspeciona um arquivo.
    """

    encoding = detect_encoding(path)

    lines: list[str] = []

    # ==========================================
    # FALLBACKS DE ENCODING
    # ==========================================

    candidate_encodings = [
        encoding,
        "utf-8",
        "latin-1",
    ]

    for enc in candidate_encodings:

        try:

            with open(
                path,
                "r",
                encoding=enc,
                errors="replace"
            ) as file:

                lines = file.readlines()

            encoding = enc

            break

        except Exception as exc:

            logger.warning(
                "Falha ao ler %s com %s: %s",
                path,
                enc,
                exc
            )

    # ==========================================
    # NORMALIZAÇÃO LEVE
    # ==========================================

    normalized_lines = [
        line.rstrip("\n")
        for line in lines
    ]

    blank_lines = sum(
        1
        for line in normalized_lines
        if not line.strip()
    )

    sample_lines = [
        line
        for line in normalized_lines
        if line.strip()
    ][:sample_size]

    # ==========================================
    # INSPEÇÃO ESTRUTURAL
    # ==========================================

    inconsistencies = detect_inconsistencies(
        normalized_lines,
        path
    )

    total_chars = sum(
        len(line)
        for line in normalized_lines
    )

    logger.info(
        "Arquivo lido: %s | linhas=%d | encoding=%s",
        os.path.basename(path),
        len(normalized_lines),
        encoding
    )

    return FileInspection(

        path=path,
        filename=os.path.basename(path),

        encoding=encoding,

        total_lines=len(normalized_lines),
        total_chars=total_chars,
        blank_lines=blank_lines,

        sample_lines=sample_lines,

        inconsistencies=inconsistencies,

        lines=normalized_lines,
    )


# ──────────────────────────────────────────────
# DETECÇÃO DE INCONSISTÊNCIAS
# ──────────────────────────────────────────────

def detect_inconsistencies(
    lines: list[str],
    path: str
) -> list[str]:
    """
    Detecta inconsistências estruturais leves.

    NÃO substitui parser.
    Apenas auxilia diagnóstico.
    """

    issues: list[str] = []

    extension = os.path.splitext(path)[1].lower()

    # ==========================================
    # CSV
    # ==========================================

    if extension == ".csv":

        csv_issues = inspect_csv_structure(
            lines
        )

        issues.extend(csv_issues)

    # ==========================================
    # LINHAS MUITO LONGAS
    # ==========================================

    long_lines = [
        index + 1
        for index, line in enumerate(lines)
        if len(line) > 2000
    ]

    if long_lines:

        issues.append(
            f"Linhas muito longas (>2000 chars): "
            f"{long_lines[:5]}"
        )

    # ==========================================
    # CARACTERES DE CONTROLE
    # ==========================================

    control_regex = re.compile(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f]"
    )

    control_lines = [
        index + 1
        for index, line in enumerate(lines)
        if control_regex.search(line)
    ]

    if control_lines:

        issues.append(
            f"Caracteres de controle "
            f"em linhas: {control_lines[:5]}"
        )

    # ==========================================
    # MUITAS LINHAS EM BRANCO
    # ==========================================

    consecutive_blank = 0
    max_blank = 0

    for line in lines:

        if not line.strip():

            consecutive_blank += 1

            max_blank = max(
                max_blank,
                consecutive_blank
            )

        else:

            consecutive_blank = 0

    if max_blank >= 3:

        issues.append(
            f"Até {max_blank} linhas "
            f"em branco consecutivas"
        )

    return issues


# ──────────────────────────────────────────────
# INSPEÇÃO LEVE DE CSV
# ──────────────────────────────────────────────

def inspect_csv_structure(
    lines: list[str]
) -> list[str]:
    """
    Inspeção leve de CSV.

    IMPORTANTE:
    Não substitui parser completo.
    Apenas reduz falsos diagnósticos.

    Melhor que split().
    Mantém foco do projeto em regex.
    """

    issues: list[str] = []

    if not lines:
        return issues

    try:

        sample = "\n".join(lines[:10])

        dialect = csv.Sniffer().sniff(
            sample,
            delimiters=";,"
        )

        delimiter = dialect.delimiter

    except Exception:

        delimiter = ";"

    column_counts: set[int] = set()

    for index, line in enumerate(lines[:50], start=1):

        if not line.strip():
            continue

        try:

            reader = csv.reader(
                [line],
                delimiter=delimiter
            )

            columns = next(reader)

            column_counts.add(
                len(columns)
            )

        except Exception:

            issues.append(
                f"Linha CSV inválida: {index}"
            )

    if len(column_counts) > 1:

        issues.append(
            "CSV com número variável "
            f"de colunas: {sorted(column_counts)}"
        )

    return issues
