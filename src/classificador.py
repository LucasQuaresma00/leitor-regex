# classificador.py

"""
Módulo responsável pela validação de padrões
textuais identificados durante a inspeção
dos arquivos.

O módulo utiliza expressões regulares para
verificar se os dados encontrados seguem
formatos considerados válidos.

Tipos suportados:
- e-mail
- telefone
- CPF
- URL
"""

import re

from regex_patterns import (
    EMAIL_VALIDO,
    TELEFONE_VALIDO,
    CPF_VALIDO,
    URL_VALIDA
)


def validar_email(email):
    """
    Valida o formato de um endereço de e-mail.

    A validação é realizada utilizando uma
    expressão regular definida no módulo
    regex_patterns.

    Args:
        email (str):
            Endereço de e-mail que será validado.

    Returns:
        bool:
            True caso o e-mail seja válido.
            False caso o formato seja inválido.
    """

    return bool(
        re.fullmatch(EMAIL_VALIDO, email)
    )


def validar_telefone(telefone):
    """
    Valida o formato de um número de telefone.

    A validação considera o padrão definido
    pela expressão regular TELEFONE_VALIDO.

    Args:
        telefone (str):
            Número de telefone que será validado.

    Returns:
        bool:
            True caso o telefone seja válido.
            False caso o formato seja inválido.
    """
    return bool(
        re.fullmatch(TELEFONE_VALIDO, telefone)
    )


def validar_cpf(cpf):
    """
    Valida o formato de um CPF.

    A verificação é realizada utilizando uma
    expressão regular definida no módulo
    regex_patterns.

    Observação:
        Esta validação verifica apenas o
        formato textual do CPF, não os
        dígitos verificadores oficiais.

    Args:
        cpf (str):
            CPF que será validado.

    Returns:
        bool:
            True caso o CPF possua formato válido.
            False caso o formato seja inválido.
    """
    return bool(
        re.fullmatch(CPF_VALIDO, cpf)
    )


def validar_url(url):
    # Essa bomba esta considerando tudo invalido lembrar de trocar o regex
    """
    Valida o formato de uma URL.

    A validação é baseada em uma expressão
    regular definida no módulo regex_patterns.

    Args:
        url (str):
            URL que será validada.

    Returns:
        bool:
            True caso a URL seja válida.
            False caso o formato seja inválido.
    """

    return bool(
        re.fullmatch(URL_VALIDA, url)
    )

