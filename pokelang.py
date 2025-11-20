# -*- coding: utf-8 -*-
import re  # Biblioteca de Expressões Regulares (O cérebro do tradutor)

# Dicionário de Regras
# Mapeia o padrão PokéLang (Regex) para Código Python
REGRAS = {
    # Início e Fim
    r"Um pokémon selvagem apareceu": "# Início\nimport sys\n",
    r"O pokémon selvagem desmaiou": "\n# Fim",

    # Funções (Evolução)
    r".*está evoluindo para (.+)": "def {nome_func}():",
    r".*parou de evoluir": "pass",
    r".*use a habilidade (.+)!": "{nome_func}()",

    # Música (Loops)
    r"🎵 (\d+) \((.+)\) na [Mm]ochila": "{var} = {val}\nwhile {var} > 0:",
    r"(.*(pega|tira|lança|joga|assa) uma \((.+)\).*)": "print(\"{frase}\")\n{var} -= 1",
    r"Nenhuma \((.+)\) na mochila.*": "pass # Fim loop\nprint(f\"Nenhuma {{{var}}} na mochila...\")",

    # Letras de música (Regra Genérica)
    r"^\s*\((.+)\) (.+)": "print(f\"{{{var}}} {texto}\")",

    # Comandos Básicos
    r"\((.+)\) Use cantar (.+)": "print({expr})",
    r"\((.+)\) tem (\d+) de vida": "{var} = {val}",
    r"\((.+)\) tem \((.+)\) de vida": "{var} = {expr}",
    r"\((.+)\) Use detectar": "{var} = input()",
    r"\((.+)\) Use Investida (.+)": "{var} = {var} {valor}",

    # Condicionais e Loops
    r"\((.+)\) Equipou Faixa da escolha enquanto \((.+)\)": "while {condicao}:",
    r"\((.+)\) Escolha o movimento se \((.+)\)": "if {condicao}:",
    r".*Fim da (faixa|escolha)": "pass",
    r"^\s*$": "",
}

# Funções Auxiliares para limpar o texto
def processar_expressao(expr):
    # Transforma (Var) em str(var)
    return re.sub(r"\((\w+)\)", lambda m: f"str({m.group(1).lower().replace(' ', '_')})", expr)

def processar_condicao(cond):
    # Transforma (Var) em var e corrige maiúsculas
    cond = re.sub(r"\((\w+)\)", lambda m: m.group(1).lower().replace(' ', '_'), cond)
    def substituir_var_solta(m):
        palavra = m.group(1)
        if palavra in ["True", "False", "None", "Not", "And", "Or"]: return palavra
        return palavra.lower().replace(' ', '_')
    return re.sub(r"\b([A-ZÁ-Ú][a-zA-Z0-9_]*)\b", substituir_var_solta, cond)

def traduzir_linha(linha):
    linha = linha.strip()
    for padrao, traducao in REGRAS.items():
        match = re.match(padrao, linha)
        if match:
            # Lógica de Funções
            if "está evoluindo para" in padrao:
                return traducao.format(nome_func=match.group(1).lower().replace(" ", "_")), 1
            if "parou de evoluir" in padrao: return traducao, -1
            if "use a habilidade" in padrao:
                return traducao.format(nome_func=match.group(1).lower().replace(" ", "_")), 0

            # Lógica de Música
            if "🎵" in padrao:
                val, var = match.group(1), match.group(2).lower().replace(" ", "_")
                return traducao.format(var=var, val=val), 1
            if "uma" in padrao and ("pega" in padrao or "lança" in padrao):
                frase, var = match.group(1), match.group(3).lower().replace(" ", "_")
                return traducao.format(var=var, frase=frase), 0
            if "Nenhuma" in padrao:
                return traducao.format(var=match.group(1).lower().replace(" ", "_")), -1

            # Evita confundir comandos com letras de música
            if padrao.startswith(r"^\s*\((.+)\) (.+)"):
                if "Use cantar" in linha: continue
                if "Escolha o movimento" in linha: continue
                if "Equipou Faixa" in linha: continue
                if "Use detectar" in linha: continue

                var, texto = match.group(1).lower().replace(" ", "_"), match.group(2)
                return traducao.format(var=var, texto=texto), 0

            # Comandos Padrão
            if "Use cantar" in padrao:
                return traducao.format(expr=processar_expressao(match.group(2))), 0
            if "Equipou Faixa" in padrao or "Escolha o movimento" in padrao:
                cond = match.group(2) if match.lastindex >= 2 else "True"
                return traducao.format(condicao=processar_condicao(f"({cond})")), 1
            if "Fim da" in padrao: return "pass", -1
            if "tem" in padrao and "de vida" in padrao:
                var = match.group(1).lower().replace(" ", "_")
                arg = match.group(2)
                val = arg if arg.isdigit() else processar_condicao(f"({arg})")
                return traducao.format(var=var, val=val, expr=val), 0
            if "Use detectar" in padrao:
                return traducao.format(var=match.group(1).lower().replace(" ", "_")), 0
            if "Use Investida" in padrao:
                var = match.group(1).lower().replace(" ", "_")
                return traducao.format(var=var, valor=match.group(2).replace(" ", "")), 0
            return traducao, 0

    if linha and not linha.startswith("#"): return f"# ERRO: {linha}", 0
    return "", 0

def converter_arquivo(arquivo_entrada):
    arquivo_saida = arquivo_entrada.rsplit('.', 1)[0] + ".py"
    linhas_py = []
    indent = 0
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            for linha in f:
                codigo, mudanca = traduzir_linha(linha)
                if mudanca < 0: indent += mudanca
                if indent < 0: indent = 0
                if codigo:
                    espacos = "    " * indent
                    linhas_py.append(espacos + codigo.replace("\n", "\n" + espacos))
                if mudanca > 0: indent += mudanca
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("\n".join(linhas_py))
        return arquivo_saida
    except Exception as e:
        print(f"ERRO: {e}")
        return None
