import subprocess
import time
import os
import sys
import random
import statistics
import matplotlib.pyplot as plt

# --- CONFIGURATION -----------------------------------------------------------
GENERATOR_SOURCE = "gerador_p2.cpp"
PROJECT_SOURCE = "e2.cpp"
GENERATOR_EXE = "./generator" if os.name != 'nt' else "generator.exe"
PROJECT_EXE = "./project" if os.name != 'nt' else "project.exe"

# Test Cases (N, M, Density)
TEST_CASES = [

    (50, 1000, 50),
    (100, 1000, 50),
    #(150, 1000, 50),
    (200, 1000, 50),
    #(250, 1000, 50),
    (300, 1000, 50),
    #(350, 1000, 50),
    (400, 1000, 50),
    #(450, 1000, 50),
    (500, 1000, 50),
    #(550, 1000, 50),
    (600, 1000, 50),
    (650, 1000, 50),
    (700, 1000, 50),
    (750, 1000, 50),
    (800, 1000, 50),
    (850, 1000, 50),
    #(1000, 1000, 50),
    #(1250, 1000, 50),
    #(1500, 1000, 50),
    #(2000, 1000, 50),
]

RUNS_PER_CASE = 10
COMPILER = "g++"
FLAGS = ["-O3", "-std=c++11"]
# -----------------------------------------------------------------------------

def compile_cpp(source, output):
    exe_name = output.replace("./", "")
    needs_compile = True
    if os.path.exists(exe_name) and os.path.exists(source):
        if os.path.getmtime(exe_name) > os.path.getmtime(source):
            needs_compile = False

    if needs_compile:
        print(f"Compiling {source}...")
        try:
            subprocess.check_call([COMPILER] + FLAGS + ["-o", exe_name, source])
        except subprocess.CalledProcessError:
            print(f"Error: Failed to compile {source}")
            sys.exit(1)

def run_test_case(n, m, d):
    """
    Runs the benchmark multiple times with random seeds.
    Returns: (avg_time_sec, stdev_sec, avg_k_value)
    """
    durations_sec = []
    k_values = []
    
    for i in range(RUNS_PER_CASE):
        # 1. Generate Input with a UNIQUE SEED for every run
        current_seed = random.randint(1, 10000000)
        
        gen_cmd = [GENERATOR_EXE, str(n), str(m), str(d), str(current_seed)]
        try:
            gen_process = subprocess.run(gen_cmd, capture_output=True, text=True, check=True)
            input_data = gen_process.stdout
        except subprocess.CalledProcessError:
            print(f"Generator failed for N={n}, seed={current_seed}")
            return None, None, None

        # 2. Extract K (Edges)
        try:
            lines_text = input_data.strip().split('\n')
            if len(lines_text) >= 4:
                k_val = int(lines_text[3].strip())
            else:
                k_val = int(input_data.split()[4])
            k_values.append(k_val)
        except (ValueError, IndexError):
            k_values.append(0)

        # 3. Benchmark Project
        start = time.perf_counter()
        try:
            subprocess.run(
                [PROJECT_EXE],
                input=input_data,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError:
            print(f"Project crashed for N={n}")
            return None, None, None
        
        end = time.perf_counter()
        # Store time directly in seconds (no multiplication)
        durations_sec.append(end - start)

    # 4. Calculate Stats
    avg_time = statistics.mean(durations_sec)
    stdev_time = statistics.stdev(durations_sec) if len(durations_sec) > 1 else 0.0
    avg_k = int(statistics.mean(k_values))
    
    return avg_time, stdev_time, avg_k

def plot_results(x_vals, y_vals, y_errs):
    plt.figure(figsize=(10, 6))
    
    plt.errorbar(x_vals, y_vals, yerr=y_errs, fmt='o-', color='b', 
                 ecolor='red', capsize=5, label='Tempo com desvio')
    
    plt.title(r'Análise de tempo: Tempo para $N(N+K)$')
    plt.xlabel(r'Complexidade: $N \times (N + K_{avg})$')
    plt.ylabel('Tempo de execução (segundos)') # Label updated
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    output_file = "benchmark_plot_seconds.png"
    plt.savefig(output_file)
    print(f"\nGraph saved to {output_file}")

def main():
    compile_cpp(GENERATOR_SOURCE, GENERATOR_EXE)
    compile_cpp(PROJECT_SOURCE, PROJECT_EXE)

    x_data = []      # N * (N + Avg_K)
    y_data = []      # Average Time (s)
    y_err_data = []  # Standard Deviation (s)

    print(f"\n{'N':<6} {'M':<6} {'Avg K':<10} {'N*(N+K)':<15} | {'Avg Time (s)':<15} | {'StDev (s)':<12}")
    print("-" * 85)

    for n, m, d in TEST_CASES:
        avg, stdev, k = run_test_case(n, m, d)
        
        if avg is not None:
            metric = n * (n + k)
            
            x_data.append(metric)
            y_data.append(avg)
            y_err_data.append(stdev)
            
            # Using 6 decimal places for better precision in seconds
            print(f"{n:<6} {m:<6} {k:<10} {metric:<15} | {avg:<15.6f} | {stdev:.6f}")
        else:
            print(f"{n:<6} {m:<6} {'-':<10} {'-':<15} | FAILED")

    if x_data:
        plot_results(x_data, y_data, y_err_data)
    else:
        print("No successful runs to plot.")

if __name__ == "__main__":
    main()