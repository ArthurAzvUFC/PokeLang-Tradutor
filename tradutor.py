# -*- coding: utf-8 -*-
import sys
import re

# --- Dicionário de Traduções (RegEx) ---
# A chave é o padrão RegEx para encontrar, o valor é como traduzir para Python.
# Usamos grupos de captura (parênteses) para extrair nomes e valores.

REGRAS_TRADUCAO = {
    # Início/Fim
    r"Um pokémon selvagem apareceu": "# Início do programa PokéLang\nimport sys\n",
    r"O pokémon selvagem desmaiou": "\n# Fim do programa PokéLang",

    # Print / Saída
    # Ex: (Pikachu) Use cantar "Olá " + (Apelido)
    r"\((.+)\) Use cantar (.+)": "print({expr})",

    # Declaração de Variável Numérica
    # Ex: (Contador) tem 99 de vida
    r"\((.+)\) tem (\d+) de vida": "{var} = {val}",

    # Declaração de Variável de Texto
    # Ex: O apelido do seu pokémon é "Pika" (Vou assumir que o nome da var é 'apelido')
    # Esta sintaxe é difícil de generalizar.
    # Sugestão: Mudar para algo como (Apelido) é "Pika"
    r"O apelido do seu pokémon é \"(.+)\"": "apelido = \"{val}\"",
    
    # Input / Entrada
    # Ex: (Apelido) Use detectar
    r"\((.+)\) Use detectar": "{var} = input()",

    # TODO: Comandos de Controle (IF, WHILE)
    # Ex: (Contador) Equipou Faixa da escolha enquanto (Contador > 0)
    # r"\((.+)\) Equipou Faixa da escolha enquanto (.+)": "while ({cond}):",
    # r"\((.+)\) Fim da faixa": "    pass # Fim do while",

    # Linha em branco
    r"^\s*$": "",
}

def processar_expressao_cantar(expr_poke):
    """
    Traduz uma expressão de 'cantar' para Python.
    Ex: "Olá " + (Apelido) -> "Olá " + str(apelido)
    """
    # Esta função usa RegEx (re.sub) para encontrar todas as (Variaveis)
    # e substituí-las por str(variavel_em_minusculo)
    def substituicao(match):
        nome_var = match.group(1).lower().replace(" ", "_")
        return f"str({nome_var})"

    # Encontra (Variavel) e aplica a função 'substituicao'
    expr_py = re.sub(r"\((\w+)\)", substituicao, expr_poke)
    return expr_py

def traduzir_linha(linha_poke):
    """
    Tenta traduzir uma única linha de PokéLang para Python.
    """
    linha_poke = linha_poke.strip()

    for padrao, traducao in REGRAS_TRADUCAO.items():
        match = re.match(padrao, linha_poke)
        if match:
            # --- Caso Especial: Comando CANTAR ---
            if "Use cantar" in padrao:
                expr_poke = match.group(2)
                expr_py = processar_expressao_cantar(expr_poke)
                return traducao.format(expr=expr_py)
            
            # --- Caso Especial: Declaração de Variável (Numérica) ---
            if "tem" in padrao and "de vida" in padrao:
                nome_var = match.group(1).lower().replace(" ", "_")
                valor = match.group(2)
                return traducao.format(var=nome_var, val=valor)
            
            # --- Caso Especial: Declaração de Variável (Texto) ---
            if "apelido" in padrao:
                valor = match.group(1)
                return traducao.format(val=valor)
            
            # --- Caso Especial: Input (Detectar) ---
            if "Use detectar" in padrao:
                nome_var = match.group(1).lower().replace(" ", "_")
                return traducao.format(var=nome_var)

            # --- Outros casos (Início, Fim, Linha em branco) ---
            return traducao

    # Se nenhuma regra corresponder, retorna um erro de sintaxe
    if linha_poke and not linha_poke.startswith("#"):
        return f"# ERRO: Sintaxe PokéLang não reconhecida: {linha_poke}"
    return ""


def main(caminho_arquivo_poke):
    """
    Função principal que lê o arquivo .poke e escreve o .py
    """
    try:
        # Define o nome do arquivo de saída (ex: 'programa.poke' -> 'programa.py')
        caminho_arquivo_py = caminho_arquivo_poke.rsplit('.', 1)[0] + ".py"
        
        linhas_traduzidas = []
        with open(caminho_arquivo_poke, 'r', encoding='utf-8') as f_poke:
            for linha in f_poke:
                linha_traduzida = traduzir_linha(linha)
                if linha_traduzida: # Ignora linhas que não geram tradução
                    linhas_traduzidas.append(linha_traduzida)
        
        with open(caminho_arquivo_py, 'w', encoding='utf-8') as f_py:
            f_py.write("\n".join(linhas_traduzidas))
        
        print(f"✅ Tradução concluída com sucesso!")
        print(f"   Arquivo de entrada: {caminho_arquivo_poke}")
        print(f"   Arquivo de saída:   {caminho_arquivo_py}")
        print(f"\nPara executar, use: python {caminho_arquivo_py}")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo_poke}' não encontrado.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu durante a tradução: {e}")

if __name__ == "__main__":
    # Verifica se o usuário passou o nome do arquivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python tradutor.py <arquivo.poke>")
        sys.exit(1)
    
    caminho_arquivo = sys.argv[1]
    if not caminho_arquivo.endswith(".poke"):
        print(f"Erro: O arquivo de entrada '{caminho_arquivo}' deve ter a extensão .poke")
        sys.exit(1)
        
    main(caminho_arquivo)