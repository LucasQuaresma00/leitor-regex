"""
Módulo responsável pela geração de relatórios por arquivo.
"""

from collections import defaultdict


def gerar_relatorio(resultados: list[dict]) -> dict:
    """
    Gera um relatório consolidado por arquivo e por tipo.
    """
    relatorio = defaultdict(
        lambda: defaultdict(
            lambda: {"total": 0, "valido": 0, "invalido": 0, "não_aplicável": 0}
        )
    )

    for occ in resultados:
        arquivo = occ["arquivo"]
        tipo = occ["tipo"]
        status = occ.get("classificacao", "não_aplicável")

        relatorio[arquivo][tipo]["total"] += 1
        if status in relatorio[arquivo][tipo]:
            relatorio[arquivo][tipo][status] += 1

    # Converte defaultdict para dict normal
    return {
        arquivo: dict(tipos) 
        for arquivo, tipos in relatorio.items()
    }