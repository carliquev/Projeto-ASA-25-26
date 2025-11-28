# Projeto-ASA-25-26

# Projeto — Análise e Síntese de Algoritmos (ASA)  
## Instituto Superior Técnico — 2025/2026

**Data do enunciado:** 15 de Novembro de 2025  
**Data limite de entrega:** 5 de Dezembro de 2025  

---

## 📘 Descrição do Problema

O jogo consiste em remover aminoácidos de uma cadeia `a₁ … aₙ`.  
Cada remoção liberta energia, dependente de:

- potencial do aminoácido: `Pᵢ`
- potencial dos vizinhos: `Pᵢ₋₁` e `Pᵢ₊₁`
- afinidade entre classes bioquímicas  
  - **P** (Polar)  
  - **N** (Não-Polar)  
  - **A** (Ácido)  
  - **B** (Base)

A energia libertada ao remover `aᵢ` é:

```
E = P(i−1) × Af(C(i−1), C(i)) × P(i)
  + P(i)   × Af(C(i), C(i+1)) × P(i+1)
```

### Afinidade Af(c₁, c₂)

| Af | P | N | A | B |
|----|---|---|---|---|
| **P** | 1 | 3 | 1 | 3 |
| **N** | 5 | 1 | 0 | 1 |
| **A** | 0 | 1 | 0 | 4 |
| **B** | 1 | 3 | 2 | 3 |

Extremidades (`0` e `n+1`) têm:

- potencial = **1**
- classe = **T**  
- afinidade neutra: `Af(T,c) = Af(c,T) = 1`

🎯 **Objetivo:** determinar a ordem de remoção dos aminoácidos que maximiza a energia total libertada.  
Se houver mais do que uma ordem ótima, devolver a lexicograficamente menor.

---

## 📥 Input

1. Um inteiro `n ≥ 1`
2. Linha com `n` inteiros (potenciais > 0)
3. Linha com `n` caracteres (classes `P`, `N`, `A`, `B`)

---

## 📤 Output

1. Energia total libertada  
2. Ordem de remoção (índices 1-based) separados por espaços  
   - se houver várias soluções ótimas → devolver a lexicograficamente menor

---

## 🧪 Exemplos

### Exemplo 1

**Input**
```
3
10 5 12
ABA
```

**Output**
```
359
1 2 3
```

---

### Exemplo 2

**Input**
```
9
4 2 7 3 5 1 2 8 3
ANBPAPBNA
```

**Output**
```
607
2 1 4 6 5 7 8 9 3
```

---

## 🛠 Implementação

Programação preferencial: **C++**.  
Java e Python são aceites mas **desaconselhados** (possível timeout).

Evitar soluções recursivas → risco de *stack overflow* em testes grandes.

### Parâmetros de compilação

```
C++: g++ -std=c++11 -O3 -Wall file.cpp -lm
C:   gcc -O3 -ansi -Wall file.c -lm
Javac: javac File.java
Java:  java -Xss32m -Xmx256m -classpath . File
Python: python3 file.py
Rust: rustc -C opt-level=3 --edition=2021 file.rs
```

---

## 📤 Submissão

### ✔ Código fonte — Mooshak  
O código deve:

- compilar sem erros  
- ler de stdin  
- escrever para stdout  

Apenas **a última submissão conta**.

### ✔ Relatório — Fénix  
Formato:

- PDF  
- máx. 2 páginas  
- fonte 12pt  
- margens 3 cm  

Conteúdo:

- descrição da solução  
- análise teórica  
- avaliação experimental  
- referências  

---

## 🧮 Avaliação

- 85% — avaliação automática (Mooshak)  
- 15% — relatório  

Avaliação automática usa:

```
diff output result
```

Nota varia entre 0 e 170.

Código com truques para casos específicos pode ser penalizado.

---

## ⚠ Detecção de Cópias

Plágio implica:

- reprovação imediata  
- comunicação ao Conselho Pedagógico  
- penalizações conforme regras da Universidade  

---

## 📎 Observação Final

Todos os testes serão divulgados **após** o deadline.  
Os estudantes são encorajados a submeter versões preliminares cedo.(s) aluno(s) implica reprovação na UC e comunicação às entidades competentes do IST, com penalizações de acordo com o regulamento da Universidade. [attached_file:file:1]
