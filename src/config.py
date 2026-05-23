"""
config.py — Configuração centralizada e extensível de padrões Regex.

Arquitetura híbrida inspirada nos pontos fortes dos Projetos A e B:

- Regex ampla (extract_pattern) → maximiza captura
- Regex estrutural (validation_pattern) → reduz falsos positivos
- Validação semântica opcional → regras de negócio reais
- Metadata rica → observabilidade e manutenção
- Preparado para pipeline moderno:
    extract → normalize → validate → analyze → export

Objetivos:
- Alta qualidade de dados
- Facilidade de expansão
- Melhor debug
- Melhor estatística
- Maior resiliência
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional, Pattern


# ──────────────────────────────────────────────
# CONFIGURAÇÃO DE PADRÕES
# ──────────────────────────────────────────────

@dataclass(slots=True)
class PatternConfig:
    """
    Configuração completa de um padrão detectável.
    """

    # Identificação
    name: str
    label: str

    # Regex principal de captura ampla
    extract_pattern: str

    # Regex estrutural rigorosa
    validation_pattern: Optional[str] = None

    # Flags
    extract_flags: int = re.IGNORECASE | re.VERBOSE
    validation_flags: int = re.VERBOSE

    # Documentação
    description: str = ""

    # Nome da função de validação semântica
    semantic_validator: Optional[str] = None

    # Normalizador opcional
    normalizer: Optional[str] = None

    # Prioridade do parser
    priority: int = 0

    # Permite múltiplas ocorrências sobrepostas
    allow_overlap: bool = False

    # Regex compiladas automaticamente
    compiled_extract: Pattern | None = field(init=False, default=None)
    compiled_validation: Pattern | None = field(init=False, default=None)

    def __post_init__(self):
        self.compiled_extract = re.compile(
            self.extract_pattern,
            self.extract_flags
        )

        if self.validation_pattern:
            self.compiled_validation = re.compile(
                self.validation_pattern,
                self.validation_flags
            )


# ──────────────────────────────────────────────
# PADRÕES PRINCIPAIS
# ──────────────────────────────────────────────

PATTERNS: list[PatternConfig] = [

    # ==========================================================
    # EMAIL
    # ==========================================================

    PatternConfig(
        name="email",
        label="E-mail",

        # Regex ampla para maximizar captura
        extract_pattern=r"""[a-zA-Z0-9._%+\-]+@[^\s<>"';]+""",

        # Regex rigorosa para validar estrutura
        validation_pattern=r"""^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$""",

        description=(
            "Captura ampla + validação estrutural rigorosa "
            "para reduzir falsos positivos."
        ),

        semantic_validator="validate_email",
        normalizer="normalize_email",
        priority=10,
    ),

    # ==========================================================
    # TELEFONE
    # ==========================================================

    PatternConfig(
        name="telefone",
        label="Telefone BR",

        extract_pattern=r"""
            (?:
                \(\d{2}\)
                |
                \b\d{2}
            )
            [\s\-]?
            (?:9?\d{4})
            [\s\-]?
            \d{4}
        """,

        validation_pattern=r"""
            ^
            (?:\(\d{2}\)|\d{2})
            [\s\-]?
            (?:9\d{4}|\d{4})
            [\s\-]?
            \d{4}
            $
        """,

        description=(
            "Telefone brasileiro com DDD obrigatório."
        ),

        semantic_validator="validate_telefone",
        normalizer="normalize_telefone",
        priority=9,
    ),

    # ==========================================================
    # CPF
    # ==========================================================

    PatternConfig(
        name="cpf",
        label="CPF",

        extract_pattern=r"""
            (?<!\d)
            \d{3}[\s.\-]?\d{3}[\s.\-]?\d{3}[\s.\-]?\d{2}
            (?!\d)
        """,

        validation_pattern=r"""
            ^
            (?:
                \d{3}\.\d{3}\.\d{3}-\d{2}
                |
                \d{11}
            )
            $
        """,

        description=(
            "CPF formatado ou não formatado."
        ),

        semantic_validator="validate_cpf",
        normalizer="normalize_cpf",
        priority=10,
    ),

    # ==========================================================
    # URL
    # ==========================================================

    PatternConfig(
        name="url",
        label="URL",

        extract_pattern=r"""
            (?:
                https?://
                |
                ftp://
                |
                www\.
            )
            [^\s<>"]+
        """,

        validation_pattern=r"""
            ^
            (?:
                https?|ftp
            )://
            (?:
                [a-zA-Z0-9\-]{1,63}\.
            )+
            [a-zA-Z]{2,6}
            (?::\d{2,5})?
            (?:[/?#][^\s]*)?
            $
        """,

        description=(
            "URL com captura ampla e validação rigorosa."
        ),

        semantic_validator="validate_url",
        normalizer="normalize_url",
        priority=8,
    ),

    # ==========================================================
    # DATA
    # ==========================================================

    PatternConfig(
        name="data",
        label="Data",

        extract_pattern=r"""
            \b
            \d{1,2}
            [/.-]
            \d{1,2}
            [/.-]
            \d{4}
            \b
        """,

        validation_pattern=r"""
            ^
            (0?[1-9]|[12]\d|3[01])
            /
            (0?[1-9]|1[0-2])
            /
            (\d{4})
            $
        """,

        extract_flags=re.VERBOSE,
        validation_flags=re.VERBOSE,

        description="Data DD/MM/YYYY.",

        semantic_validator="validate_data",
        normalizer="normalize_data",
    ),

    # ==========================================================
    # HORÁRIO
    # ==========================================================

    PatternConfig(
        name="horario",
        label="Horário",

        extract_pattern=r"""
            \b
            \d{1,2}:\d{2}(?::\d{2})?
            \b
        """,

        validation_pattern=r"""
            ^
            ([01]\d|2[0-3])
            :
            ([0-5]\d)
            (?:
                :
                ([0-5]\d)
            )?
            $
        """,

        extract_flags=re.VERBOSE,
        validation_flags=re.VERBOSE,

        description="Horário HH:MM[:SS].",
    ),

    # ==========================================================
    # DATA + HORA
    # ==========================================================

    PatternConfig(
        name="datetime",
        label="Data e Hora",

        extract_pattern=r"""
            \b
            \d{1,2}/\d{1,2}/\d{4}
            \s+
            \d{1,2}:\d{2}(?::\d{2})?
            \b
        """,

        validation_pattern=r"""
            ^
            (0?[1-9]|[12]\d|3[01])
            /
            (0?[1-9]|1[0-2])
            /
            (\d{4})
            \s+
            ([01]\d|2[0-3])
            :
            ([0-5]\d)
            (?:
                :
                ([0-5]\d)
            )?
            $
        """,

        extract_flags=re.VERBOSE,
        validation_flags=re.VERBOSE,

        description="Data + hora combinadas.",
    ),

    # ==========================================================
    # VALOR MONETÁRIO
    # ==========================================================

    PatternConfig(
        name="valor_monetario",
        label="Valor Monetário",

        extract_pattern=r"""
            R\$
            \s?
            \d[\d\.,]*
        """,

        validation_pattern=r"""
            ^
            R\$
            \s*
            \d{1,3}
            (?:\.\d{3})*
            (?:,\d{2})?
            $
        """,

        extract_flags=re.VERBOSE,
        validation_flags=re.VERBOSE,

        description="Valor monetário brasileiro.",

        normalizer="normalize_currency",
    ),

    # ==========================================================
    # NOME PRÓPRIO
    # ==========================================================

    PatternConfig(
        name="nome_proprio",
        label="Nome Próprio",

        extract_pattern=r"""
            \b
            [A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]
            [a-záàâãéêíóôõúç]{1,20}
            (?:
                \s
                [A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]
                [a-záàâãéêíóôõúç]{1,20}
            ){1,4}
            \b
        """,

        validation_pattern=r"""
            ^
            [A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]
            [a-záàâãéêíóôõúç]{1,20}
            (?:
                \s
                [A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]
                [a-záàâãéêíóôõúç]{1,20}
            ){1,4}
            $
        """,

        extract_flags=re.VERBOSE,
        validation_flags=re.VERBOSE,

        description=(
            "Nome próprio com 2-5 tokens."
        ),

        semantic_validator="validate_nome",
    ),

    # ==========================================================
    # IPv4
    # ==========================================================

    PatternConfig(
        name="ip",
        label="IPv4",

        extract_pattern=r"""
            \b
            (?:
                \d{1,3}\.
            ){3}
            \d{1,3}
            \b
        """,

        validation_pattern=r"""
            ^
            (?:
                (?:25[0-5]|2[0-4]\d|[01]?\d\d?)
                \.
            ){3}
            (?:25[0-5]|2[0-4]\d|[01]?\d\d?)
            $
        """,

        extract_flags=re.VERBOSE,
        validation_flags=re.VERBOSE,

        description="Endereço IPv4 válido.",
    ),

    # ==========================================================
    # SESSION ID
    # ==========================================================

    PatternConfig(
        name="session_id",
        label="Session ID",

        extract_pattern=r"""
            session=
            [A-Za-z0-9]{6,32}
        """,

        validation_pattern=r"""
            ^
            session=
            [A-Za-z0-9]{8,16}
            $
        """,

        extract_flags=re.VERBOSE,
        validation_flags=re.VERBOSE,

        description="Session IDs encontrados em logs.",
    ),
]


# ──────────────────────────────────────────────
# DETECÇÃO DE TIPO DE ARQUIVO
# ──────────────────────────────────────────────

FILE_TYPE_SIGNALS = {
    "log": [
        re.compile(r"\[(INFO|WARN|ERROR|DEBUG)\]"),
        re.compile(r"service=\w+\s+seq=\d+"),
        re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"),
    ],

    "chat": [
        re.compile(
            r"^\[\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\]\s+\S+.*:"
        ),
        re.compile(r"@\w+"),
    ],

    "csv": [
        re.compile(r"^[^;,\n]+[;,][^;,\n]+[;,]"),
        re.compile(r"^id[;,]nome[;,]"),
    ],

    "texto_livre": [],
}


# ──────────────────────────────────────────────
# BLACKLIST PARA NOMES
# ──────────────────────────────────────────────

NOME_BLACKLIST = {
    "Urgente",
    "Limpar",
    "Error",
    "Info",
    "Warn",
    "Debug",
    "Json",
    "Csv",
    "Session",
    "Service",
    "Payload",
    "Email",
    "Cliente",
    "Suporte",
}