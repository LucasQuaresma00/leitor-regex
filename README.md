# Analisador de Padrões Regex

Sistema de extração, classificação e visualização de padrões em texto via expressões regulares. Desenvolvido como trabalho acadêmico, atendendo os requisitos de leitura de arquivos, extração com regex, classificação válido/inválido, organização dos dados e análise quantitativa.

🌐 Acesse a versão online do dashboard via GitHub Pages: https://lucasquaresma00.github.io/leitor-regex/frontend/

---

## Requisitos

- Python 3.10 ou superior (sem dependências externas)
- Navegador moderno com suporte a ES Modules (Chrome, Firefox, Edge)
- Servidor HTTP local para o frontend (instrução abaixo)

---

## Como usar

### 1. Executar o backend

```bash
python main.py
```

O script lê os arquivos da pasta `dados/`, processa todos os padrões e grava os resultados em `output/`:

```
output/
├── resultados.json   ← consumido pelo dashboard
├── resultados.csv    ← para análise em planilhas
└── relatorio.txt     ← resumo estatístico em texto
```

### 2. Abrir o dashboard

O frontend usa ES Modules, que exigem um servidor HTTP — não funciona ao abrir o arquivo diretamente no navegador. Na raiz do projeto, execute:

```bash
python -m http.server 8000
```

Depois acesse: **http://localhost:8000/frontend/**

> O dashboard lê `output/resultados.json` automaticamente e exibe os cards, gráficos, filtros e tabela.

---

## Estrutura do projeto

```
regex_simples/
│
├── main.py                  # Orquestrador — ponto de entrada
│
├── src/                     # Módulos do backend
│   ├── padroes.py           # Dicionários de regex (extração e validação)
│   ├── leitor.py            # Leitura e inspeção dos arquivos
│   ├── extrator.py          # Extração de padrões e classificação
│   ├── estatisticas.py      # Análise quantitativa
│   └── exportador.py        # Geração de JSON, CSV e relatório TXT
│
├── frontend/                # Dashboard web
│   ├── index.html
│   ├── style.css
│   ├── app.js               # Ponto de entrada do frontend
│   └── js/
│       ├── charts.js        # Gráficos (Chart.js)
│       ├── table.js         # Renderização da tabela
│       └── filters.js       # Filtros interativos
│
├── dados/                   # Arquivos de entrada
│   ├── 01_atendimentos_bagunçados.txt
│   ├── 02_logs_mistos.log
│   ├── 03_mensagens_chat.txt
│   └── 04_exportacao_suja.csv
│
└── output/                  # Gerado pelo main.py
    ├── resultados.json
    ├── resultados.csv
    └── relatorio.txt
```
