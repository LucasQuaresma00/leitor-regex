"""
Módulo responsável pela extração de padrões textuais.
Versão corrigida e completa.
"""

import re
from regex_patterns import compilar_patterns
from classificador import (
    validar_email,
    validar_telefone,
    validar_cpf,
    validar_url,
    validar_data_hora,
    validar_data,
    validar_horario,
    validar_valor_monetario,
    validar_nome_proprio
)


def criar_ocorrencia(tipo: str, valor: str, arquivo: str, classificacao: str = "não_aplicável"):
    return {
        "tipo": tipo,
        "valor": valor.strip(),
        "arquivo": arquivo,
        "classificacao": classificacao
    }


def extrair_padroes(linhas: list, nome_arquivo: str):
    resultados = []
    texto = "\n".join(linhas)
    
    patterns = compilar_patterns()

    # ==================== EMAIL ====================
    for match in patterns["email_geral"].finditer(texto):
        valor = match.group()
        status = "valido" if validar_email(valor) else "invalido"
        resultados.append(criar_ocorrencia("email", valor, nome_arquivo, status))

    # ==================== TELEFONE ====================
    for match in patterns["telefone_geral"].finditer(texto):
        valor = match.group()
        status = "valido" if validar_telefone(valor) else "invalido"
        resultados.append(criar_ocorrencia("telefone", valor, nome_arquivo, status))

    # ==================== CPF ====================
    for match in patterns["cpf_geral"].finditer(texto):
        valor = match.group()
        status = "valido" if validar_cpf(valor) else "invalido"
        resultados.append(criar_ocorrencia("cpf", valor, nome_arquivo, status))

    # ==================== URL ====================
    for match in patterns["url_geral"].finditer(texto):
        valor = match.group()
        status = "valido" if validar_url(valor) else "invalido"
        resultados.append(criar_ocorrencia("url", valor, nome_arquivo, status))

    # ==================== OUTROS ====================
    for match in patterns["data"].finditer(texto):
        valor = match.group()
        status = "valido" if validar_data(valor) else "invalido"
        resultados.append(criar_ocorrencia("data", valor, nome_arquivo, status))

    for match in patterns["horario"].finditer(texto):
        valor = match.group()
        status = "valido" if validar_horario(valor) else "invalido"
        resultados.append(criar_ocorrencia("horario", valor, nome_arquivo, status))

    for match in patterns["data_hora"].finditer(texto):
        valor = match.group()
        status = "valido" if validar_data_hora(valor) else "invalido"
        resultados.append(criar_ocorrencia("data_hora", valor, nome_arquivo, status))

    for match in patterns["valor"].finditer(texto):
        valor = match.group()
        status = "valido" if validar_valor_monetario(valor) else "invalido"
        resultados.append(criar_ocorrencia("valor_monetario", valor, nome_arquivo, status))

    for match in patterns["nome"].finditer(texto):
        valor = match.group()
        status = "valido" if validar_nome_proprio(valor) else "invalido"
        resultados.append(criar_ocorrencia("nome_proprio", valor, nome_arquivo, status))

    return resultados