"""
extractor.py — Motor inteligente de extração contextual.

Versão híbrida baseada nos pontos fortes dos Projetos A e B.

PRINCIPAIS MELHORIAS:
────────────────────────────────────────────────────────

✅ Context-aware extraction (Projeto B)
✅ Arquitetura modular e tipada (Projeto A)
✅ Dual regex:
    - extract_pattern
    - validation_pattern
✅ Normalização desacoplada
✅ Pós-processamento semântico
✅ Deduplicação
✅ Priorização contextual
✅ Fallback global
✅ Melhor performance
✅ Melhor qualidade de dados
✅ Melhor observabilidade

PIPELINE:
────────────────────────────────────────────────────────

detect_context
    → context prioritized patterns
        → fallback patterns
            → extraction
                → normalization
                    → structural validation
                        → semantic validation
                            → occurrence
"""

from __future__ import annotations

import re
import logging

from dataclasses import dataclass
from typing import Iterable

from src.config import (
    PATTERNS,
    PatternConfig,
    NOME_BLACKLIST,
)

logger = logging.getLogger("extractor")


# ──────────────────────────────────────────────
# MODELO DE OCORRÊNCIA
# ──────────────────────────────────────────────

@dataclass(slots=True)
class Occurrence:

    # Identificação
    pattern_name: str
    pattern_label: str

    # Dados
    raw_value: str
    normalized_value: str

    # Origem
    filename: str
    line_number: int

    # Contexto
    detected_context: str
    context_excerpt: str

    # Regex utilizadas
    extract_regex: str
    validation_regex: str | None

    # Resultado
    structural_status: str = "pendente"
    semantic_status: str = "pendente"

    # Metadata
    confidence: float = 0.0
    final_status: str = "pendente"


# ──────────────────────────────────────────────
# CACHE DE CONFIGURAÇÕES
# ──────────────────────────────────────────────

PATTERN_MAP = {
    p.name: p
    for p in PATTERNS
}


# ──────────────────────────────────────────────
# ROTEAMENTO CONTEXTUAL
# ──────────────────────────────────────────────

CONTEXT_PATTERNS = {

    # ==========================================
    # CONTATO
    # ==========================================

    "contato": [
        "email",
        "telefone",
        "nome_proprio",
    ],

    # ==========================================
    # CLIENTE
    # ==========================================

    "cliente": [
        "cpf",
        "nome_proprio",
        "telefone",
        "email",
    ],

    # ==========================================
    # LOG
    # ==========================================

    "log": [
        "ip",
        "session_id",
        "datetime",
        "url",
    ],

    # ==========================================
    # ACESSO
    # ==========================================

    "acesso": [
        "url",
        "ip",
        "datetime",
        "session_id",
    ],
}


# Regex fallback globais
GLOBAL_FALLBACK_PATTERNS = [
    "email",
    "telefone",
    "cpf",
    "url",
]


# ──────────────────────────────────────────────
# DETECÇÃO DE CONTEXTO
# ──────────────────────────────────────────────

def detect_context(line: str) -> str:
    """
    Detecta o contexto dominante da linha.

    Estratégia:
    - leve
    - rápida
    - baseada em sinais
    - sem regex pesada
    """

    lower = line.lower()

    # ==========================================
    # CONTATO
    # ==========================================

    contato_signals = (
        "email",
        "telefone",
        "celular",
        "fone",
        "contato",
    )

    if any(s in lower for s in contato_signals):
        return "contato"

    # ==========================================
    # CLIENTE
    # ==========================================

    cliente_signals = (
        "cpf",
        "cliente",
        "nome",
        "cadastro",
    )

    if any(s in lower for s in cliente_signals):
        return "cliente"

    # ==========================================
    # LOG
    # ==========================================

    log_signals = (
        "[error]",
        "[warn]",
        "[info]",
        "session=",
        "service=",
    )

    if any(s in lower for s in log_signals):
        return "log"

    # ==========================================
    # ACESSO
    # ==========================================

    acesso_signals = (
        "http://",
        "https://",
        "login",
        "acesso",
    )

    if any(s in lower for s in acesso_signals):
        return "acesso"

    return "texto_livre"


# ──────────────────────────────────────────────
# EXTRAÇÃO PRINCIPAL
# ──────────────────────────────────────────────

