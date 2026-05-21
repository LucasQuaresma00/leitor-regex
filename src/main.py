"""
Módulo principal do sistema de processamento
de arquivos com expressões regulares.
"""

import os
from leitor import ler_arquivo, contar_linhas
from processador import processar_arquivo
from exportador import salvar_json
from estatisticas import gerar_estatisticas
from relatorio import gerar_relatorio


# Configurações
PASTA_DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados")

ARQUIVOS = [
    "01_atendimentos_bagunçados.txt",
    "02_logs_mistos.log",
    "03_mensagens_chat.txt",
    "04_exportacao_suja.csv"
]


def mostrar_amostra(linhas, quantidade=5):
    print("\n--- AMOSTRA DO ARQUIVO ---")
    for linha in linhas[:quantidade]:
        print(linha[:120])  # limita largura
    print("-" * 60)


def mostrar_resumo(resultados, limite=8):
    print(f"\n--- RESUMO DE OCORRÊNCIAS ({len(resultados)} encontradas) ---")
    for occ in resultados[:limite]:
        print(f"[{occ['tipo'].upper():12}] {occ['valor'][:80]:80} → {occ['classificacao']}")
    if len(resultados) > limite:
        print(f"... e mais {len(resultados) - limite} ocorrências")


def main():
    print("=" * 70)
    print("🚀 PROCESSADOR DE ARQUIVOS COM REGEX - VERSÃO OTIMIZADA")
    print("=" * 70)

    todos_resultados = []

    for nome_arquivo in ARQUIVOS:
        caminho = os.path.join(PASTA_DADOS, nome_arquivo)

        print(f"\n📄 Processando: {nome_arquivo}")

        # Processamento completo do arquivo
        resultado_processamento = processar_arquivo(caminho, nome_arquivo)

        todos_resultados.extend(resultado_processamento["ocorrencias"])

        # Exibição
        mostrar_amostra(resultado_processamento["linhas"])
        mostrar_resumo(resultado_processamento["ocorrencias"])

        # Salvar JSON individual
        nome_saida = nome_arquivo.split(".")[0]
        salvar_json(nome_saida, resultado_processamento)

    # ====================== RELATÓRIOS GERAIS ======================
    print("\n" + "=" * 70)
    print("📊 GERANDO RELATÓRIOS GERAIS")
    print("=" * 70)

    estatisticas = gerar_estatisticas(todos_resultados)
    relatorio = gerar_relatorio(todos_resultados)

    # JSON Final
    estrutura_geral = {
        "resumo_execucao": {
            "total_arquivos": len(ARQUIVOS),
            "total_ocorrencias": len(todos_resultados)
        },
        "estatisticas": estatisticas,
        "relatorio": relatorio,
        "ocorrencias": todos_resultados
    }

    salvar_json("resultados_gerais", estrutura_geral)

    # Exibição final no terminal
    print("\n✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print(f"Total de ocorrências extraídas: {len(todos_resultados)}")

    print("\n--- TOTAL POR TIPO ---")
    for tipo, qtd in estatisticas["total_por_tipo"].items():
        print(f"  {tipo.upper():15}: {qtd}")


if __name__ == "__main__":
    main()