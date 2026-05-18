# estatisticas.py
"""
Módulo responsável pela geração de estatísticas
das ocorrências identificadas durante o processo
de inspeção dos arquivos.

O módulo organiza informações quantitativas
sobre:
- total de ocorrências por tipo
- quantidade de válidos e inválidos
- distribuição das ocorrências por arquivo
"""

from collections import Counter
from collections import defaultdict


def gerar_estatisticas(resultados):
    """
    Gera estatísticas consolidadas a partir das
    ocorrências processadas pelo sistema.

    A função percorre todas as ocorrências
    encontradas e produz métricas organizadas
    em diferentes categorias estatísticas.

    Estatísticas geradas:
    - Total de ocorrências por tipo
    - Quantidade de válidos e inválidos
    - Distribuição das ocorrências por arquivo

    Args:
        resultados (list[dict]):
            Lista contendo as ocorrências
            identificadas durante a análise.

            Cada ocorrência deve possuir:
            - tipo
            - arquivo
            - classificacao

    Returns:
        dict:
            Estrutura contendo todas as
            estatísticas calculadas.

            Estrutura retornada:
            {
                "total_por_tipo": {},
                "validos_invalidos": {},
                "distribuicao_arquivos": {}
            }
    """
    
    estatisticas = {}

    # ==========================================
    # TOTAL POR TIPO
    # ==========================================

    total_por_tipo = Counter()

    # ==========================================
    # VALIDOS / INVALIDOS
    # ==========================================

    validos_invalidos = defaultdict(
        lambda: {
            "valido": 0,
            "invalido": 0,
            "não_aplicável": 0
        }
    )

    # ==========================================
    # DISTRIBUIÇÃO POR ARQUIVO
    # ==========================================

    distribuicao_arquivos = defaultdict(Counter)

    # ==========================================
    # PROCESSAMENTO
    # ==========================================

    for ocorrencia in resultados:

        tipo = ocorrencia["tipo"]

        arquivo = ocorrencia["arquivo"]

        classificacao = ocorrencia["classificacao"]

        # Total por tipo
        total_por_tipo[tipo] += 1

        # Validos / invalidos
        validos_invalidos[tipo][classificacao] += 1

        # Distribuição por arquivo
        distribuicao_arquivos[arquivo][tipo] += 1

    # ==========================================
    # ORGANIZAR RESULTADO
    # ==========================================

    estatisticas["total_por_tipo"] = dict(total_por_tipo)

    estatisticas["validos_invalidos"] = {
        k: dict(v)
        for k, v in validos_invalidos.items()
    }

    estatisticas["distribuicao_arquivos"] = {
        k: dict(v)
        for k, v in distribuicao_arquivos.items()
    }

    return estatisticas

