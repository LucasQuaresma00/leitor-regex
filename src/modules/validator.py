"""
validator.py — Validação estrutural orientada a Regex.

ARQUITETURA:
────────────────────────────────────────────────────────

Este módulo NÃO substitui Regex por lógica procedural.

O objetivo dele é:

1. Aplicar a validation_pattern do config.py
2. Centralizar classificação
3. Executar validações semânticas SOMENTE quando
   Regex não é suficiente formalmente
   (ex.: CPF com dígito verificador)

FOCO DO TRABALHO:
────────────────────────────────────────────────────────

✅ Regex continua sendo o núcleo
✅ validation_pattern é a principal validação
✅ Validator apenas orquestra
✅ Sem fuga de escopo acadêmico
✅ Mantém arquitetura profissional

PIPELINE:
────────────────────────────────────────────────────────

Occurrence
    → validation_pattern
        → semantic validation opcional
            → classificação final
"""

from __future__ import annotations

import re
import logging

from dataclasses import dataclass, field

from src.modules.extractor import (
    Occurrence,
    PATTERN_MAP,
)

logger = logging.getLogger("validator")


# ──────────────────────────────────────────────
# RESULTADO DE VALIDAÇÃO
# ──────────────────────────────────────────────

@dataclass(slots=True)
class ValidationResult:

    pattern_name: str

    structural_status: str
    semantic_status: str

    final_status: str

    confidence: float

    reasons: list[str] = field(default_factory=list)


# ──────────────────────────────────────────────
# VALIDAÇÃO SEMÂNTICA — CPF
# ──────────────────────────────────────────────
#
# Regex NÃO consegue validar:
# - dígitos verificadores
# - CPFs inválidos matematicamente
#
# Portanto:
# esta validação continua válida no escopo.
# ──────────────────────────────────────────────

def _cpf_digit(
    digits: str,
    length: int
) -> int:

    total = sum(
        int(d) * (length + 1 - i)
        for i, d in enumerate(digits[:length])
    )

    remainder = (total * 10) % 11

    return (
        0
        if remainder >= 10
        else remainder
    )


def validate_cpf_semantics(
    cpf: str
) -> tuple[bool, list[str]]:

    reasons = []

    digits = re.sub(
        r"\D",
        "",
        cpf
    )

    # Quantidade incorreta
    if len(digits) != 11:

        reasons.append(
            "CPF deve conter 11 dígitos"
        )

        return False, reasons

    # Todos iguais
    if len(set(digits)) == 1:

        reasons.append(
            "CPF possui todos os dígitos iguais"
        )

        return False, reasons

    d1 = _cpf_digit(digits, 9)
    d2 = _cpf_digit(digits, 10)

    if digits[9] != str(d1):

        reasons.append(
            "Primeiro dígito verificador inválido"
        )

    if digits[10] != str(d2):

        reasons.append(
            "Segundo dígito verificador inválido"
        )

    return (
        len(reasons) == 0,
        reasons
    )


# ──────────────────────────────────────────────
# REGISTRY DE VALIDAÇÕES SEMÂNTICAS
# ──────────────────────────────────────────────
#
# SOMENTE validações impossíveis via regex.
# ──────────────────────────────────────────────

SEMANTIC_VALIDATORS = {

    "cpf": validate_cpf_semantics,
}


# ──────────────────────────────────────────────
# PIPELINE PRINCIPAL
# ──────────────────────────────────────────────

def validate_occurrences(
    occurrences: list[Occurrence]
) -> list[Occurrence]:

    logger.info(
        "Validando %d ocorrências",
        len(occurrences)
    )

    for occ in occurrences:

        result = validate_occurrence(
            occ
        )

        occ.structural_status = (
            result.structural_status
        )

        occ.semantic_status = (
            result.semantic_status
        )

        occ.final_status = (
            result.final_status
        ) 

        occ.confidence = (
            result.confidence
        )

    summarize_validation(
        occurrences
    )

    return occurrences


# ──────────────────────────────────────────────
# VALIDAÇÃO UNITÁRIA
# ──────────────────────────────────────────────