def extract_all(
    files_lines: dict[str, list[str]]
) -> list[Occurrence]:

    occurrences: list[Occurrence] = []

    # Deduplicação global
    seen: set[tuple] = set()

    for filename, lines in files_lines.items():

        logger.info(
            "Processando arquivo: %s",
            filename
        )

        for line_number, line in enumerate(lines, start=1):

            if not line.strip():
                continue

            # ======================================
            # CONTEXTO
            # ======================================

            detected_context = detect_context(line)

            # ======================================
            # PADRÕES PRIORITÁRIOS
            # ======================================

            prioritized_patterns = (
                CONTEXT_PATTERNS.get(
                    detected_context,
                    []
                )
            )

            # ======================================
            # FALLBACK GLOBAL
            # ======================================

            candidate_patterns = list(
                dict.fromkeys(
                    prioritized_patterns
                    + GLOBAL_FALLBACK_PATTERNS
                )
            )

            # ======================================
            # EXECUÇÃO DE REGEX
            # ======================================

            for pattern_name in candidate_patterns:

                pc = PATTERN_MAP.get(pattern_name)

                if not pc:
                    continue

                regex = pc.compiled_extract

                if not regex:
                    continue

                try:

                    for match in regex.finditer(line):

                        raw_value = match.group(0)

                        # ==========================
                        # PÓS-FILTRO
                        # ==========================

                        if pc.name == "nome_proprio":

                            raw_value = (
                                filter_nome(raw_value)
                            )

                            if not raw_value:
                                continue

                        # ==========================
                        # NORMALIZAÇÃO
                        # ==========================

                        normalized_value = normalize_value(
                            pc.name,
                            raw_value
                        )

                        # ==========================
                        # DEDUP
                        # ==========================

                        dedup_key = (
                            pc.name,
                            normalized_value.lower(),
                            filename,
                            line_number,
                        )

                        if dedup_key in seen:
                            continue

                        seen.add(dedup_key)

                        # ==========================
                        # CONTEXTO DA LINHA
                        # ==========================

                        excerpt = build_excerpt(
                            line,
                            match.start(),
                            match.end(),
                        )

                        # ==========================
                        # VALIDAÇÃO ESTRUTURAL
                        # ==========================

                        structural_status = (
                            validate_structurally(
                                pc,
                                normalized_value
                            )
                        )

                        # ==========================
                        # SCORE DE CONFIANÇA
                        # ==========================

                        confidence = calculate_confidence(
                            context=detected_context,
                            pattern_name=pc.name,
                            structural_status=structural_status,
                        )

                        # ==========================
                        # OCORRÊNCIA
                        # ==========================

                        occurrence = Occurrence(

                            pattern_name=pc.name,
                            pattern_label=pc.label,

                            raw_value=raw_value,
                            normalized_value=normalized_value,

                            filename=filename,
                            line_number=line_number,

                            detected_context=detected_context,
                            context_excerpt=excerpt,

                            extract_regex=truncate_regex(
                                pc.extract_pattern
                            ),

                            validation_regex=truncate_regex(
                                pc.validation_pattern
                            ),

                            structural_status=structural_status,

                            confidence=confidence,
                        )

                        occurrences.append(
                            occurrence
                        )

                except Exception as exc:

                    logger.exception(
                        "Erro no padrão '%s' "
                        "arquivo=%s linha=%d erro=%s",
                        pc.name,
                        filename,
                        line_number,
                        exc
                    )

    logger.info(
        "Extração finalizada: %d ocorrências",
        len(occurrences)
    )

    return occurrences


# ──────────────────────────────────────────────
# VALIDAÇÃO ESTRUTURAL
# ──────────────────────────────────────────────

def validate_structurally(
    pc: PatternConfig,
    value: str
) -> str:

    if not pc.compiled_validation:
        return "não_aplicável"

    if pc.compiled_validation.fullmatch(value):
        return "valido"

    return "invalido"


# ──────────────────────────────────────────────
# NORMALIZAÇÃO
# ──────────────────────────────────────────────

def normalize_value(
    pattern_name: str,
    value: str
) -> str:

    if pattern_name == "email":
        return value.strip().lower()

    if pattern_name == "telefone":
        return re.sub(r"\D", "", value)

    if pattern_name == "cpf":
        return re.sub(r"\D", "", value)

    if pattern_name == "nome_proprio":
        return " ".join(
            p.capitalize()
            for p in value.split()
        )

    return value.strip()


# ──────────────────────────────────────────────
# FILTRO DE NOMES
# ──────────────────────────────────────────────

def filter_nome(raw: str) -> str:

    tokens = raw.split()

    # Blacklist
    for token in tokens:

        if token in NOME_BLACKLIST:
            return ""

    # Siglas
    if any(
        t.isupper() and len(t) > 1
        for t in tokens
    ):
        return ""

    # Muito curto
    if len(raw.replace(" ", "")) < 6:
        return ""

    return raw


# ──────────────────────────────────────────────
# CONTEXTO VISUAL
# ──────────────────────────────────────────────

def build_excerpt(
    line: str,
    start: int,
    end: int,
    radius: int = 40
) -> str:

    left = max(0, start - radius)
    right = min(len(line), end + radius)

    excerpt = line[left:right].strip()

    if left > 0:
        excerpt = "…" + excerpt

    if right < len(line):
        excerpt += "…"

    return excerpt


# ──────────────────────────────────────────────
# SCORE DE CONFIANÇA
# ──────────────────────────────────────────────

def calculate_confidence(
    context: str,
    pattern_name: str,
    structural_status: str
) -> float:

    score = 0.5

    # Contexto coerente
    if pattern_name in CONTEXT_PATTERNS.get(context, []):
        score += 0.3

    # Estruturalmente válido
    if structural_status == "valido":
        score += 0.2

    return round(
        min(score, 1.0),
        2
    )


# ──────────────────────────────────────────────
# UTIL
# ──────────────────────────────────────────────

def truncate_regex(
    pattern: str | None,
    limit: int = 80
) -> str | None:

    if not pattern:
        return None

    cleaned = (
        pattern
        .replace("\n", " ")
        .strip()
    )

    if len(cleaned) <= limit:
        return cleaned

    return cleaned[:limit] + "..."