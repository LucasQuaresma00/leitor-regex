"""
Módulo responsável pela identificação do tipo de conteúdo dos arquivos.
"""

import re


def identificar_tipo(linhas: list[str]) -> str:
    """
    Identifica o tipo do arquivo com base no conteúdo.
    Ordem de prioridade: CSV > LOG > CHAT > TEXTO LIVRE
    """
    if not linhas:
        return "TEXTO LIVRE"

    texto = "\n".join(linhas).lower()

    # ==================== CSV ====================
    if ";" in texto and any(header in texto for header in ["id;nome", "email;", "cpf;", "telefone;"]):
        return "CSV"

    # ==================== LOG ====================
    if any(tag in texto for tag in ["[info]", "[error]", "[warn]", "[debug]", "[warn]", "session="]):
        return "LOG"

    # ==================== CHAT ====================
    if re.search(r"\[\d{2}/\d{2}/\d{4}", texto) or "]: " in texto or "@" in texto and "msg=" in texto:
        return "CHAT"

    return "TEXTO LIVRE"