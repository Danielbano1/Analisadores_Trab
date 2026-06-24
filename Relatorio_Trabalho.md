# Relatório do Trabalho: Analisador Sintático ObsAct

## 1. O que foi implementado
Foi implementado um transpilador completo da linguagem **ObsAct** para a linguagem **C**. O trabalho foi desenvolvido utilizando a ferramenta PLY (Python Lex-Yacc) para construir os analisadores léxico (`lexer.py`) e sintático (`parser.py`). Os testes foram organizados em múltiplos arquivos dentro da pasta `testes/`. O script `rodar_testes.py` foi criado para rodar todos os exemplos em lote e gerar o código C resultante na pasta `saida_testes/`, testando o fluxo ponta a ponta de forma automatizada.

## 2. Como foi implementado

### Analisador Léxico (`lexer.py`)
- O arquivo de tokens foi expandido para cobrir todas as palavras reservadas do ObsAct: `dispositivo`, `set`, `se`, `entao`, `senao`, `ligar`, `desligar`, `verificar`, `enviar`, `alerta`, `para`, `todos`, além de valores lógicos `True` e `False`.
- Foram adicionadas expressões regulares para todos os operadores lógicos exigidos (`>`, `<`, `>=`, `<=`, `==`, `!=`, `&&`) e símbolos de pontuação (`{`, `}`, `(`, `)`, `:`, `,`, `.`, `=`).
- Tokens de `ID` (letras/números começando com letra), `NUM` (inteiros) e `STRING` (entre aspas) foram corretamente mapeados e seus valores extraídos.

### Analisador Sintático e Transpilador (`parser.py`)
- O parser foi modelado estritamente com base na gramática definida no PDF. A árvore sintática (AST) é montada e, logo em seguida, percorrida para gerar o código equivalente em linguagem C.
- **Estrutura Base em C:** Todo programa gerado automaticamente inclui as bibliotecas `<stdio.h>` e `<string.h>` e declara as 4 funções básicas de dispositivos (`ligar`, `desligar`, `verificar`, e `alerta` sobrecarregada com variáveis inteiras) no topo do arquivo. A função `main` declara e inicializa as variáveis de observação (como `0`, conforme regra 1.4 do PDF) e executa os comandos.

## 3. Alterações na Gramática (Regra 1.5 do PDF)
Para garantir que a linguagem final atenda todos os cenários dos exemplos fornecidos no documento, as seguintes adições e flexibilizações foram feitas na gramática:

1. **Permissão de Ações como Observações (`OBS`)**:
   No PDF, é dado o exemplo `se verificar(umidificador) == 0 entao`. Para suportar isso, foi adicionada uma derivação extra na regra de observação:
   `OBS -> VERIFICAR LPAREN ID RPAREN oplogic VAR`.
2. **Atribuição com Chaves (`ATTRIB`)**:
   No exemplo `set {lampada, potenciaLampada} = 100 .`, a atribuição é feita usando as chaves dos dispositivos. Adicionou-se a regra:
   `ATTRIB -> SET LBRACE ID COMMA ID RBRACE EQUALS VAR`. Na transpilação, o valor `100` é atribuído à variável observada (no caso, `potenciaLampada`).
3. **Broadcasting de Alertas (`ACTALERT`)**:
   A regra foi expandida para suportar o broadcast explícito (ex: `enviar alerta ("msg") para todos: dev1, dev2`).
   Adicionaram-se regras `ENVIAR ALERTA LPAREN STRING RPAREN PARA TODOS COLON id_list`, traduzidas como múltiplas chamadas individuais à função `alerta()` em C.
4. **Terminador Opcional (`.`)**:
   O PDF define que `.` encerra os comandos. Pela falta de delimitadores explícitos de fim de bloco (como `fimse` ou chaves `{ }`), e seguindo as restrições da gramática original ascendente LALR(1), um comando `se` aninhará os comandos subsequentes em seu corpo `entao` de forma sequencial (devido à preferência natural de `Shift` do parser na recursão à direita de `cmds`). O ponto final foi mapeado de forma a suportar a separação dos comandos como exemplificado sem interromper o fluxo léxico.

## 4. O que funciona
- Declaração de dispositivos, com e sem variáveis de observação.
- Inicialização de variáveis observadas como `0` em linguagem C.
- Comandos de atribuição de variáveis lógicas e numéricas.
- Estruturas de decisão complexas (`se ... entao ... senao ...`), incluindo condições compostas com `&&`.
- Comandos de ação (`ligar`, `desligar`, `verificar`) e envio de `alerta` com concatenação.
- Geração completa e válida do arquivo final contendo o código na linguagem de programação C.

## 5. Como Executar (Testes)
Para testar, basta executar no terminal na mesma pasta dos arquivos:
```bash
python3 teste.py
```
Isso compilará o programa de exemplo especificado internamente e fará o print do código fonte em C no terminal (já contendo as importações e funções predefinidas). O usuário pode então copiar o código C, colar em um arquivo (ex: `main.c`) e compilá-lo com GCC (`gcc main.c -o main`) para testar nativamente se desejar.
