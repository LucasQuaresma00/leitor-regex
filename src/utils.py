# utils.py
"""
Módulo contendo funções utilitárias utilizadas
em diferentes partes do sistema.

As funções deste módulo auxiliam em tarefas
de apoio, como exibição de informações no terminal.
"""

def mostrar_amostra(conteudos, quantidade=3):
    """
    Exibe uma pequena amostra do conteúdo analisado.

    A função imprime no terminal uma quantidade
    limitada de linhas do conteúdo recebido,
    permitindo uma visualização rápida dos dados.

    Args:
        conteudos (list[str]):
            Lista contendo as linhas do arquivo
            ou conteúdo processado.

        quantidade (int, optional):
            Quantidade máxima de linhas que serão
            exibidas na amostra.
            Valor padrão: 3.

    Returns:
        None:
            A função apenas exibe informações
            no terminal.
    """

    print("\n--- AMOSTRA ---")

    for linha in conteudos[:quantidade]:
        print(linha)

    print()
