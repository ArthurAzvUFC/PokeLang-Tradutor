import re



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



    # Letras de música (Regra Genérica) - MOVIDA PARA O FINAL

    r"^\s*\((.+)\) (.+)": "print(f\"{{{var}}} {texto}\")",

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



            # Comandos Padrão - ANTES da regra genérica

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



            # Regra genérica de música (só agora, depois de todos comandos)

            if padrao.startswith(r"^\s*\((.+)\) (.+)"):

                var, texto = match.group(1).lower().replace(" ", "_"), match.group(2)

                return traducao.format(var=var, texto=texto), 0



            return traducao, 0



    if linha and not linha.startswith("#"): return f"# ERRO: {linha}", 0

    return "", 0



def converter_arquivo(arquivo_entrada):

    arquivo_saida = arquivo_entrada.rsplit('.', 1)[0] + ".py"

    linhas_py = []

    indent = 0

    lendo = False  # só traduz entre as frases-chave

    try:

        with open(arquivo_entrada, 'r', encoding='utf-8') as f:

            for linha in f:

                linha_limpa = linha.strip()



                # → Ativa leitura

                if re.match(r"Um pokémon selvagem apareceu", linha_limpa, re.IGNORECASE):

                    lendo = True

                    codigo, mudanca = traduzir_linha(linha_limpa)

                # → Desativa leitura e para

                elif re.match(r"O pokémon selvagem desmaiou", linha_limpa, re.IGNORECASE):

                    codigo, mudanca = traduzir_linha(linha_limpa)

                    if codigo:

                        espacos = "    " * indent

                        linhas_py.append(espacos + codigo)

                    break  # encerra totalmente

                else:

                    # Se ainda não encontrou o início → ignora completamente

                    if not lendo:

                        continue

                    # Se já passou do fim → ignora também

                    # (não ocorre pois damos break, mas mantenho por segurança)

                    codigo, mudanca = traduzir_linha(linha_limpa)



                # Controle de indentação

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
