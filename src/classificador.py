"""
Módulo responsável pela validação dos padrões extraídos.
"""

import re
from regex_patterns import (
    EMAIL_VALIDO,
    TELEFONE_VALIDO,
    CPF_VALIDO,
    URL_VALIDA,
    DATA_HORA,
    VALOR,
    NOME
)


def validar_email(email: str) -> bool:
    return bool(re.fullmatch(EMAIL_VALIDO, email.strip()))


def validar_telefone(telefone: str) -> bool:
    return bool(re.fullmatch(TELEFONE_VALIDO, telefone.strip()))


def validar_cpf(cpf: str) -> bool:
    return bool(re.fullmatch(CPF_VALIDO, cpf.strip()))


def validar_url(url: str) -> bool:
    return bool(re.fullmatch(URL_VALIDA, url.strip()))


# === Novos validadores ===
def validar_data_hora(valor: str) -> bool:
    return bool(re.fullmatch(DATA_HORA, valor.strip()))


def validar_valor_monetario(valor: str) -> bool:
    return bool(re.fullmatch(VALOR, valor.strip()))


def validar_nome_proprio(nome: str) -> bool:
    return bool(re.fullmatch(NOME, nome.strip()))