# Sistema de Análise Regex

## Objetivo

O projeto tem como objetivo realizar leitura, detecção, extração,
validação e geração de estatísticas sobre arquivos textuais
desestruturados utilizando Expressões Regulares (Regex)
como núcleo principal do processamento.

O sistema processa arquivos contendo:

- logs
- chats
- CSVs
- textos livres

identificando padrões estruturais e informações relevantes.

---

# Arquitetura Geral

O sistema utiliza uma arquitetura modular baseada em pipeline
de processamento.

Fluxo principal:

```text
Leitura
→ Detecção estrutural
→ Extração Regex
→ Validação estrutural
→ Validação semântica
→ Estatísticas
→ Exportação
```

Cada etapa possui responsabilidade isolada,
facilitando manutenção e evolução futura.

---

# Estrutura do Projeto

```text
src/
│
├── config.py
│
└── modules/
    ├── reader.py
    ├── detector.py
    ├── extractor.py
    ├── validator.py
    ├── statistics.py
    └── exporter.py
```

---

# Conceitos Utilizados

## 1. Modularização

O sistema é dividido em módulos independentes,
cada um responsável por uma etapa específica do processamento.

Objetivos:

- reduzir acoplamento
- facilitar manutenção
- melhorar organização
- permitir expansão futura

---

## 2. Separation of Concerns

Cada módulo possui responsabilidade única.

### reader.py

Responsável pela leitura e inspeção dos arquivos.

### detector.py

Responsável pela detecção estrutural do tipo de conteúdo.

### extractor.py

Responsável pela extração utilizando Regex.

### validator.py

Responsável pela validação estrutural e semântica.

### statistics.py

Responsável pela geração de métricas e estatísticas.

### exporter.py

Responsável pela exportação dos resultados.

---

## 3. Regex-Centric Architecture

Regex é o núcleo principal do projeto.

As expressões regulares são utilizadas para:

- detecção estrutural
- extração de dados
- validação estrutural
- classificação textual

O sistema foi projetado para manter Regex
como principal mecanismo de análise.

---

## 4. Validação em Camadas

A validação ocorre em múltiplas etapas:

```text
Extração Regex
→ Validação Estrutural
→ Validação Semântica
```

### Validação estrutural

Realizada através de expressões regulares.

### Validação semântica

Utilizada apenas quando Regex não é suficiente,
como no caso de CPF com dígitos verificadores.

---

## 5. Arquitetura Baseada em Configuração

O sistema utiliza configuração centralizada no arquivo:

```text
config.py
```

Nele são definidos:

- padrões Regex
- labels
- sinais estruturais
- regras de validação

Benefícios:

- fácil manutenção
- fácil expansão
- redução de código hardcoded

---

## 6. Heurísticas Estruturais

O módulo detector.py utiliza heurísticas baseadas em:

- score de padrões
- sinais regex
- análise percentual
- características estruturais

para identificar o tipo predominante do arquivo.

---

## 7. Data Classes

O projeto utiliza dataclasses para estruturar dados
internos do sistema.

Exemplos:

- Occurrence
- Statistics
- FileInspection

Benefícios:

- tipagem clara
- melhor organização
- maior legibilidade

---

# Estratégia de Extração

O sistema utiliza múltiplos padrões Regex para localizar:

- CPF
- e-mail
- telefone
- IP
- URL
- datas
- sessões
- nomes

As ocorrências extraídas são posteriormente normalizadas
e validadas.

---

# Estratégia de Exportação

Os resultados são exportados em:

- JSON
- CSV
- relatório textual

permitindo análise posterior dos dados processados.

---

# Considerações

O projeto prioriza:

- uso intensivo de Regex
- organização modular
- clareza arquitetural
- separação de responsabilidades
- validação multicamada

mantendo foco acadêmico em processamento textual
e análise baseada em expressões regulares.