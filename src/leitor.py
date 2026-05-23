"""
leitor.py — Leitura e inspeção dos arquivos de entrada.

Responsabilidades:
  - Ler arquivo com fallback de encoding
  - Contar linhas e identificar linhas vazias
  - Detectar o tipo de conteúdo (csv, log, chat, texto_livre)
  - Retornar uma amostra de linhas
"""

import os
import re


def ler_arquivo(caminho: str) -> dict:
    """Lê um arquivo e retorna suas informações de inspeção."""
    nome = os.path.basename(caminho)
    linhas = []

    for enc in ("utf-8", "latin-1"):
        try:
            with open(caminho, "r", encoding=enc, errors="replace") as f:
                linhas = [l.rstrip("\n") for l in f.readlines()]
            encoding = enc
            break
        except Exception:
            encoding = "desconhecido"

    tipo = _detectar_tipo(nome, linhas)
    amostra = [l for l in linhas if l.strip()][:5]

    return {
        "nome":          nome,
        "caminho":       caminho,
        "encoding":      encoding,
        "total_linhas":  len(linhas),
        "linhas_vazias": sum(1 for l in linhas if not l.strip()),
        "tipo":          tipo,
        "amostra":       amostra,
        "linhas":        linhas,
    }


def _detectar_tipo(nome: str, linhas: list[str]) -> str:
    """
    Identifica o tipo geral do arquivo por heurística de conteúdo.
      - csv:         maioria das linhas tem múltiplos ';' ou ','
      - log:         linhas com [INFO/WARN/ERROR] ou timestamp ISO
      - chat:        linhas com padrão [DD/MM/YYYY HH:MM] Usuário:
      - texto_livre: tudo que não se encaixa nos anteriores
    """
    if nome.endswith(".csv"):
        return "csv"

    amostra = [l for l in linhas[:100] if l.strip()]
    total = len(amostra) or 1

    score_log  = sum(1 for l in amostra if re.search(r'\[(INFO|WARN|ERROR|DEBUG)\]|\d{4}-\d{2}-\d{2}T', l))
    score_chat = sum(1 for l in amostra if re.search(r'^\[\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}', l))
    score_csv  = sum(1 for l in amostra if l.count(';') >= 2 or l.count(',') >= 2)

    if score_csv  / total >= 0.4: return "csv"
    if score_chat / total >= 0.2: return "chat"
    if score_log  / total >= 0.2: return "log"
    return "texto_livre"
