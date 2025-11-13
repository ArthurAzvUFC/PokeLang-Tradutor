# -*- coding: utf-8 -*-
import re

# --- Dicionário de Traduções (RegEx) ---
REGRAS_TRADUCAO = {
    # Início/Fim
    r"Um pokémon selvagem apareceu": "# Início do programa PokéLang\nimport sys\n",
    r"O pokémon selvagem desmaiou": "\n# Fim do programa PokéLang",

    # Print / Saída
    r"\((.+)\) Use cantar (.+)": "print({expr})",

    # Variável numérica
    r"\((.+)\) tem (\d+) de vida": "{var} = {val}",
    r"\((.+)\) tem \((.+)\) de vida": "{var} = {expr}",

    # Variável de texto (caso fixo para 'apelido')
    r"O apelido do seu pokémon é \"(.+)\"": "apelido = \"{val}\"",

    # Input
    r"\((.+)\) Use detectar": "{var} = input()",
    
    # Loop (WHILE)
    r"\((.+)\) Equipou Faixa da escolha enquanto \((.+)\)": "while {condicao}:",
    r"\((.+)\) Fim da faixa": "", # Apenas controla a indentação

    # Condicional (IF)
    r"\((.+)\) Escolha o movimento se \((.+)\)": "if {condicao}:",
    r"\((.+)\) Fim da escolha": "", # Apenas controla a indentação

    # Matemática
    # Ex: (Contador) Use Investida -1
    r"\((.+)\) Use Investida (.+)": "{var} = {var} {valor}",

    # Linha em branco
    r"^\s*$": "",
}