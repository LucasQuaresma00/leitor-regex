# identificador.py
"""
Módulo responsável pela identificação do tipo
de conteúdo presente nos arquivos analisados.

A identificação é feita com base em padrões
textuais encontrados no conteúdo do arquivo.
"""

import re


def identificar_tipo(conteudos):
    """
    Identifica o tipo geral do arquivo com base
    em padrões encontrados no conteúdo textual.

    Regras utilizadas:
    - Presença de ';' e cabeçalho típico -> CSV
    - Presença de padrão de data de chat -> CHAT
    - Presença de tags de log -> LOG
    - Demais casos -> TEXTO LIVRE

    Args:
        conteudos (list[str]):
            Lista contendo as linhas do arquivo.

    Returns:
        str:
            Tipo identificado do arquivo.
            Os valores possíveis são:
            - CSV
            - CHAT
            - LOG
            - TEXTO LIVRE
    """

    texto_completo = "\n".join(conteudos)

    # CSV
    if ";" in texto_completo and "id;nome;email" in texto_completo:
        return "CSV"

    # CHAT
    padrao_chat = r"\[\d{2}/\d{2}/\d{4}"

    if re.search(padrao_chat, texto_completo):
        return "CHAT"

    # LOG
    if any(tag in texto_completo for tag in ["[INFO]", "[ERROR]", "[WARN]", "[DEBUG]"]):
        return "LOG"

    # TEXTO LIVRE
    return "TEXTO LIVRE"
