#!/usr/bin/env python3
import subprocess
import time
import math
import matplotlib.pyplot as plt

# caminhos dos executáveis já compilados
GEN = "/home/carlique/Documents/IST/Year2/ASA/projeto/Entrega1/gerador_p1.o"      # gerador C++ do enunciado
PROG = "/home/carlique/Documents/IST/Year2/ASA/projeto/Entrega1/e1.o"      # o teu programa

# parâmetros
P_MAX = 50         # Pmax passado ao gerador (ajusta se quiseres)
SEED = 67671       # seed fixa para todos os n
N_VALUES = [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800]
N_CUBED = [50**3, 100**3, 150**3, 200**3, 250**3, 300**3, 400**3, 500**3, 600**3, 700**3, 800**3]

def generate_input_with_gen(n: int) -> str:
    """
    Usa o gerador C++:
        gen <N> <Pmax> <seed>
    e devolve o input gerado como string.
    """
    proc = subprocess.run(
        [GEN, str(n), str(P_MAX), str(SEED)],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=True,
        text=True
    )
    return proc.stdout

def run_once(input_data: str) -> float:
    """
    Executa o programa C++ uma vez com o input dado e devolve o tempo em segundos.
    """
    start = time.perf_counter()
    subprocess.run(
        [PROG],
        input=input_data,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
        text=True
    )
    end = time.perf_counter()
    return end - start

def main():
    means = []
    std_devs = []
    n_cubed = [n ** 3 for n in N_VALUES]

    REPS = 5  # número de repetições para média e desvio padrão

    for n in N_VALUES:
        inp = generate_input_with_gen(n)

        samples = [run_once(inp) for _ in range(REPS)]
        avg = sum(samples) / REPS
        var = sum((t - avg) ** 2 for t in samples) / REPS
        std = math.sqrt(var)

        print(f"n={n}, média={avg:.4f}s, desvio={std:.4f}s")

        means.append(avg)
        std_devs.append(std)

    plt.figure(figsize=(8, 5))
    # gráfico com barras de erro
    plt.errorbar(n_cubed, means, yerr=std_devs, fmt="o-", markersize = 4, capsize=4, color="#2b2d42", ecolor="#8d99ae")

    plt.xlabel(r"$n^3$")
    plt.ylabel("Tempo de execução (s)")
    plt.title("Tempo de execução do programa C++ em função de $n^3$")
    plt.grid(True)

    plt.savefig("tempo_vs_n3.png", dpi=150, bbox_inches="tight")
    print("Gráfico guardado em tempo_vs_n3.png")


if __name__ == "__main__":
    main()