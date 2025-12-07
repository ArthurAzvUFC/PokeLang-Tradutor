# -*- coding: utf-8 -*-
import re

# --- CÓDIGO INJETADO (Runtime Cinnabar Engine) ---
# Este bloco é inserido no topo de todo programa traduzido
CABECALHO = r'''# Início PokéLang
import sys
import time
import random
import builtins

# Configuração de áudio (Seguro para Mac/Linux)
SOM_ATIVO = False
try:
    import winsound
    SOM_ATIVO = True
except ImportError:
    pass

# Cores ANSI (Nativo do terminal)
ROXO = "\033[95m"
VERMELHO = "\033[91m"
VERDE = "\033[92m"
CINZA = "\033[90m"
RESET = "\033[0m"

# --- EFEITOS VISUAIS ---

def type_effect(texto, delay=0.015):
    # Efeito máquina de escrever
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("")

def glitch_text(texto):
    # Insere artefatos visuais aleatórios (MissingNo effect)
    if random.random() > 0.3: return texto
    chars = ['#', '?', '%', '§', '¿', '▓', '▒']
    lista = list(texto)
    for _ in range(random.randint(1, 3)):
        if lista:
            pos = random.randint(0, len(lista))
            lista.insert(pos, random.choice(chars))
    return "".join(lista)

def error_beep():
    if SOM_ATIVO:
        try: winsound.Beep(1500, 500)
        except: pass
    else:
        sys.stdout.write('\a')

# --- FUNÇÕES CORE ---

def void_echo(*args):
    # Print customizado
    texto = " ".join(map(str, args))
    texto_bugado = glitch_text(texto)
    prefixo = f"{VERDE}▓▒░{RESET} "
    if texto != texto_bugado: prefixo = f"{VERMELHO}⚠ {RESET}"
    sys.stdout.write(prefixo)
    type_effect(texto_bugado)

def void_input(prompt=""):
    # Input customizado
    if prompt: void_echo(prompt)
    return builtins.input(f"{ROXO}0x??? >> {RESET}")

def safe_float(valor):
    # Wrapper seguro para conversão numérica
    try:
        return float(valor)
    except:
        print(f"{VERMELHO}[ERR] Valor '{valor}' inválido. Assumindo 0.0{RESET}")
        return 0.0

# Tratamento de erro global (Bad Egg)
def global_except_hook(exctype, value, traceback):
    if exctype == KeyboardInterrupt: return
    print(f"\n{VERMELHO}>> FATAL ERROR: BAD EGG DETECTED <<{RESET}")
    print(f"{CINZA}Memory Dump: {value}{RESET}")
    error_beep()

sys.excepthook = global_except_hook
print(f"{ROXO}▒▒ CINNABAR KERNEL LOADED ▒▒{RESET}\n")
'''

# --- AUXILIARES DO TRADUTOR ---

def limpar(nome):
    return nome.lower().replace(' ', '_')

def processar_expr(expr):
    # Substitui float() pelo nosso safe_float()
    expr = re.sub(r"\bfloat\(", "safe_float(", expr)
    # Ajusta nomes de variáveis dentro de parenteses
    expr = re.sub(r"(?<!\w)\((\w+)\)", lambda m: limpar(m.group(1)), expr)

    def var_replacer(m):
        w = m.group(1)
        if w in ["True", "False", "None", "not", "and", "or", "input", "str", "int"]: return w
        return w.lower()

    # Ajusta variáveis soltas (Case sensitive fix)
    return re.sub(r"\b([A-Z][a-zA-Z0-9_]*)\b", var_replacer, expr)

# --- REGRAS DE TRADUÇÃO ---

