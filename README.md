# 🔴 PokéLang - Documentação Oficial

**Disciplina:** Paradigmas de Linguagens de Programação
[cite_start]**Projeto:** Criação de Linguagem Esotérica [cite: 5]
[cite_start]**Extensão de Arquivo:** `.poke` [cite: 8]
[cite_start]**Linguagem Alvo:** Python 3 [cite: 8]

---

## 1. Introdução

[cite_start]A **PokéLang** é uma linguagem de programação esotérica de propósito geral, temática no universo da franquia Pokémon[cite: 5]. O objetivo da linguagem é transformar a lógica de programação árida em uma narrativa de batalha ou em letras de música.

[cite_start]O código fonte é escrito em arquivos com extensão `.poke`, que são processados por um tradutor (transpilador) desenvolvido em Python, gerando código executável nativo[cite: 9, 14].

---

## 2. Estrutura do Programa

Todo programa em PokéLang simula um encontro com um Pokémon selvagem. [cite_start]O código deve estar contido dentro deste bloco de abertura e fechamento[cite: 1, 3]:

```text
Um pokémon selvagem apareceu
    ... (Seu código aqui) ...
O pokémon selvagem desmaiou
````

-----

## [cite\_start]3. Guia de Sintaxe e Comandos [cite: 6]

### 3.1. Saída de Dados (Print)

[cite\_start]Para exibir informações na tela, o Pokémon utiliza o comando de "cantar"[cite: 1, 3].

  * **Sintaxe:** `(NomeDoPokemon) Use cantar "Texto"`
  * **Exemplo:**

<!-- end list -->

```text
(Pikachu) Use cantar "Olá Mundo!"
```

### 3.2. Declaração de Variáveis

Variáveis são tratadas como atributos do Pokémon (Vida) ou características.

  * **Atribuição Numérica:**

      * **Sintaxe:** `(Variavel) tem [Valor] de vida`
      * **Exemplo:** `(HP) tem 100 de vida` (Equivale a `hp = 100`)

  * **Atribuição de Texto/Genérica:**

      * **Sintaxe:** `(Variavel) tem [Expressão] de vida`
      * **Exemplo:** `(Nome) tem "Ash Ketchum" de vida`

### 3.3. Entrada de Dados (Input)

[cite\_start]Para ler dados do usuário, utiliza-se a habilidade "detectar"[cite: 2].

  * **Sintaxe:** `(Variavel) Use detectar`
  * **Exemplo:** `(Escolha) Use detectar`

### 3.4. Estruturas de Controle (Condicionais)

[cite\_start]O fluxo é controlado como uma escolha de movimentos em um turno de batalha[cite: 1].

  * **Sintaxe (IF):**

<!-- end list -->

```text
(Variavel) Escolha o movimento se (Condição)
    ... código ...
(Variavel) Fim da escolha
```

  * **Exemplo:**

<!-- end list -->

```text
(Escolha) Escolha o movimento se (Escolha == "1")
    (Narrador) Use cantar "Você escolheu Fogo!"
(Escolha) Fim da escolha
```

### 3.5. Estruturas de Repetição (Loops)

**A. Loop Padrão (While):**
Simula o uso de um item de batalha ("Faixa").

```text
(Contador) Equipou Faixa da escolha enquanto (Contador > 0)
    ... código ...
(Contador) Fim da faixa
```

**B. Modo Música (Loop Decrescente Especial):**
[cite\_start]Uma estrutura poética exclusiva para iterar contadores decrescentes (inspirado na música "99 Bottles of Beer")[cite: 40].

  * **Sintaxe:**

<!-- end list -->

```text
🎵 [Valor Inicial] ([Variavel]) na Mochila
    ([Variavel]) na mochila... (Imprime valor atual)
    Ash pega uma ([Variavel])... (Decrementa 1 e imprime a ação)
