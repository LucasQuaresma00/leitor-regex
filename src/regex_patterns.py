"""
Módulo central de padrões regex.
Separação clara: GERAL (extração ampla) × VALIDO (validação rigorosa)
"""

import re

# ==================== EMAILS ====================
EMAIL_GERAL = r'[a-zA-Z0-9._%+-]+@[^\s<>"\']+'
EMAIL_VALIDO = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# ==================== TELEFONES ====================
TELEFONE_GERAL = r'(?![\n])[\(\)\d\s-]{8,}'
TELEFONE_VALIDO = r'^(?:\(\d{2}\)\s?|\d{2}\s?)9\d{4}-?\d{4}$'
# ==================== CPF ====================
CPF_GERAL = r'\d{3}[\s.-]?\d{3}[\s.-]?\d{3}[\s.-]?\d{2}'
CPF_VALIDO = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'

# ==================== URL ====================
URL_GERAL = r'https?://[^\s<>"]+|www\.[^\s<>"]+[^\s<>"]*'
URL_VALIDA = r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/[^\s<>"]*)?$'

# ==================== OUTROS ====================
DATA = r'\b\d{2}[/.-]\d{2}[/.-]\d{4}\b'
DATA_VALIDA = r'^(?:(?:31([/.-])(?:0?[13578]|1[02]))\1|(?:(?:29|30)([/.-])(?:0?[1,3-9]|1[0-2])\2))(?:1[6-9]|[2-9]\d)?\d{2}$|^(?:29([/.-])0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])([/.-])(?:(?:0?[1-9])|(?:1[0-2]))\4(?:1[6-9]|[2-9]\d)?\d{2}$'

HORARIO = r'\b\d{1,2}:\d{2}(?::\d{2})?\b'
HORARIO_VALIDO = r'^(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$'

DATA_HORA = r'\b\d{2}[/.-]\d{2}[/.-]\d{4}\s+\d{1,2}:\d{2}(?::\d{2})?\b'
VALOR = r'R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?'

NOME = r'\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+(?:\s[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+){1,4}\b'


def compilar_patterns():
    """Compila todas as regex para melhor performance."""
    return {
        "email_geral": re.compile(EMAIL_GERAL, re.IGNORECASE),
        "email_valido": re.compile(EMAIL_VALIDO, re.IGNORECASE),
        "telefone_geral": re.compile(TELEFONE_GERAL),
        "telefone_valido": re.compile(TELEFONE_VALIDO),
        "cpf_geral": re.compile(CPF_GERAL),
        "cpf_valido": re.compile(CPF_VALIDO),
        "url_geral": re.compile(URL_GERAL, re.IGNORECASE),
        "url_valida": re.compile(URL_VALIDA, re.IGNORECASE),
        "data": re.compile(DATA),
        "data_valida": re.compile(DATA_VALIDA),
        "horario": re.compile(HORARIO),
        "horario_valido": re.compile(HORARIO_VALIDO),
        "data_hora": re.compile(DATA_HORA),
        "valor": re.compile(VALOR),
        "nome": re.compile(NOME),
    }