REGRAS = {
    # 1. Estrutura
    r"Um pokémon selvagem apareceu": CABECALHO,
    r"O pokémon selvagem desmaiou": "\n# Fim\nprint(f'{CINZA}[CONNECTION CLOSED]{RESET}')",

    # 2. Funções
    r".*está evoluindo para\s+(.+)": "def {nome_func}():",
    r".*parou de evoluir": "pass",
    r".*use a habilidade\s+(\w+)!": "{nome_func}()",

    # 3. Loops Musicais
    r"🎵\s+(\d+)\s+\((.+)\)\s+na [Mm]ochila": "{var} = {val}\nwhile {var} > 0:",
    r"(.*(pega|tira|lança|joga|assa) uma \((.+)\).*)": "void_echo(\"{frase}\")\n{var} -= 1",
    r"Nenhuma \((.+)\) na mochila.*": "void_echo(f\"Nenhuma {{{var}}} na mochila...\")",

    # 4. IO e Atribuição
    r"\((.+)\) Use cantar\s+(.+)": "void_echo({expr})",
    r"\((.+)\) Use detectar": "{var} = void_input()",
    r"\((.+)\) tem\s+(.+)\s+de vida": "{var} = {val}",

    # 5. Fluxo
    r"\((.+)\) Equipou Faixa da escolha enquanto\s+\((.+)\)": "while {condicao}:",
    r"\((.+)\) Escolha o movimento se\s+\((.+)\)": "if {condicao}:",
    r".*Fim da (faixa|escolha)": "pass",
    r"^\s*$": "",

    # 6. Genérico (Print)
    r"^\s*\(([^)]+)\)\s+(.+)": "void_echo(f\"{{{var}}} {texto}\")",
}

def traduzir_linha(linha):
    linha = linha.strip()
    for padrao, traducao in REGRAS.items():
        match = re.match(padrao, linha)
        if match:
            # Lógica de indentação baseada no retorno (+1 ou -1)

            # Funções
            if "está evoluindo para" in padrao:
                return traducao.format(nome_func=limpar(match.group(1))), 1
            if "parou de evoluir" in padrao: return traducao, -1
            if "use a habilidade" in padrao:
                return traducao.format(nome_func=limpar(match.group(1))), 0

            # Loop Música
            if "🎵" in padrao:
                val, var = match.group(1), match.group(2)
                return traducao.format(var=limpar(var), val=val), 1
            if "uma" in padrao and ("pega" in padrao or "lança" in padrao):
                frase, var = match.group(1), match.group(3)
                return traducao.format(var=limpar(var), frase=frase), 0
            if "Nenhuma" in padrao:
                return traducao.format(var=limpar(match.group(1))), -1

            # Comandos
            if "Use cantar" in padrao:
                # Processa expressão para garantir str() e vars corretas
                raw_expr = match.group(2)
                # Garante que str((Var)) vire str(var)
                clean_expr = re.sub(r"str\s*\(\s*\(([a-zA-Z0-9_]+)\)\s*\)", r"str(\1)", raw_expr)
                return traducao.format(expr=processar_expr(clean_expr)), 0

            if "Use detectar" in padrao:
                return traducao.format(var=limpar(match.group(1))), 0

            if "tem" in padrao and "de vida" in padrao:
                var = limpar(match.group(1))
                val = processar_expr(match.group(2))
                return traducao.format(var=var, val=val), 0

            if "Equipou Faixa" in padrao or "Escolha o movimento" in padrao:
                cond = match.group(2)
                return traducao.format(condicao=processar_expr(cond)), 1

            if "Fim da" in padrao: return "pass", -1

            # Genérico (Cuidado com conflitos)
            if padrao.startswith(r"^\s*\(([^)]+)\)"):
                if any(x in linha for x in ["Use cantar", "Use detectar", "tem", "Escolha", "Equipou", "Fim"]):
                    continue
                var = limpar(match.group(1))
                texto = match.group(2)
                return traducao.format(var=var, texto=texto), 0

            return traducao, 0

    if linha and not linha.startswith("#"): return f"# ERRO: {linha}", 0
    return "", 0

def converter_arquivo(arquivo_entrada):
    arquivo_saida = arquivo_entrada.rsplit('.', 1)[0] + ".py"
    linhas_py = []
    indent = 0
    lendo = False

    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()

                # Controle de bloco principal
                if re.match(r"Um pokémon selvagem apareceu", linha, re.IGNORECASE):
                    lendo = True
                    codigo, chg = traduzir_linha(linha)
                elif re.match(r"O pokémon selvagem desmaiou", linha, re.IGNORECASE):
                    codigo, chg = traduzir_linha(linha)
                    if codigo: linhas_py.append(("    " * indent) + codigo)
                    break
                else:
                    if not lendo: continue
                    codigo, chg = traduzir_linha(linha)

                # Indentação
                if chg < 0: indent += chg
                if indent < 0: indent = 0

                if codigo:
                    espacos = "    " * indent
                    linhas_py.append(espacos + codigo.replace("\n", "\n" + espacos))

                if chg > 0: indent += chg

        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("\n".join(linhas_py))
        return arquivo_saida
    except Exception as e:
        print(f"Erro no motor: {e}")
        return None
