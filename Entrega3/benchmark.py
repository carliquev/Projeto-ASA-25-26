#!/usr/bin/env python3
"""
Script de Benchmark para o Problema do Campeonato de Futebol
Gera 11 instâncias com tamanhos incrementais, executa 3 vezes cada e cria gráficos.
"""

import subprocess
import time
import random
import numpy as np
import matplotlib.pyplot as plt

def gerar_instancia(n, m_jogos_realizados):
    """
    Gera uma instância de teste com n equipas e m_jogos_realizados jogos já disputados.
    Retorna o input como string.
    """
    total_jogos = n * (n - 1)
    m_jogos_realizados = min(m_jogos_realizados, total_jogos)

    lines = [f"{n} {m_jogos_realizados}"]

    # Gerar lista de todos os jogos possíveis
    jogos_possiveis = []
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                jogos_possiveis.append((i, j))

    # Selecionar m_jogos_realizados aleatórios
    jogos_selecionados = random.sample(jogos_possiveis, m_jogos_realizados)

    for casa, fora in jogos_selecionados:
        # Resultado aleatório: 0 (empate), casa (vitória casa), fora (vitória fora)
        resultado = random.choice([0, casa, fora])
        lines.append(f"{casa} {fora} {resultado}")

    return '\n'.join(lines)

def executar_solver(input_str, solver_path='e3_v2.py'):
    """
    Executa o solver e retorna o tempo de execução.
    """
    start_time = time.time()

    try:
        result = subprocess.run(
            ['python3', solver_path],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=120  # timeout de 120 segundos
        )
        end_time = time.time()

        if result.returncode == 0:
            return end_time - start_time
        else:
            print(f"    Erro: {result.stderr[:100]}")
            return None
    except subprocess.TimeoutExpired:
        print("    Timeout!")
        return None
    except Exception as e:
        print(f"    Exceção: {e}")
        return None

def main():
    # Nome do ficheiro do solver (ajustar conforme necessário)
    SOLVER_FILE = 'e3_v2.py'

    print("=" * 90)
    print(" BENCHMARK - Problema do Campeonato de Futebol")
    print("=" * 90)
    print(f"Solver: {SOLVER_FILE}")
    print(f"Execuções por instância: 3")
    print("=" * 90)

    # Definir as 11 instâncias com tamanhos incrementais
    instancias = [
        (3, 2),
        (4, 4),
        (5, 8),
        (6, 12),
        (7, 18),
        (8, 24),
        (9, 32),
        (10, 40),
        (11, 50),
        (12, 60),
        (13, 72),
    ]

    resultados = []

    print("\nExecutando instâncias...")
    print("-" * 90)

    for idx, (n, m_realizados) in enumerate(instancias, 1):
        total_jogos = n * (n - 1)
        m_restantes = total_jogos - m_realizados
        complexidade = n * (m_restantes + n)

        print(f"\nInstância {idx:2d}: n={n:2d}, m_realiz={m_realizados:2d}, "
              f"m_restantes={m_restantes:2d}, n*(m_rest+n)={complexidade:4d}")

        tempos = []

        for run in range(1, 4):
            print(f"  Run {run}/3...", end=' ', flush=True)

            # Gerar nova instância aleatória
            input_data = gerar_instancia(n, m_realizados)
            tempo = executar_solver(input_data, SOLVER_FILE)

            if tempo is not None:
                tempos.append(tempo)
                print(f"✓ {tempo:.3f}s")
            else:
                print("✗ Falhou")

        if tempos:
            tempo_medio = np.mean(tempos)
            tempo_std = np.std(tempos)

            resultados.append({
                'n': n,
                'm_realizados': m_realizados,
                'm_restantes': m_restantes,
                'complexidade': complexidade,
                'tempo_medio': tempo_medio,
                'tempo_std': tempo_std,
                'tempos': tempos
            })

            print(f"  → Média: {tempo_medio:.4f}s (±{tempo_std:.4f}s)")
        else:
            print(f"  → ERRO: Falhou em todas as execuções")

    print("\n" + "=" * 90)
    print(f"Benchmark concluído! {len(resultados)}/{len(instancias)} instâncias executadas com sucesso")
    print("=" * 90)

    if not resultados:
        print("\nNenhuma instância foi executada com sucesso. Verifique o caminho do solver.")
        return

    # Criar tabela de resultados
    print("\n" + "=" * 90)
    print("TABELA DE RESULTADOS")
    print("=" * 90)
    print(f"{'Inst':^6}{'n':^6}{'m_real':^8}{'m_rest':^8}{'n*(m+n)':^10}{'Tempo (s)':^12}{'Desvio':^10}")
    print("-" * 90)

    for idx, r in enumerate(resultados, 1):
        print(f"{idx:^6}{r['n']:^6}{r['m_realizados']:^8}{r['m_restantes']:^8}"
              f"{r['complexidade']:^10}{r['tempo_medio']:^12.4f}{r['tempo_std']:^10.4f}")

    print("=" * 90)

    # Criar gráfico
    complexidades = [r['complexidade'] for r in resultados]
    tempos_medios = [r['tempo_medio'] for r in resultados]

    plt.figure(figsize=(12, 7))

    # Gráfico principal
    plt.plot(complexidades, tempos_medios, 'o-', linewidth=2, markersize=8, 
             color='#2E86AB', label='Tempo de Execução')

    # Adicionar barras de erro (desvio padrão)
    desvios = [r['tempo_std'] for r in resultados]
    plt.errorbar(complexidades, tempos_medios, yerr=desvios, fmt='none', 
                 ecolor='#A23B72', elinewidth=2, capsize=5, alpha=0.6)

    plt.xlabel('n × (m + n)', fontsize=13, fontweight='bold')
    plt.ylabel('Tempo de Execução (segundos)', fontsize=13, fontweight='bold')
    plt.title('Complexidade Temporal do Programa - Campeonato de Futebol', 
              fontsize=15, fontweight='bold', pad=20)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.legend(fontsize=11)

    # Ajustar layout
    plt.tight_layout()

    # Salvar gráfico
    plt.savefig('benchmark_grafico.png', dpi=300, bbox_inches='tight')
    print("\n✓ Gráfico salvo: benchmark_grafico.png")

    # Salvar dados em CSV
    with open('benchmark_resultados.csv', 'w') as f:
        f.write("Instancia,n,m_realizados,m_restantes,complexidade,tempo_medio,tempo_std\n")
        for idx, r in enumerate(resultados, 1):
            f.write(f"{idx},{r['n']},{r['m_realizados']},{r['m_restantes']},"
                   f"{r['complexidade']},{r['tempo_medio']:.6f},{r['tempo_std']:.6f}\n")

    print("✓ Dados salvos: benchmark_resultados.csv")

    plt.show()

if __name__ == "__main__":
    main()
