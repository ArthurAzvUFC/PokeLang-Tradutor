# -*- coding: utf-8 -*-
import sys
from traduzir import traduzir_linha

def main(caminho_arquivo_poke):
    """
    Lê um arquivo .poke e gera um .py equivalente,
    controlando o nível de indentação.
    """
    caminho_arquivo_py = caminho_arquivo_poke.rsplit('.', 1)[0] + ".py"
    
    linhas_traduzidas = []
    nivel_indentacao = 0
    espaco_indent = "    " # 4 espaços

    try:
        with open(caminho_arquivo_poke, 'r', encoding='utf-8') as f_poke:
            for i, linha_poke in enumerate(f_poke):
                
                # O tradutor retorna o texto E a mudança de indentação
                linha_traduzida, mudanca_indent = traduzir_linha(linha_poke)
                
                # Se a mudança for -1 (Fim de Bloco),
                # diminuímos a indentação ANTES de adicionar a linha
                if mudanca_indent < 0:
                    nivel_indentacao += mudanca_indent
                
                # Garante que não teremos indentação negativa
                if nivel_indentacao < 0:
                    print(f"Erro de indentação na linha {i+1}: {linha_poke.strip()}")
                    nivel_indentacao = 0

                # Adiciona os espaços de indentação
                indentacao_atual = espaco_indent * nivel_indentacao
                
                if linha_traduzida:
                    linhas_traduzidas.append(indentacao_atual + linha_traduzida)
                
                # Se a mudança for +1 (Início de Bloco),
                # aumentamos a indentação DEPOIS de adicionar a linha
                if mudanca_indent > 0:
                    nivel_indentacao += mudanca_indent

        with open(caminho_arquivo_py, 'w', encoding='utf-8') as f_py:
            f_py.write("\n".join(linhas_traduzidas))
        
        print(f"✅ Tradução concluída: {caminho_arquivo_py}")
        print(f"Para executar, use: python {caminho_arquivo_py}")

    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo_poke}' não encontrado.")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo.poke>")
        sys.exit(1)

    arquivo = sys.argv[1]
    if not arquivo.endswith(".poke"):
        print("Erro: o arquivo deve ter extensão .poke")
        sys.exit(1)

    main(arquivo)