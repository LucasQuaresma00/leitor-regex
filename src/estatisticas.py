"""
estatisticas.py — Análise quantitativa das ocorrências extraídas.

Produz:
  - total geral de ocorrências
  - quantidade por tipo
  - válidos e inválidos por tipo
  - distribuição por arquivo
"""

from collections import defaultdict

# Definição de entrada e saida da funcao para fins de lembranca
# loop obtido O(n)
# Nota[Melhoria] possivel melhoria estatisticas por arquivo futura
def calcular(ocorrencias: list[dict]) -> dict:
    """Calcula estatísticas sobre as ocorrências extraídas."""
    por_tipo     = defaultdict(int)
    validos      = defaultdict(int)
    invalidos    = defaultdict(int)
    por_arquivo  = defaultdict(int)

    for occ in ocorrencias:
        tipo = occ["tipo"]
        por_tipo[tipo]    += 1
        por_arquivo[occ["arquivo"]] += 1

        if occ["classificacao"] == "valido":
            validos[tipo] += 1
        elif occ["classificacao"] == "invalido":
            invalidos[tipo] += 1

    return {
        "total_geral":      len(ocorrencias),
        "por_tipo":         dict(por_tipo),
        "validos_por_tipo": dict(validos),
        "invalidos_por_tipo": dict(invalidos),
        "por_arquivo":      dict(por_arquivo),
    }
