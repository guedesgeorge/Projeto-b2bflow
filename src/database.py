"""Acesso ao banco de dados no Supabase via API REST (PostgREST).

Em vez da biblioteca supabase-py, falamos direto com a API REST do
Supabase usando requests. Isso evita incompatibilidades da lib com o
formato novo de chave (sb_publishable_...) e deixa explícito o que é
enviado em cada requisição.
"""

import logging
from typing import List

import requests

from src import config

logger = logging.getLogger(__name__)

# Timeout (em segundos) para a requisição HTTP
_TIMEOUT = 30


def buscar_contatos(limite: int = config.LIMITE_CONTATOS) -> List[dict]:
    """Busca os contatos cadastrados no Supabase pela API REST.

    Retorna uma lista de dicionários no formato:
        {"nome_contato": "...", "telefone": "..."}

    Aplica o limite definido pelo desafio (até 3 contatos).
    """
    url = f"{config.SUPABASE_URL}/rest/v1/{config.SUPABASE_TABELA}"
    params = {"select": "nome_contato,telefone", "limit": limite}
    # A API exige a chave no header 'apikey' e tambem no 'Authorization'.
    headers = {
        "apikey": config.SUPABASE_KEY,
        "Authorization": f"Bearer {config.SUPABASE_KEY}",
        "Accept": "application/json",
    }

    logger.info("Buscando ate %d contato(s) na tabela '%s'...", limite, config.SUPABASE_TABELA)

    try:
        resposta = requests.get(url, params=params, headers=headers, timeout=_TIMEOUT)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as erro:
        corpo = getattr(erro.response, "text", "") if getattr(erro, "response", None) else ""
        logger.error("Falha ao consultar o Supabase: %s %s", erro, corpo)
        raise

    contatos = resposta.json() or []
    logger.info("%d contato(s) encontrado(s).", len(contatos))
    return contatos