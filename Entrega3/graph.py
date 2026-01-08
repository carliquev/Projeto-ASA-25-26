import subprocess
import time
import os
import matplotlib.pyplot as plt
import sys

# --- Configuration ---
CPP_GENERATOR_FILE = "gerador.cpp"
GENERATOR_EXE = "./gerador"  # Name of the compiled executable
PYTHON_SCRIPT = "e3_v2.py"
OUTPUT_IMAGE = "performance_graph.png"

# Test parameters
START_N = 5      # Start with N teams
END_N = 30       # End with N teams
STEP_N = 5       # Increment
PROBABILITY = 80 # Probability of games played (0-100)

def compile_generator():
    """Compiles the C++ generator code."""
    print(f"Compiling {CPP_GENERATOR_FILE}...")
    try:
        subprocess.run(["g++", "-o", "gerador", CPP_GENERATOR_FILE], check=True)
        print("Compilation successful.\n")
    except subprocess.CalledProcessError:
        print("Error: Compilation failed. Please check your C++ code.")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: g++ not found. Please ensure a C++ compiler is installed.")
        sys.exit(1)

def run_experiment():
    """Runs the generator and the python script, collecting metrics."""
    n_values = []
    input_sizes = [] # Number of lines/games in input
    execution_times = []

    print(f"{'N':<10} | {'Games':<10} | {'Time (s)':<10}")
    print("-" * 35)

    for n in range(START_N, END_N + 1, STEP_N):
        # 1. Run the Generator to create input
        # Command: ./gerador <N> <P>
        try:
            result_gen = subprocess.run(
                [GENERATOR_EXE, str(n), str(PROBABILITY)],
                capture_output=True,
                text=True,
                check=True
            )
            input_data = result_gen.stdout
        except subprocess.CalledProcessError as e:
            print(f"Generator failed for N={n}: {e}")
            continue

        # Calculate input size (number of games is usually line count - 1)
        # The first line is "N M", subsequent M lines are games.
        lines = input_data.strip().split('\n')
        num_games = 0
        if len(lines) > 0:
            header = lines[0].split()
            if len(header) >= 2:
                num_games = int(header[1])

        # 2. Run the Python Script (e3_v2.py) with the generated input
        start_time = time.time()
        try:
            # We pass the input_data via stdin
            subprocess.run(
                ["python3", PYTHON_SCRIPT],
                input=input_data,
                text=True,
                check=True,
                capture_output=True # We capture output so it doesn't clutter console
            )
        except subprocess.CalledProcessError as e:
            print(f"Script execution failed for N={n}: {e.stderr}")
            continue
        end_time = time.time()

        elapsed_time = end_time - start_time

        # Store data
        n_values.append(n)
        input_sizes.append(num_games)
        execution_times.append(elapsed_time)

        print(f"{n:<10} | {num_games:<10} | {elapsed_time:.4f}")

    return n_values, input_sizes, execution_times

def plot_results(n_vals, sizes, times):
    """Generates a dual-axis plot."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Number of Teams (N)')
    ax1.set_ylabel('Execution Time (seconds)', color=color)
    ax1.plot(n_vals, times, color=color, marker='o', label='Time')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)

    # Instantiate a second axes that shares the same x-axis
    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Input Size (Number of Games)', color=color)  
    ax2.plot(n_vals, sizes, color=color, linestyle='--', marker='x', label='Input Size')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f"Performance Analysis: {PYTHON_SCRIPT}\n(Probability P={PROBABILITY})")
    fig.tight_layout()  
    plt.savefig(OUTPUT_IMAGE)
    print(f"\nGraph saved to {OUTPUT_IMAGE}")
    plt.show()

if __name__ == "__main__":
    if not os.path.exists(PYTHON_SCRIPT):
        print(f"Error: {PYTHON_SCRIPT} not found in the current directory.")
        sys.exit(1)
        
    compile_generator()
    n_data, size_data, time_data = run_experiment()
    
    if n_data:
        plot_results(n_data, size_data, time_data)
    else:
        print("No data collected.")