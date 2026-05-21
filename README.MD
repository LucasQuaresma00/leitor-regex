# 📌 Visão geral do sistema

Este projeto é um sistema de processamento e análise de arquivos utilizando expressões regulares. Ele realiza a leitura de arquivos diversos, identifica seu tipo, extrai padrões estruturados (como emails, CPFs, URLs e telefones), valida os dados e gera estatísticas e relatórios em formato JSON para consumo posterior por um frontend.

---

# 🧩 Arquitetura do sistema

O sistema é modular e dividido em camadas com responsabilidades bem definidas:

---

# 🚀 main.py

Responsável por iniciar a aplicação e orquestrar a execução geral do sistema.

Sua função é percorrer os arquivos configurados, chamar o `processador.py` para executar o pipeline completo e exportar os resultados individuais em JSON.

---

# ⚙ processador.py

É o núcleo do sistema (orquestrador do fluxo de processamento).

Centraliza todas as etapas do pipeline:

- leitura do arquivo
- identificação do tipo
- extração de padrões
- validação de dados
- geração de estatísticas
- geração de relatórios

---

# 📖 leitor.py

Responsável pela leitura dos arquivos de entrada.

Executa operações como:
- leitura do conteúdo do arquivo
- retorno das linhas em memória
- contagem de linhas
- suporte à análise inicial

---

# 🧠 identificador.py

Responsável pela identificação do tipo de arquivo.

Detecta padrões estruturais como:
- CSV
- LOG
- CHAT
- TEXTO LIVRE

---

# 🔍 extrator.py

Responsável pela extração de informações estruturadas do texto.

Utiliza expressões regulares para localizar padrões como:
- emails
- telefones
- CPFs
- URLs

Também associa cada ocorrência à sua classificação inicial.

---

# 📌 regex_patterns.py

Centraliza todas as expressões regulares do sistema.

Permite manutenção simplificada e reutilização dos padrões em diferentes módulos.

---

# 🧪 classificador.py

Responsável pela validação dos dados extraídos.

Verifica se os padrões seguem formatos válidos definidos pelas regras do sistema, incluindo:
- email
- telefone
- CPF
- URL

---

# 📊 validador_csv.py

Responsável pela validação estrutural de arquivos CSV.

Detecta inconsistências como:
- número incorreto de colunas
- linhas malformadas

---

# 📈 estatisticas.py

Responsável pela geração de métricas do sistema.

Gera indicadores como:
- total por tipo de dado
- quantidade de válidos e inválidos
- distribuição por arquivo

---

# 📑 relatorio.py

Responsável pela consolidação dos dados processados.

Agrupa ocorrências por:
- arquivo
- tipo
- classificação

---

# 💾 exportador.py

Responsável pela exportação dos resultados.

Salva os dados processados em arquivos JSON para consumo externo.

---

# 🛠 utils.py

Contém funções auxiliares utilizadas pelo sistema.

Inclui utilitários para suporte geral ao processamento e exibição de dados.

---

# 🔄 Fluxo de execução do sistema

O processamento ocorre na seguinte sequência:

1. **main.py** inicia o sistema  
2. **processador.py** coordena todo o pipeline  
3. **leitor.py** realiza a leitura dos arquivos  
4. **identificador.py** identifica o tipo do arquivo  
5. **extrator.py** extrai padrões usando regex  
6. **classificador.py** valida os padrões encontrados  
7. **validador_csv.py** valida estrutura de CSV (quando aplicável)  
8. **estatisticas.py** gera métricas e indicadores  
9. **relatorio.py** consolida os resultados  
10. **exportador.py** salva os dados em JSON  
11. **frontend** consome os JSONs e exibe o dashboard  

---

# 📊 Frontend

O frontend é responsável por consumir os arquivos JSON gerados pelo backend e apresentar os dados em formato de dashboard interativo, permitindo análise visual das ocorrências e estatísticas.

---

# 💡 Observação de arquitetura

O sistema segue uma abordagem modular inspirada em boas práticas de engenharia de software, separando responsabilidades entre:

- leitura
- processamento
- validação
- análise
- apresentação