"""
detector.py — Detecção estrutural inteligente de conteúdo.

Baseado em:
- heurísticas regex
- score percentual
- sinais estruturais
- tolerância a arquivos bagunçados

Tipos suportados:
- log
- chat
- csv
- texto_livre
"""

from __future__ import annotations

import os
import logging

from src.config import FILE_TYPE_SIGNALS

logger = logging.getLogger("detector")


# ──────────────────────────────────────────────
# CONFIGURAÇÕES
# ──────────────────────────────────────────────

MIN_LINES_ANALYZED = 50

THRESHOLDS = {
    "csv": 0.40,
    "chat": 0.25,
    "log": 0.20,
}


# ──────────────────────────────────────────────
# FUNÇÃO AUXILIAR
# ──────────────────────────────────────────────

def calculate_signal_score(
    lines: list[str],
    patterns: list
) -> int:
    """
    Conta quantas linhas possuem
    pelo menos um sinal compatível.
    """

    score = 0

    for line in lines:

        for pattern in patterns:

            if pattern.search(line):
                score += 1
                break

    return score


# ──────────────────────────────────────────────
# DETECÇÃO PRINCIPAL
# ──────────────────────────────────────────────

def detect_content_type(
    filename: str,
    lines: list[str]
) -> str:
    """
    Detecta o tipo estrutural predominante
    do arquivo usando heurísticas regex.

    Estratégia:
    1. Analisa conteúdo
    2. Calcula score por tipo
    3. Usa percentuais mínimos
    4. Extensão apenas influencia
    """

    if not lines:
        return "texto_livre"

    ext = os.path.splitext(filename)[1].lower()

    # ==========================================
    # AMOSTRA
    # ==========================================

    sample = [
        line
        for line in lines[:MIN_LINES_ANALYZED]
        if line.strip()
    ]

    if not sample:
        return "texto_livre"

    total = len(sample)

    # ==========================================
    # SCORE POR TIPO
    # ==========================================

    scores: dict[str, int] = {}

    for content_type, patterns in FILE_TYPE_SIGNALS.items():

        if content_type == "texto_livre":
            continue

        scores[content_type] = (
            calculate_signal_score(
                sample,
                patterns
            )
        )

    # ==========================================
    # AJUSTE POR EXTENSÃO
    # ==========================================

    # Extensão ajuda mas não decide sozinha

    if ext == ".csv":
        scores["csv"] += 3

    elif ext == ".log":
        scores["log"] += 2

    # ==========================================
    # PERCENTUAIS
    # ==========================================

    percentages = {
        k: v / total
        for k, v in scores.items()
    }

    logger.debug(
        "Detecção %s | scores=%s | percentuais=%s",
        filename,
        scores,
        percentages
    )

    # ==========================================
    # CSV
    # ==========================================

    if percentages.get("csv", 0) >= THRESHOLDS["csv"]:
        detected = "csv"

    # ==========================================
    # CHAT
    # ==========================================

    elif percentages.get("chat", 0) >= THRESHOLDS["chat"]:
        detected = "chat"

    # ==========================================
    # LOG
    # ==========================================

    elif percentages.get("log", 0) >= THRESHOLDS["log"]:
        detected = "log"

    # ==========================================
    # FALLBACK
    # ==========================================

    else:
        detected = "texto_livre"

    logger.info(
        "Tipo detectado para %s: %s",
        filename,
        detected
    )

    return detected