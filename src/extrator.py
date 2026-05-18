# extrator.py
"""
Módulo responsável pela extração de padrões
textuais presentes nos arquivos analisados.

O módulo utiliza expressões regulares para
identificar diferentes tipos de informações
no conteúdo dos arquivos, como:
- e-mails
- telefones
- CPF
- URLs

Após a extração, cada ocorrência é validada
e estruturada em um formato padronizado.
"""

import re

from regex_patterns import *

from classificador import (
    validar_email,
    validar_telefone,
    validar_cpf,
    validar_url
)


def criar_ocorrencia(
tipo,
    valor,
    arquivo,
    classificacao="não_aplicável"
):
    
    """
    Cria uma estrutura padronizada de ocorrência.

    A função organiza os dados encontrados
    durante a extração em um dicionário
    estruturado, facilitando o processamento
    e exportação das informações.

    Args:
        tipo (str):
            Tipo da informação identificada.
            Exemplo:
            - email
            - telefone
            - cpf
            - url

        valor (str):
            Valor encontrado no conteúdo analisado.

        arquivo (str):
            Nome do arquivo onde a ocorrência
            foi identificada.

        classificacao (str, optional):
            Resultado da validação da ocorrência.
            Valor padrão:
            "não_aplicável".

    Returns:
        dict:
            Estrutura contendo os dados
            padronizados da ocorrência.
    """

    return {
        "tipo": tipo,
        "valor": valor,
        "arquivo": arquivo,
        "classificacao": classificacao
    }


def extrair_padroes(linhas, nome_arquivo):
    """
    Extrai padrões textuais de um conteúdo
    utilizando expressões regulares.

    A função realiza buscas por diferentes
    tipos de informações no texto e valida
    cada valor encontrado utilizando funções
    específicas do módulo classificador.

    Padrões analisados:
    - e-mails
    - telefones
    - CPF
    - URLs

    Args:
        linhas (list[str]):
            Lista contendo as linhas do arquivo.

        nome_arquivo (str):
            Nome do arquivo analisado.

    Returns:
        list[dict]:
            Lista contendo todas as ocorrências
            identificadas no conteúdo.

            Cada ocorrência possui:
            - tipo
            - valor
            - arquivo
            - classificacao
    """
    
    resultados = []

    texto = "\n".join(linhas)

    # ==========================================
    # EMAILS
    # ==========================================

    emails = re.findall(EMAIL_GERAL, texto)

    for email in emails:

        status = (
            "valido"
            if validar_email(email)
            else "invalido"
        )

        resultados.append(
            criar_ocorrencia(
                "email",
                email,
                nome_arquivo,
                status
            )
        )

    # ==========================================
    # TELEFONES
    # ==========================================

    telefones = re.findall(TELEFONE_GERAL, texto)

    for telefone in telefones:

        telefone = telefone.strip()

        status = (
            "valido"
            if validar_telefone(telefone)
            else "invalido"
        )

        resultados.append(
            criar_ocorrencia(
                "telefone",
                telefone,
                nome_arquivo,
                status
            )
        )

    # ==========================================
    # CPF
    # ==========================================

    cpfs = re.findall(CPF_GERAL, texto)

    for cpf in cpfs:

        status = (
            "valido"
            if validar_cpf(cpf)
            else "invalido"
        )

        resultados.append(
            criar_ocorrencia(
                "cpf",
                cpf,
                nome_arquivo,
                status
            )
        )

    # ==========================================
    # URL
    # ==========================================

    urls = re.findall(URL_GERAL, texto)

    for url in urls:

        status = (
            "valido"
            if validar_url(url)
            else "invalido"
        )

        resultados.append(
            criar_ocorrencia(
                "url",
                url,
                nome_arquivo,
                status
            )
        )

    return resultados
