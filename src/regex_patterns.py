# regex_patterns.py
"""
Módulo responsável pelo armazenamento centralizado
das expressões regulares utilizadas no sistema.

Os padrões definidos neste arquivo são utilizados
pelos módulos de:
- extração
- validação
- identificação de conteúdo

A separação das regex em um módulo específico
facilita:
- manutenção
- reutilização
- organização do projeto
- atualização dos padrões
"""


# ==================================================
# EMAILS
# ==================================================

# EMAIL_GERAL = r'\S+@\S+'
EMAIL_GERAL = (
    r'[a-zA-Z0-9._%+-]+'
    r'@[^\s]+'
)

EMAIL_VALIDO = (
    r'[a-zA-Z0-9._%+-]+'
    r'@'
    r'(?:[a-zA-Z0-9-]+\.)+'
    r'[a-zA-Z]{2,}'
)


# ==================================================
# TELEFONES
# ==================================================

TELEFONE_GERAL = r'[\(\)\d\s-]{8,}'

TELEFONE_VALIDO = (
    r'(?:\(\d{2}\)\s?|\d{2}\s?)'
    r'9?\d{4,5}-?\d{4}'
)


# ==================================================
# CPF
# ==================================================

CPF_GERAL = r'[\d.-]{11,14}'

CPF_VALIDO = r'\d{3}\.\d{3}\.\d{3}-\d{2}'


# ==================================================
# URL
# ==================================================

URL_GERAL = r'\S+\.\S+'

URL_VALIDA = r'(https?:\/\/)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(\S*)?'

# ==================================================
# OUTROS PADRÕES
# ==================================================
# Expressões auxiliares utilizadas para
# identificação de dados adicionais.

DATA = r'\b\d{2}/\d{2}/\d{4}\b'

HORARIO = r'\b\d{2}:\d{2}:\d{2}\b'

DATA_HORA = r'\b\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\b'

VALOR = r'R\$\s?\d{1,3}(?:\.\d{3})*,\d{2}'

NOME = (
    r'\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]'
    r'[a-záàâãéêíóôõúç]+'
    r'(?:\s[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]'
    r'[a-záàâãéêíóôõúç]+)+'
)
