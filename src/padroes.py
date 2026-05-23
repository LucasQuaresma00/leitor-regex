"""
padroes.py — Padrões regex de extração e validação.

Cada tipo tem dois padrões:
  - EXTRACAO: amplo, captura o máximo possível
  - VALIDACAO: rigoroso, define o que é válido

Critério para nomes próprios:
  - Mínimo 2 palavras, máximo 5
  - Cada token: maiúscula + minúsculas
  - Sem siglas, sem palavras da blacklist
  Justificativa: palavras únicas em maiúscula confundem
  com substantivos comuns; nomes compostos são muito mais
  precisos e reduzem falsos positivos.
"""

import re

EXTRACAO = {
    # Regex para capturar e-mails: valida o início com letras, números e 
    # símbolos comuns (+, -, _, ., %),
    # exige o caractere '@' e captura o domínio excluindo espaços (\s),
    #  tags (<>), aspas ("') e ponto e vírgula (;).
    "email": re.compile(
        r'[a-zA-Z0-9._%+\-]+@[^\s<>"\';\']+',
    ),
    # Regex captura sequências de 8 a 15 dígitos que contenham
    #  espaços, hifens ou parênteses
    "telefone": re.compile(
        r'(?:\(?\d{2}\)?[\s\-]?)?(?:9\d{4}|\d{4})[\s\-]?\d{4}',
    ),
    # Captura 11 dígitos isolados (\b), aceitando ou não
    # pontos, hifens e espaços entre os blocos.
    "cpf": re.compile(
        r'\b\d{3}[\s.\-]?\d{3}[\s.\-]?\d{3}[\s.\-]?\d{2}\b',
    ),
    # Captura formatos como (D OU DD)/MM/AAAA usando barras, pontos
    # ou hifens como separadores.
    "data": re.compile(
        r'\b\d{1,2}[/.\-]\d{1,2}[/.\-]\d{4}\b',
    ),
    # Horário Geral: Captura horas e minutos (HH:MM), tornando os segundos
    #  (:SS) opcionais no final.
    "horario": re.compile(
        r'\b\d{1,2}:\d{2}(?::\d{2})?\b',
    ),
    # Datetime Geral: Combina os padrões de data e horário separados por
    # um ou mais espaços em branco.
    "datetime": re.compile(
        r'\b\d{1,2}[/.\-]\d{1,2}[/.\-]\d{4}\s+\d{1,2}:\d{2}(?::\d{2})?\b',
    ),
    # URL Geral: Captura links iniciados por protocolo/www ou domínios 
    # diretos (ex: google.com) até achar um espaço.
    "url": re.compile(
        r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}[^\s<>"]*',
        re.IGNORECASE,
    ),
    # Valor Monetário Geral: Captura números com formato de preço, com ou
    #  sem símbolos de moeda (R$, U$, $).
    "valor_monetario": re.compile(
        r'(?:R\$|U\$|\$)?\s?\d+[\d.,]*\b',
    ),
    # Nome Próprio Geral: Captura sequências de palavras iniciadas por 
    # maiúsculas, aceitando nomes únicos ou com conectores (de, da).
    "nome_proprio": re.compile(r'\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-zA-ZáàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇde\. ]{2,}\b'
    ),
}

VALIDACAO = {
    # Proíbe pontos consecutivos (..), pontos nas extremidades e garante a estrutura do domínio.
    "email": re.compile(
        r'^[a-zA-Z0-9_%+\-]+(?:\.[a-zA-Z0-9_%+\-]+)*'
        r'@[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,}$',
    ),
    #  DDD opcional, obriga o dígito 9 para celulares 
    # (9XXXXXXXX) ou aceita fixos (XXXX-XXXX).
    "telefone": re.compile(
        r'^\(?\d{2}\)?[\s\-]?(?:9\d{4}|\d{4})[\s\-]?\d{4}$',
    ),
    # Valida a estrutura dos 11 dígitos, aceitando o formato
    #  puramente numérico ou com pontos e hífen.
    "cpf": re.compile(
        r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    ),
    # Valida o calendário limitando dias de 01 a 31 e meses
    #  de 01 a 12 (formato DD/MM/AAAA).   
    "data": re.compile(
        r'^(0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/\d{4}$',
    ),
    #Valida o relógio limitando horas de 00 a 23 e 
    # minutos/segundos de 00 a 59.
    "horario": re.compile(
        r'^([01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$',
    ),
    # Combina as validações lógicas de calendário e de
    #  relógio em uma única string isolada.
    "datetime": re.compile(
        r'^(0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/\d{4}'
        r'\s+([01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$',
    ),
    # URL Rígida: Exige obrigatoriamente o protocolo http ou https por segurança, validando 
    # a estrutura exata de subdomínios, domínio principal, portas opcionais e parâmetros
    #  de busca.
    "url": re.compile(
        r'^(?:https?://)?'
        r'(?:www\.)?'
        r'[a-zA-Z0-9\-]{1,63}'
        r'(?:\.[a-zA-Z0-9\-]{1,63})*'
        r'\.[a-zA-Z]{2,6}'
        r'(?::\d{2,5})?'
        r'(?:[/?#][^\s]*)?$',
        re.IGNORECASE,
    ),
    # Valor Monetário Rígido: Obriga o R$, valida a separação de milhar
    #  por pontos e torna os centavos opcionais.
    "valor_monetario": re.compile(
        r'^R\$\s?\d{1,3}(?:\.\d{3})*(?:,\d{2})?$',
    ),
    # Exige maiúsculas em cada nome, limita o tamanho das palavras e 
    # aceita conectores legítimos (de, da, do, dos, e).
    "nome_proprio": re.compile(
        r'^[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{1,20}'
        r'(?:\s[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]{1,20}){1,4}$',
    ),
}

# Palavras que não são nomes próprios mesmo iniciando com maiúscula
NOMES_BLACKLIST = {
    "Urgente", "Erro", "Info", "Debug", "Aviso", "Arquivo", "Sistema",
    "Email", "Cliente", "Suporte", "Session", "Service", "Payload",
    "Json", "Csv", "True", "False", "None", "Error", "Warn",
}
