# -*- coding: utf-8 -*-
import re
from regras import REGRAS_TRADUCAO
from processar import processar_expressao_cantar, processar_condicao

def traduzir_linha(linha_poke):
    """
    Tenta traduzir uma única linha de PokéLang para Python.
    
    Retorna uma tupla: (linha_traduzida, mudanca_indentacao)
    mudanca_indentacao:
       +1: Inicia um bloco (if, while), indente as próximas linhas
       -1: Termina um bloco (Fim da...), des-indente esta linha
        0: Linha normal
    """
    linha_poke = linha_poke.strip()

    for padrao, traducao in REGRAS_TRADUCAO.items():
        match = re.match(padrao, linha_poke)
        if match:
            
            # --- BLOCOS DE INDENTAÇÃO ---
            
            # WHILE (Início)
            if "Equipou Faixa da escolha" in padrao:
                cond_poke = match.group(2)
                cond_py = processar_condicao(cond_poke)
                return traducao.format(condicao=cond_py), 1 # +1 indent
            
            # IF (Início)
            if "Escolha o movimento" in padrao:
                cond_poke = match.group(2)
                cond_py = processar_condicao(cond_poke)
                return traducao.format(condicao=cond_py), 1 # +1 indent

            # Fim de Bloco (IF/WHILE)
            if "Fim da faixa" in padrao or "Fim da escolha" in padrao:
                # Retorna "pass" para garantir que blocos vazios funcionem
                return "pass", -1 # -1 indent

            # --- COMANDOS NORMAIS ---
            
            if "Use cantar" in padrao:
                expr_poke = match.group(2)
                expr_py = processar_expressao_cantar(expr_poke)
                return traducao.format(expr=expr_py), 0
            
            if "tem" in padrao and "de vida" in padrao:
                nome_var = match.group(1).lower().replace(" ", "_")
                # Regra: (Var) tem 99 de vida
                if traducao == "{var} = {val}": 
                    valor = match.group(2)
                    return traducao.format(var=nome_var, val=valor), 0
                # Regra: (Var) tem (OutraVar) de vida
                if traducao == "{var} = {expr}":
                    expr_poke = match.group(2)
                    # processar_condicao também serve para (Variavel) -> variavel
                    expr_py = processar_condicao(f"({expr_poke})") 
                    return traducao.format(var=nome_var, expr=expr_py), 0

            if "apelido" in padrao:
                valor = match.group(1)
                return traducao.format(val=valor), 0

            if "Use detectar" in padrao:
                nome_var = match.group(1).lower().replace(" ", "_")
                return traducao.format(var=nome_var), 0
            
            # Matemática (Investida)
            if "Use Investida" in padrao:
                nome_var = match.group(1).lower().replace(" ", "_")
                valor = match.group(2).replace(" ", "") # Garante "-1"
                return traducao.format(var=nome_var, valor=valor), 0

            # Regras simples (Início, Fim, Linha Branca)
            return traducao, 0

    if linha_poke and not linha_poke.startswith("#"):
        return f"# ERRO: Sintaxe PokéLang não reconhecida: {linha_poke}", 0
    
    return "", 0 # Linha vazia ou comentário