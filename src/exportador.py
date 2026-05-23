"""
exportador.py — Exportação dos resultados em JSON, CSV e relatório TXT.

Cada ocorrência contém: tipo, valor, valor_normalizado, arquivo,
classificacao, status_final, confianca — campos compatíveis com o frontend.
"""

import os
import json
import csv


def exportar_json(ocorrencias: list[dict], output_dir: str) -> str:
    """Exporta ocorrências para arquivo JSON."""

    caminho = os.path.join(output_dir, "resultados.json")
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(ocorrencias, f, ensure_ascii=False, indent=2)
    return caminho


def exportar_csv(ocorrencias: list[dict], output_dir: str) -> str:
    """Exporta ocorrências para arquivo CSV."""
    
    caminho = os.path.join(output_dir, "resultados.csv")
    campos = ["tipo", "valor", "arquivo", "classificacao", "status_final", "confianca"]
    # Gera CSV separado por ';'
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(ocorrencias)
    return caminho


def exportar_relatorio(arquivos: list[dict], stats: dict, output_dir: str) -> str:
    """Gera relatório TXT consolidado da análise."""
    caminho = os.path.join(output_dir, "relatorio.txt")
    sep = "─" * 60

    linhas = [
        "╔════════════════════════════════════════════════╗",
        "║        RELATÓRIO — ANÁLISE REGEX               ║",
        "╚════════════════════════════════════════════════╝",
        "", sep, "1. ARQUIVOS PROCESSADOS", sep,
    ]

    for arq in arquivos:
        linhas += [
            f"  Arquivo : {arq['nome']}",
            f"  Tipo    : {arq['tipo']}",
            f"  Linhas  : {arq['total_linhas']}",
            f"  Encoding: {arq['encoding']}",
            f"  Amostra : {arq['amostra'][0][:80] if arq['amostra'] else '(vazio)'}",
            "",
        ]

    linhas += [
        sep, "2. ESTATÍSTICAS GERAIS", sep,
        f"  Total de ocorrências: {stats['total_geral']}",
        "",
        f"  {'TIPO':<20} {'TOTAL':>7} {'VÁLIDOS':>9} {'INVÁLIDOS':>10}",
        f"  {'-'*20} {'-'*7} {'-'*9} {'-'*10}",
    ]

    for tipo in sorted(stats["por_tipo"]):
        t = stats["por_tipo"][tipo]
        v = stats["validos_por_tipo"].get(tipo, 0)
        i = stats["invalidos_por_tipo"].get(tipo, 0)
        linhas.append(f"  {tipo:<20} {t:>7} {v:>9} {i:>10}")

    linhas += [
        "", sep, "3. DISTRIBUIÇÃO POR ARQUIVO", sep,
    ]
    for arq, total in sorted(stats["por_arquivo"].items()):
        linhas.append(f"  {arq:<45}: {total:>5} ocorrências")

    linhas += ["", sep, "FIM DO RELATÓRIO", sep]

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    return caminho
