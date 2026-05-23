"""
main.py — Orquestrador do analisador de padrões Regex.

Fluxo:
  1. Leitura e inspeção dos arquivos   (src/leitor.py)
  2. Extração e classificação          (src/extrator.py)
  3. Estatísticas                      (src/estatisticas.py)
  4. Exportação JSON/CSV/TXT           (src/exportador.py)
"""

import os, sys

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR  = os.path.join(BASE_DIR, "dados")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

sys.path.insert(0, BASE_DIR)

from src.leitor       import ler_arquivo
from src.extrator     import extrair
from src.estatisticas import calcular
from src.exportador   import exportar_json, exportar_csv, exportar_relatorio

ARQUIVOS = [
    "01_atendimentos_bagunçados.txt",
    "02_logs_mistos.log",
    "03_mensagens_chat.txt",
    "04_exportacao_suja.csv",
]


def main():
    print("\n══════════════════════════════════════════════════════")
    print("  ANALISADOR REGEX")
    print("══════════════════════════════════════════════════════")

    # ── 1. Leitura ──────────────────────────────────────────
    print("\n[1] Leitura e inspeção dos arquivos")
    arquivos = []
    for nome in ARQUIVOS:
        caminho = os.path.join(DADOS_DIR, nome)
        if not os.path.exists(caminho):
            print(f"  ⚠ Não encontrado: {nome}")
            continue
        arq = ler_arquivo(caminho)
        arquivos.append(arq)
        print(f"  ✔ {arq['nome']}")
        print(f"    Linhas : {arq['total_linhas']:,} | Tipo: {arq['tipo']}")
        print(f"    Amostra: {arq['amostra'][0][:80] if arq['amostra'] else '(vazio)'}")

    if not arquivos:
        print("Nenhum arquivo carregado. Encerrando.")
        return

    # ── 2. Extração e classificação ─────────────────────────
    print("\n[2] Extração e classificação")
    todas = []
    for arq in arquivos:
        ocorrencias = extrair(arq)
        todas.extend(ocorrencias)
        print(f"  {arq['nome']}: {len(ocorrencias):,} ocorrências")

    print(f"\n  Total geral: {len(todas):,}")

    # ── 3. Estatísticas ─────────────────────────────────────
    print("\n[3] Estatísticas por tipo")
    stats = calcular(todas)
    print(f"  {'TIPO':<20} {'TOTAL':>7} {'VÁLIDO':>8} {'INVÁLIDO':>10}")
    print(f"  {'-'*20} {'-'*7} {'-'*8} {'-'*10}")
    for tipo in sorted(stats["por_tipo"]):
        t = stats["por_tipo"][tipo]
        v = stats["validos_por_tipo"].get(tipo, 0)
        i = stats["invalidos_por_tipo"].get(tipo, 0)
        print(f"  {tipo:<20} {t:>7} {v:>8} {i:>10}")

    # ── 4. Exportação ────────────────────────────────────────
    print("\n[4] Exportação")
    print(f"  JSON     : {exportar_json(todas, OUTPUT_DIR)}")
    print(f"  CSV      : {exportar_csv(todas, OUTPUT_DIR)}")
    print(f"  Relatório: {exportar_relatorio(arquivos, stats, OUTPUT_DIR)}")

    print("\n══════════════════════════════════════════════════════")
    print("  CONCLUÍDO")
    print("══════════════════════════════════════════════════════\n")


if __name__ == "__main__":
    main()
