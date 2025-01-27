# parallel_runner.py

import os
import subprocess
from multiprocessing import Process
import sys


def run_benchmark(args_list, process_id):
    """
    Runs benchmark.py in a subprocess with the given CLI arguments.
    Args:
        args_list (list): A list of command-line arguments 
                          (e.g., ["--model", "resnet18", "--iterations", "30"]).
        process_id (int): An ID to identify this process in logs/prints.
    """
    print(f"[Process {process_id}] Starting benchmark with args: {args_list}")

    # "python benchmark.py" plus the CLI arguments
    cmd = [sys.executable, "benchmark.py"] + args_list

    try:
        # subprocess.run blocks until the command finishes
        subprocess.run(cmd, check=True)
        print(f"[Process {process_id}] Finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[Process {process_id}] Error: {e}")


def main():
    """
    Example concurrency:
    We define a list of different argument sets for benchmark.py,
    spawn a process for each set, and run them in parallel.
    """
    # Each item in this list is a separate process's arguments to benchmark.py
    benchmark_args = [
        ["--model", "resnet18", "--iterations", "30", "--batch-size", "1", "--save-logs"],
        ["--model", "mobilenet_v2", "--iterations", "30", "--batch-size", "2", "--save-logs"],
        ["--model", "alexnet", "--iterations", "30", "--batch-size", "1", "--mock-delay", "0.01", "--save-logs"]
    ]

    processes = []

    # Create and start a process for each set of arguments
    for i, args in enumerate(benchmark_args):
        p = Process(target=run_benchmark, args=(args, i))
        processes.append(p)
        p.start()

    # Optionally, wait for all processes to finish
    for p in processes:
        p.join()

    print("All concurrent benchmarks have finished.")


if __name__ == "__main__":
    main()
