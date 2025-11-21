# 🔴 PokéLang - Documentação Oficial

**Disciplina:** Paradigmas de Linguagens de Programação
**Projeto:** Criação de Linguagem Esotérica
**Extensão de Arquivo:** `.poke`
**Linguagem Alvo:** Python 3

---

## 1. Introdução

A **PokéLang** é uma linguagem de programação esotérica de propósito geral, temática no universo da franquia Pokémon. O objetivo da linguagem é transformar a lógica de programação árida em uma narrativa de batalha ou em letras de música.

O código fonte é escrito em arquivos com extensão `.poke`, que são processados por um tradutor (transpilador) desenvolvido em Python, gerando código executável nativo

---

## 2. Estrutura do Programa

Todo programa em PokéLang simula um encontro com um Pokémon selvagem. O código deve estar contido dentro deste bloco de abertura e fechamento:

```text
Um pokémon selvagem apareceu
    ... (Seu código aqui) ...
O pokémon selvagem desmaiou
````

-----

## 3. Guia de Sintaxe e Comandos

### 3.1. Saída de Dados (Print)

Para exibir informações na tela, o Pokémon utiliza o comando de "cantar".

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

Para ler dados do usuário, utiliza-se a habilidade "detectar".

  * **Sintaxe:** `(Variavel) Use detectar`
  * **Exemplo:** `(Escolha) Use detectar`

### 3.4. Estruturas de Controle (Condicionais)

O fluxo é controlado como uma escolha de movimentos em um turno de batalha.

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
Uma estrutura poética exclusiva para iterar contadores decrescentes (inspirado na música "99 Bottles of Beer").

  * **Sintaxe:**

<!-- end list -->

```text
🎵 [Valor Inicial] ([Variavel]) na Mochila
    ([Variavel]) na mochila... (Imprime valor atual)
    Ash pega uma ([Variavel])... (Decrementa 1 e imprime a ação)
```

### 3.6. Funções (Evolução)

Funções são declaradas como evoluções e chamadas como habilidades.

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

## 4. Implementação Técnica (O Tradutor) 

O tradutor da PokéLang foi desenvolvido em **Python**. Ele funciona como um **Transpilador (Source-to-Source Compiler)**.

### Arquitetura

O sistema é composto por dois arquivos principais:

1.  **`pokelang.py` (O Motor):** Contém um dicionário de regras baseadas em **Expressões Regulares (Regex)**. Ele lê o arquivo `.poke` linha por linha, identifica padrões (como `Use cantar`) e substitui pela sintaxe Python correspondente (`print()`). Ele também gerencia a indentação automática para blocos de código.
2.  **`pokego.py` (O Executor):** É o script principal. Utiliza a biblioteca nativa `sys` para ler o arquivo de entrada e `subprocess` para executar o código Python traduzido automaticamente, garantindo uma experiência fluida para o usuário.

-----

## 5. Códigos Exemplo 

Abaixo estão os três programas obrigatórios escritos em PokéLang.

### 5.1. Hello World (`ola_mundo.poke`) 

```text
Um pokémon selvagem apareceu
(Pikachu) Use cantar "Hello World! Pika Pika!"
O pokémon selvagem desmaiou
```

### 5.2. 99 Garrafas (`99-garrafas.poke`) 

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

### 5.3. Programa Livre: Quiz Interativo (`quiz.poke`) 

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

## 6. Como Executar 

Para rodar os programas, é necessário ter o Python 3 instalado.

1.  Coloque os arquivos `pokego.py`, `pokelang.py` e seu arquivo `.poke` na mesma pasta.
2.  Abra o terminal ou prompt de comando.
3.  Execute o comando abaixo passando o nome do seu arquivo:

<!-- end list -->

```bash
python pokego.py 99-garrafas.poke
```

*(O script irá traduzir o código, executar o programa e limpar os arquivos temporários automaticamente).*