def validate_occurrence(
    occ: Occurrence
) -> ValidationResult:

    reasons: list[str] = []

    pc = PATTERN_MAP.get(
        occ.pattern_name
    )

    # ==========================================
    # CONFIG NÃO ENCONTRADA
    # ==========================================

    if not pc:

        return ValidationResult(

            pattern_name=occ.pattern_name,

            structural_status="erro",
            semantic_status="erro",

            final_status="erro",

            confidence=0.0,

            reasons=[
                "PatternConfig não encontrado"
            ]
        )

    # ==========================================
    # VALIDAÇÃO ESTRUTURAL
    # ==========================================

    structural_status = validate_structurally(
        pc,
        occ.normalized_value
    )

    # ==========================================
    # VALIDAÇÃO SEMÂNTICA
    # ==========================================

    semantic_status = "não_aplicável"

    # Só executa semântica
    # se estrutural passou
    if structural_status == "valido":

        semantic_validator = (
            SEMANTIC_VALIDATORS.get(
                occ.pattern_name
            )
        )

        if semantic_validator:

            semantic_ok, semantic_reasons = (
                semantic_validator(
                    occ.normalized_value
                )
            )

            reasons.extend(
                semantic_reasons
            )

            semantic_status = (
                "valido"
                if semantic_ok
                else "invalido"
            )

    # ==========================================
    # STATUS FINAL
    # ==========================================

    final_status = determine_final_status(
        structural_status,
        semantic_status
    )

    # ==========================================
    # SCORE FINAL
    # ==========================================

    confidence = calculate_confidence(
        occ,
        structural_status,
        semantic_status
    )

    return ValidationResult(

        pattern_name=occ.pattern_name,

        structural_status=structural_status,

        semantic_status=semantic_status,

        final_status=final_status,

        confidence=confidence,

        reasons=reasons,
    )


# ──────────────────────────────────────────────
# VALIDAÇÃO ESTRUTURAL
# ──────────────────────────────────────────────
#
# O verdadeiro núcleo do trabalho.
#
# validation_pattern é a fonte oficial
# de validação.
# ──────────────────────────────────────────────

def validate_structurally(
    pc,
    value: str
) -> str:

    if not pc.compiled_validation:
        return "não_aplicável"

    try:

        if pc.compiled_validation.fullmatch(value):
            return "valido"

        return "invalido"

    except Exception as exc:

        logger.exception(
            "Erro validando '%s': %s",
            pc.name,
            exc
        )

        return "erro"


# ──────────────────────────────────────────────
# STATUS FINAL
# ──────────────────────────────────────────────

def determine_final_status(
    structural_status: str,
    semantic_status: str
) -> str:

    if structural_status == "erro":
        return "erro"

    if structural_status == "invalido":
        return "invalido"

    if semantic_status == "invalido":
        return "invalido"

    return "valido"


# ──────────────────────────────────────────────
# SCORE DE CONFIANÇA
# ──────────────────────────────────────────────

def calculate_confidence(
    occ: Occurrence,
    structural_status: str,
    semantic_status: str
) -> float:

    confidence = occ.confidence

    # Regex rigorosa passou
    if structural_status == "valido":
        confidence += 0.2

    # Semântica passou
    if semantic_status == "valido":
        confidence += 0.1

    # Regex rigorosa falhou
    if structural_status == "invalido":
        confidence -= 0.4

    # Semântica falhou
    if semantic_status == "invalido":
        confidence -= 0.2

    return round(
        max(0.0, min(confidence, 1.0)),
        2
    )


# ──────────────────────────────────────────────
# ESTATÍSTICAS
# ──────────────────────────────────────────────

def summarize_validation(
    occurrences: list[Occurrence]
) -> None:

    structural_valid = sum(
        1
        for o in occurrences
        if o.structural_status == "valido"
    )

    structural_invalid = sum(
        1
        for o in occurrences
        if o.structural_status == "invalido"
    )

    semantic_invalid = sum(
        1
        for o in occurrences
        if o.semantic_status == "invalido"
    )

    logger.info(
        (
            "Resumo validação | "
            "estrutural válido=%d | "
            "estrutural inválido=%d | "
            "semântico inválido=%d"
        ),
        structural_valid,
        structural_invalid,
        semantic_invalid
    )