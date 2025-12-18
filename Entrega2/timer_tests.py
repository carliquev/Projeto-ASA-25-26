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
    (100, 1000, 50),
    (250, 1000, 50),
    (300, 1000, 50),
    (500, 1000, 50),
    (700, 1000, 50),
    (750, 1000, 50),
    (1000, 500, 50),
    (1250, 600, 50),
    (1500, 750, 50),
    (2000, 1000, 50),
]

RUNS_PER_CASE = 5
COMPILER = "g++"
FLAGS = ["-O3 -Wall", "-std=c++11"]
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
    """Returns (average_time, standard_deviation)."""
    # 1. Generate Input
    gen_cmd = [GENERATOR_EXE, str(n), str(m), str(d), str(random.randint(0, 42))]
    try:
        gen_process = subprocess.run(gen_cmd, capture_output=True, text=True, check=True)
        input_data = gen_process.stdout
    except subprocess.CalledProcessError:
        return None, None

    # 2. Benchmark Project Multiple Times
    durations = []
    for _ in range(RUNS_PER_CASE):
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
            return None, None
        durations.append(time.perf_counter() - start)

    # 3. Calculate Stats
    avg_time = statistics.mean(durations)
    # If we only run once, stdev is 0
    stdev_time = statistics.stdev(durations) if len(durations) > 1 else 0.0
    
    return avg_time, stdev_time

def plot_results(x_vals, y_vals, y_errs):
    """Generates a plot with error bars."""
    plt.figure(figsize=(10, 6))
    
    # 'yerr' adds the margin of error bars
    # 'capsize' adds the little horizontal lines at the top/bottom of the error bars
    plt.errorbar(x_vals, y_vals, yerr=y_errs, fmt='o-', color='b', 
                 ecolor='red', capsize=5, label='Tempo medido ± margem de erro')
    
    plt.title('Performance Analysis: Time vs N(N+M)')
    plt.xlabel('Complexity Factor: N * (N + M)')
    plt.ylabel('Execution Time (seconds)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    output_file = "benchmark_plot_with_error.png"
    plt.savefig(output_file)
    print(f"\nGraph saved to {output_file}")
    plt.show()

def main():
    compile_cpp(GENERATOR_SOURCE, GENERATOR_EXE)
    compile_cpp(PROJECT_SOURCE, PROJECT_EXE)

    x_data = []      # N * (N + M)
    y_data = []      # Average Time
    y_err_data = []  # Standard Deviation

    print(f"\n{'N':<8} {'M':<8} {'N*(N+M)':<15} | {'Avg Time (s)':<15} | {'StDev (s)':<15}")
    print("-" * 75)

    for n, m, d in TEST_CASES:
        avg, stdev = run_test_case(n, m, d)
        
        if avg is not None:
            metric = n * (n + m)
            x_data.append(metric)
            y_data.append(avg)
            y_err_data.append(stdev)
            
            print(f"{n:<8} {m:<8} {metric:<15} | {avg:.6f}          | {stdev:.6f}")
        else:
            print(f"{n:<8} {m:<8} {'-':<15} | FAILED")

    if x_data:
        plot_results(x_data, y_data, y_err_data)
    else:
        print("No successful runs to plot.")

if __name__ == "__main__":
    main()