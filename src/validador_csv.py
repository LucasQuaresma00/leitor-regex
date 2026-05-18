# validador_csv.py
"""
Módulo responsável pela validação estrutural
de arquivos CSV.

A validação verifica se todas as linhas do
arquivo possuem a mesma quantidade de colunas
definida no cabeçalho.
"""

def validar_csv(linhas, nome_arquivo):
    """
    Valida a consistência estrutural de um arquivo CSV.

    A função analisa se todas as linhas possuem
    a mesma quantidade de colunas do cabeçalho.
    Caso encontre divergências, registra as
    inconsistências identificadas.

    Regras de validação:
    - Linhas vazias são ignoradas.
    - O cabeçalho define a quantidade esperada
      de colunas.
    - Linhas com quantidade diferente de colunas
      são classificadas como inválidas.

    Args:
        linhas (list[str]):
            Lista contendo as linhas do arquivo CSV.

        nome_arquivo (str):
            Nome do arquivo analisado.

    Returns:
        list[dict]:
            Lista contendo as inconsistências
            encontradas durante a validação.

            Cada inconsistência possui:
            - tipo
            - valor
            - arquivo
            - classificacao
            - linha
            - colunas_esperadas
            - colunas_encontradas
    """
    inconsistencias = []

    # Remove linhas vazias
    linhas = [
        linha for linha in linhas
        if linha.strip()
    ]

    if not linhas:
        return inconsistencias

    # Cabeçalho
    cabecalho = linhas[0]

    quantidade_esperada = len(
        cabecalho.split(";")
    )

    # Verificar linhas
    for numero_linha, linha in enumerate(
        linhas[1:],
        start=2
    ):

        quantidade_colunas = len(
            linha.split(";")
        )

        if quantidade_colunas != quantidade_esperada:

            inconsistencias.append({
                "tipo": "csv_inconsistente",
                "valor": linha,
                "arquivo": nome_arquivo,
                "classificacao": "invalido",
                "linha": numero_linha,
                "colunas_esperadas": quantidade_esperada,
                "colunas_encontradas": quantidade_colunas
            })

    return inconsistencias
