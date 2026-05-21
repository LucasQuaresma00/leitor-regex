"""
Módulo responsável pela validação estrutural de arquivos CSV.
Versão melhorada para arquivos sujos.
"""

def validar_csv(linhas: list[str], nome_arquivo: str):
    """
    Valida a estrutura do CSV e reporta inconsistências.
    """
    inconsistencias = []
    linhas_validas = [linha.strip() for linha in linhas if linha.strip()]

    if not linhas_validas:
        return inconsistencias

    # Cabeçalho
    cabecalho = linhas_validas[0]
    colunas_esperadas = len(cabecalho.split(";"))

    print(f"   Cabeçalho tem {colunas_esperadas} colunas")

    for num_linha, linha in enumerate(linhas_validas[1:], start=2):
        colunas_encontradas = len(linha.split(";"))

        if colunas_encontradas != colunas_esperadas:
            valor_truncado = linha[:120] + "..." if len(linha) > 120 else linha

            inconsistencias.append({
                "tipo": "csv_inconsistente",
                "valor": valor_truncado,
                "arquivo": nome_arquivo,
                "classificacao": "invalido",
                "linha": num_linha,
                "colunas_esperadas": colunas_esperadas,
                "colunas_encontradas": colunas_encontradas,
                "descricao": f"Esperado {colunas_esperadas} colunas, encontrado {colunas_encontradas}"
            })

    total_linhas = len(linhas_validas) - 1  # menos o cabeçalho
    print(f"   Total de linhas analisadas: {total_linhas} | Inconsistências: {len(inconsistencias)}")

    return inconsistencias