```

### 3.6. Funções (Evolução)

[cite\_start]Funções são declaradas como evoluções e chamadas como habilidades[cite: 1].

  * **Declaração:**

<!-- end list -->

```text
[Pokemon] está evoluindo para [NomeDaFuncao]
    ... código da função ...
[Pokemon] parou de evoluir
```

  * **Chamada:**

<!-- end list -->

```text
[Pokemon] use a habilidade [NomeDaFuncao]!
```

-----

## [cite\_start]4. Implementação Técnica (O Tradutor) [cite: 13]

O tradutor da PokéLang foi desenvolvido em **Python**. [cite\_start]Ele funciona como um **Transpilador (Source-to-Source Compiler)**[cite: 9].

### Arquitetura

O sistema é composto por dois arquivos principais:

1.  **`pokelang.py` (O Motor):** Contém um dicionário de regras baseadas em **Expressões Regulares (Regex)**. Ele lê o arquivo `.poke` linha por linha, identifica padrões (como `Use cantar`) e substitui pela sintaxe Python correspondente (`print()`). Ele também gerencia a indentação automática para blocos de código.
2.  **`pokego.py` (O Executor):** É o script principal. [cite\_start]Utiliza a biblioteca nativa `sys` para ler o arquivo de entrada e `subprocess` para executar o código Python traduzido automaticamente, garantindo uma experiência fluida para o usuário[cite: 21].

-----

## [cite\_start]5. Códigos Exemplo [cite: 15]

Abaixo estão os três programas obrigatórios escritos em PokéLang.

### 5.1. [cite\_start]Hello World (`ola_mundo.poke`) [cite: 16, 3]

```text
Um pokémon selvagem apareceu
(Pikachu) Use cantar "Hello World! Pika Pika!"
O pokémon selvagem desmaiou
```

### 5.2. [cite\_start]99 Garrafas (`99-garrafas.poke`) [cite: 17, 40]

Demonstra o "Modo Música" (Loop especializado).

```text
Um pokémon selvagem apareceu

🎵 99 (Garrafas) na Mochila
    (Garrafas) na mochila,
    (Garrafas) pra beber!
    Ash pega uma (Garrafas), passa pra trás!
    (Garrafas) garrafas pra beber!
    (Pausa) Use cantar "---"

Nenhuma (Garrafas) na mochila, hora de ir pra casa...
O pokémon selvagem desmaiou
```

### 5.3. [cite\_start]Programa Livre: Quiz Interativo (`quiz.poke`) [cite: 20, 1]

Demonstra uso de Input, Condicionais, Variáveis e Funções.

```text
Um pokémon selvagem apareceu

# Definindo uma função
Professor está evoluindo para Boas Vindas
    (Prof) Use cantar "Bem-vindo ao mundo Pokémon!"
Professor parou de evoluir

# Programa Principal
Professor use a habilidade Boas Vindas!

(Prof) Use cantar "Qual é o seu nome?"
(Nome) Use detectar

(Prof) Use cantar "Olá " + (Nome)
(Prof) Use cantar "Escolha: (1) Charmander ou (2) Squirtle"
(Escolha) Use detectar

(Escolha) Escolha o movimento se (Escolha == "1")
    (Prof) Use cantar "Você escolheu Fogo! 🔥"
(Escolha) Fim da escolha

(Escolha) Escolha o movimento se (Escolha == "2")
    (Prof) Use cantar "Você escolheu Água! 💧"
(Escolha) Fim da escolha

O pokémon selvagem desmaiou
```

-----

## [cite\_start]6. Como Executar [cite: 21]

Para rodar os programas, é necessário ter o Python 3 instalado.

1.  Coloque os arquivos `pokego.py`, `pokelang.py` e seu arquivo `.poke` na mesma pasta.
2.  Abra o terminal ou prompt de comando.
3.  Execute o comando abaixo passando o nome do seu arquivo:

<!-- end list -->

```bash
python pokego.py 99-garrafas.poke
```

*(O script irá traduzir o código, executar o programa e limpar os arquivos temporários automaticamente).*

```
