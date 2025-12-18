import subprocess
import time
import statistics
import os
import sys
import math
import matplotlib.pyplot as plt

# -------------------- CONFIGURAÇÃO --------------------

SOLVER_SRC = "e2.cpp"  # código da solução
SOLVER_EXEC = "./project"  # executável da solução

GEN_SRC = "gerador_p2.cpp"  # código do gerador
GEN_EXEC = "./generator"  # executável do gerador

Ks = []

NUM_TRUCKS = 1000  # M
DENSITY = 50  # D (0-100)
RUNS_PER_N = 10

NS = [i for i in range(50, 1000, 50)]

# -------------------- UTILITÁRIOS --------------------


def ensure_dir_for_file(path: str):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def make_executable(path: str):
    # Se existir mas não for executável, tenta corrigir permissões
    if os.path.exists(path) and not os.access(path, os.X_OK):
        try:
            os.chmod(path, os.stat(path).st_mode | 0o111)
        except Exception:
            pass


# -------------------- COMPILAÇÃO --------------------


def compile_cpp(source: str, output: str):
    """Compila um ficheiro C++ usando g++ com flags de optimização."""
    if not os.path.exists(source):
        print(f"[ERRO] Ficheiro fonte '{source}' não encontrado.")
        sys.exit(1)

    ensure_dir_for_file(output)

    print(f"Compilando {source} -> {output} ...")
    cmd = ["g++", "-O3", "-std=c++11", source, "-o", output]
    ret = subprocess.run(cmd)

    if ret.returncode != 0:
        print(f"[ERRO] Falha ao compilar {source}.")
        sys.exit(1)

    make_executable(output)


def ensure_executables():
    """Verifica se os executáveis existem; se não, compila."""
    if not os.path.exists(SOLVER_EXEC):
        compile_cpp(SOLVER_SRC, SOLVER_EXEC)
    else:
        make_executable(SOLVER_EXEC)

    if not os.path.exists(GEN_EXEC):
        compile_cpp(GEN_SRC, GEN_EXEC)
    else:
        make_executable(GEN_EXEC)


# -------------------- BENCHMARK --------------------


def run_instance(n: int, seed: int):
    """
    Gera uma instância e mede o tempo do solver.
    Retorna (tempo_segundos, K_real).
    """
    gen_cmd = [GEN_EXEC, str(n), str(NUM_TRUCKS), str(DENSITY), str(seed)]

    try:
        gen_out = subprocess.check_output(gen_cmd, text=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("[ERRO] Gerador falhou.")
        if e.stderr:
            print("STDERR do gerador:\n", e.stderr)
        sys.exit(1)

    # Parse do K real: 4ª linha (0-index: 3)
    lines = gen_out.splitlines()
    if len(lines) < 4:
        raise RuntimeError("Output do gerador inválido (menos de 4 linhas).")
    try:
        K_real = int(lines[3].strip())
    except ValueError:
        raise RuntimeError(f"Não consegui ler K na linha 4: '{lines[3]}'")

    start = time.perf_counter()
    try:
        subprocess.run(
            [SOLVER_EXEC],
            input=gen_out,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print("[ERRO] Solver falhou.")
        if e.stderr:
            print("STDERR do solver:\n", e.stderr)
        raise
    end = time.perf_counter()

    return (end - start, K_real)


def approx_K_for_density_dag(n: int, density_percent: int) -> float:
    """
    Aproxima K para um DAG gerado tipicamente só com arestas i->j com i<j:
    máximo de arestas = n(n-1)/2.
    """
    max_edges = n * (n - 1) / 2.0
    return (density_percent / 100.0) * max_edges


def main():
    ensure_executables()

    results_n = []
    means = []
    stds = []

    print("-" * 40)
    print("Iniciando Benchmark")
    print(f"M (Trucks): {NUM_TRUCKS}, D (Density): {DENSITY}%")
    print("-" * 40)

    for n in NS:
        print(f"Testando n = {n} ... ", end="", flush=True)
        times = []

        for r in range(RUNS_PER_N):
            seed = 1234 + r
            t, K_real = run_instance(n, seed)
            times.append(t)
            Ks.append(K_real)

        avg_time = statistics.mean(times)
        std_time = statistics.pstdev(times) if len(times) > 1 else 0.0

        results_n.append(n)
        means.append(avg_time)
        stds.append(std_time)

        print(f"Média: {avg_time * 1000:.2f} ms")

    # -------------------- TABELAS --------------------

    print("\n" + "=" * 50)
    print("RESULTADOS (Markdown)")
    print("=" * 50)
    print("| Tamanho n | Tempo médio (ms) | Desvio padrão (ms) |")
    print("|----------:|-----------------:|-------------------:|")
    for n, m, s in zip(results_n, means, stds):
        print(f"| {n:9d} | {m * 1000:16.3f} | {s * 1000:18.3f} |")

    print("\n" + "=" * 50)
    print("RESULTADOS (LaTeX)")
    print("=" * 50)
    print("\\begin{tabular}{@{}rrr@{}}")
    print("    \\toprule")
    print("    Size $n$ & Time (ms) & Std (ms) \\\\")
    print("    \\midrule")
    for n, m, s in zip(results_n, means, stds):
        ms = m * 1000
        sd = s * 1000
        ms_latex = f"{ms:.3f}".replace(".", "{,}")
        sd_latex = f"{sd:.3f}".replace(".", "{,}")
        print(f"    {n:<10d} & {ms_latex:>10} & {sd_latex:>10} \\\\")
    print("    \\bottomrule\n\\end{tabular}")

    # -------------------- PLOT --------------------

    # Eixo X = f(N,K) = N*(N+K), com K aproximado via densidade num DAG típico
    x_values = []
    for n in results_n:
        K_est = approx_K_for_density_dag(n, DENSITY)
        x_values.append(float(n) * (float(n) + K_est))

    x_label = r"Complexidade: $N \times (N + K)$"

    y_values = means
    y_err = stds

    plt.figure(figsize=(8, 6))
    plt.errorbar(
        x_values,
        y_values,
        yerr=y_err,
        fmt="o",
        capsize=4,
        markersize=5,
        label="Tempo com desvio",
        color="#2b2d42",
        ecolor="#8d99ae"
    )
    plt.plot(x_values, y_values, linestyle="--", linewidth=1, alpha=0.7, color="black")

    plt.xlabel(x_label, fontsize=11)
    plt.ylabel("Tempo de Execução (segundos)", fontsize=11)
    plt.title(f"Análise de tempo: Tempo para $N(N+K)$", fontsize=13)

    plt.ticklabel_format(style="sci", axis="x", scilimits=(0, 0))
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)
    plt.legend()
    plt.tight_layout()

    filename = "tempo_vs_fn.png"
    plt.savefig(filename, dpi=300)
    print(f"\n[SUCESSO] Gráfico salvo como '{filename}'.")


if __name__ == "__main__":
    main()