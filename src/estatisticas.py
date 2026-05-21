"""
Módulo responsável pela geração de estatísticas consolidadas.
"""

from collections import Counter, defaultdict


def gerar_estatisticas(resultados: list[dict]) -> dict:
    """
    Gera estatísticas completas a partir das ocorrências.
    """
    if not resultados:
        return {
            "total_por_tipo": {},
            "validos_invalidos": {},
            "distribuicao_arquivos": {}
        }

    # Total por tipo
    total_por_tipo = Counter()

    # Válidos x Inválidos por tipo
    validos_invalidos = defaultdict(lambda: {"valido": 0, "invalido": 0, "não_aplicável": 0})

    # Distribuição por arquivo
    distribuicao_arquivos = defaultdict(Counter)

    for occ in resultados:
        tipo = occ["tipo"]
        arquivo = occ["arquivo"]
        classificacao = occ.get("classificacao", "não_aplicável")

        total_por_tipo[tipo] += 1
        validos_invalidos[tipo][classificacao] += 1
        distribuicao_arquivos[arquivo][tipo] += 1

    return {
        "total_por_tipo": dict(total_por_tipo),
        "validos_invalidos": {
            k: dict(v) for k, v in validos_invalidos.items()
        },
        "distribuicao_arquivos": {
            k: dict(v) for k, v in distribuicao_arquivos.items()
        },
        "total_ocorrencias": len(resultados)
    }