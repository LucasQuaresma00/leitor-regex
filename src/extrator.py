"""
extrator.py — Extração de padrões e classificação válido/inválido.

Para cada tipo de padrão:
  1. Aplica a regex de extração ampla ao texto do arquivo
  2. Valida cada ocorrência com a regex rigorosa
  3. Retorna lista de ocorrências com campos prontos para o frontend
"""

from src.padroes import EXTRACAO, VALIDACAO, NOMES_BLACKLIST


def extrair(arquivo: dict) -> list[dict]:
    """Extrai e classifica todas as ocorrências do arquivo."""
    texto = "\n".join(arquivo["linhas"])
    ocorrencias = []

    for tipo, regex in EXTRACAO.items():
        for match in regex.finditer(texto):
            valor = match.group(0).strip()

            if tipo == "nome_proprio" and not _nome_valido(valor):
                continue

            classificacao = _classificar(tipo, valor)

            ocorrencias.append({
                "tipo":              tipo,
                "valor":             valor,
                "valor_normalizado": valor,   # campo esperado pelo frontend
                "arquivo":           arquivo["nome"],
                "classificacao":     classificacao,
                "status_final":      classificacao,  # campo esperado pelo frontend
                "confianca":         1.0 if classificacao == "valido" else 0.0,
            })

    return ocorrencias


def _classificar(tipo: str, valor: str) -> str:
    """Aplica a regex de validação rigorosa e retorna 'valido' ou 'invalido'."""
    regex_val = VALIDACAO.get(tipo)
    if not regex_val:
        return "nao_aplicavel"
    return "valido" if regex_val.fullmatch(valor) else "invalido"


def _nome_valido(valor: str) -> bool:
    """
    Filtra falsos positivos em nomes próprios.
    Critério: 2-5 palavras, sem blacklist, sem siglas.
    """
    tokens = valor.split()
    if not (2 <= len(tokens) <= 5):
        return False
    for t in tokens:
        if t in NOMES_BLACKLIST:
            return False
        if t.isupper() and len(t) > 1:
            return False
    return True
