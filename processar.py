# -*- coding: utf-8 -*-
import re

def processar_expressao_cantar(expr_poke):
    """
    Traduz uma expressão de 'cantar' para Python.
    Ex: "Olá " + (Apelido) -> "Olá " + str(apelido)
    """
    def substituicao(match):
        nome_var = match.group(1).lower().replace(" ", "_")
        return f"str({nome_var})"

    expr_py = re.sub(r"\((\w+)\)", substituicao, expr_poke)
    return expr_py

def processar_condicao(cond_poke):
    """
    Traduz uma expressão de condição (if/while) para Python.
    Ex: (Contador > 0) -> contador > 0
    Ex: (Contador == 1) -> contador == 1
    """
    def substituicao(match):
        # Apenas converte (NomeVariavel) para nomevariavel
        nome_var = match.group(1).lower().replace(" ", "_")
        return nome_var

    # Encontra (Variavel) e troca por variavel
    expr_py = re.sub(r"\((\w+)\)", substituicao, cond_poke)
    return expr_py