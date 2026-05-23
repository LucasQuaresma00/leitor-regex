"""
padroes.py — Padrões regex de extração e validação.

Cada tipo tem dois padrões:
  - EXTRACAO: amplo, captura o máximo possível
  - VALIDACAO: rigoroso, define o que é válido

Critério para nomes próprios:
  - Mínimo 2 palavras, máximo 5
  - Cada token: maiúscula + minúsculas
  - Sem siglas, sem palavras da blacklist
  Justificativa: palavras únicas em maiúscula confundem
  com substantivos comuns; nomes compostos são muito mais
  precisos e reduzem falsos positivos.
"""

import re

EXTRACAO = {
    "email": re.compile(
        r'[a-zA-Z0-9._%+\-]+@[^\s<>"\']+',
    ),
    "telefone": re.compile(
        r'(?:\(?\d{2}\)?[\s\-]?)?(?:9\d{4}|\d{4})[\s\-]?\d{4}',
    ),
    "cpf": re.compile(
        r'\b\d{3}[\s.\-]?\d{3}[\s.\-]?\d{3}[\s.\-]?\d{2}\b',
    ),
    "data": re.compile(
        r'\b\d{1,2}[/.\-]\d{1,2}[/.\-]\d{4}\b',
    ),
    "horario": re.compile(
        r'\b\d{1,2}:\d{2}(?::\d{2})?\b',
    ),
    "datetime": re.compile(
        r'\b\d{1,2}[/.\-]\d{1,2}[/.\-]\d{4}\s+\d{1,2}:\d{2}(?::\d{2})?\b',
    ),
    "url": re.compile(
        r'https?://[^\s<>"]+|www\.[^\s<>"]+',
        re.IGNORECASE,
    ),
    "valor_monetario": re.compile(
        r'R\$\s?\d[\d.,]*',
    ),
    "nome_proprio": re.compile(
        r'\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{1,20}'
        r'(?:\s[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{1,20}){1,4}\b',
    ),
}

VALIDACAO = {
    "email": re.compile(
        r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$',
    ),
    "telefone": re.compile(
        r'^\(?\d{2}\)?[\s\-]?(?:9\d{4}|\d{4})[\s\-]?\d{4}$',
    ),
    "cpf": re.compile(
        r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    ),
    "data": re.compile(
        r'^(0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/\d{4}$',
    ),
    "horario": re.compile(
        r'^([01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$',
    ),
    "datetime": re.compile(
        r'^(0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/\d{4}'
        r'\s+([01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$',
    ),
    "url": re.compile(
        r'^https?://[a-zA-Z0-9\-]{1,63}(\.[a-zA-Z0-9\-]{1,63})+'
        r'\.[a-zA-Z]{2,6}(:\d{2,5})?([/?#][^\s]*)?$',
        re.IGNORECASE,
    ),
    "valor_monetario": re.compile(
        r'^R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?$',
    ),
    "nome_proprio": re.compile(
        r'^[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{1,20}'
        r'(?:\s[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{1,20}){1,4}$',
    ),
}

# Palavras que não são nomes próprios mesmo iniciando com maiúscula
NOMES_BLACKLIST = {
    "Urgente", "Erro", "Info", "Debug", "Aviso", "Arquivo", "Sistema",
    "Email", "Cliente", "Suporte", "Session", "Service", "Payload",
    "Json", "Csv", "True", "False", "None", "Error", "Warn",
}
