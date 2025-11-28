# Projeto-ASA-25-26

# ASA 2025/2026 – Projeto 1

Este repositório contém uma solução para o 1.º projeto de **Análise e Síntese de Algoritmos** (ASA) 2025/2026 do IST, sobre maximização da energia libertada ao remover aminoácidos de uma cadeia. [attached_file:file:1]

## Descrição informal do problema

Dada uma cadeia de \(n\) aminoácidos \(a_1, \dots, a_n\), cada aminoácido \(a_i\) tem:
- Um potencial \(P_i > 0\).
- Uma classe bioquímica \(C(i) \in \{P, N, A, B\}\). [attached_file:file:1]

As posições 0 e \(n+1\) são “terminais” com potencial 1 e classe especial \(T\), tal que a afinidade com qualquer classe é 1. [attached_file:file:1]

Quando se remove um aminoácido \(a_i\), a energia libertada é:
\[
E_{\text{libertada}} =
P_{i-1} \cdot Af(C(i-1), C(i)) \cdot P_i
+ P_i \cdot Af(C(i), C(i+1)) \cdot P_{i+1}
\]
onde \(Af\) é a afinidade entre classes, dada por uma tabela não simétrica. [attached_file:file:1]

O objetivo é determinar a ordem de remoção de todos os aminoácidos que **maximiza o somatório da energia total libertada**; em caso de empate, escolhe‑se a sequência lexicograficamente menor. [attached_file:file:1]

## Formato de input

O programa lê de `stdin`:

1. Uma linha com um inteiro \(n \ge 1\).
2. Uma linha com \(n\) inteiros \(P_1, \dots, P_n\) (potenciais).
3. Uma linha com uma string de \(n\) caracteres com as classes \(C(1), \dots, C(n)\), cada uma em `{P, N, A, B}`. [attached_file:file:1]

## Formato de output

O programa escreve em `stdout`:

1. Uma linha com o valor da energia total libertada máxima.
2. Uma linha com a ordem de remoção (permutação de `1..n`, separada por espaços) que atinge esse valor; em caso de múltiplas ordens ótimas, imprime‑se a lexicograficamente menor. [attached_file:file:1]

## Implementação

- Linguagem recomendada: **C++** (aceitam‑se também Java/Python, mas são desaconselhados). [attached_file:file:1]
- O programa deve ser iterativo (soluções recursivas podem rebentar a pilha em testes grandes). [attached_file:file:1]
- O executável deve:
  - Ler **apenas** de `stdin`.
  - Escrever **apenas** para `stdout`. [attached_file:file:1]

Comandos de compilação sugeridos:

- C++: `g++ -std=c++11 -O3 -Wall file.cpp -lm`
- C: `gcc -O3 -ansi -Wall file.c -lm`
- Java: `javac File.java` e `java -Xss32m -Xmx256m -classpath . File`
- Python: `python3 file.py`
- Rust: `rustc -C opt-level=3 --edition=2021 file.rs` [attached_file:file:1]

## Submissão

- **Código fonte**: submetido no **Mooshak**, seguindo a linguagem escolhida (extensão do ficheiro identifica a linguagem). [attached_file:file:1]
- **Relatório**: submetido no **Fénix**, em PDF, máx. 2 páginas, fonte 12pt, margens 3 cm, contendo:
  - Descrição da solução.
  - Análise teórica.
  - Avaliação experimental.
  - Referências usadas. [attached_file:file:1]

Apenas a **última submissão** (código + relatório) é considerada para avaliação. [attached_file:file:1]

## Avaliação

- Avaliação automática no Mooshak:
  - 85% da nota, usando testes ocultos com limites de tempo e memória.
  - Comparação de outputs via `diff output result`. [attached_file:file:1]
- Relatório:
  - 15% da nota final. [attached_file:file:1]

Código que não compila, não respeita o formato de I/O, ou usa estratégias “hard‑coded” para inputs concretos pode receber nota 0 ou sofrer cortes. [attached_file:file:1]

## Detecção de cópias

Qualquer forma de plágio ou submissão de código não desenvolvido pelo(s) aluno(s) implica reprovação na UC e comunicação às entidades competentes do IST, com penalizações de acordo com o regulamento da Universidade. [attached_file:file:1]
