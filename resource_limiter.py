# resource_limiter.py

import os
import psutil
import time


def limit_cpu_affinity(cpu_core_ids):
    """
    Restricts the current process (and optionally its children) to the specified CPU cores.
    This simulates having fewer CPU cores available.

    Args:
        cpu_core_ids (list of int): The indices of the CPU cores you want to allow.
                                    E.g., [0] to allow only the first core,
                                    [0,1] to allow the first two cores, etc.
    """
    process = psutil.Process(os.getpid())
    try:
        process.cpu_affinity(cpu_core_ids)
        print(f"Set CPU affinity to cores: {cpu_core_ids}")
    except AttributeError:
        print("Error: Setting CPU affinity is not supported on this platform.")
    except psutil.AccessDenied:
        print("Error: Insufficient permissions to set CPU affinity.")


def simulate_limited_cpu():
    """
    Example function to show how limiting CPU affinity might affect a CPU-intensive task.
    """
    print("Starting a CPU-intensive task with artificially limited CPU cores...")
    start = time.time()

    # A trivial CPU-intensive loop
    x = 0
    for i in range(10_000_000):
        x += i

    end = time.time()
    print(f"Result of CPU task: {x}, took {end - start:.2f} seconds")


if __name__ == "__main__":
    print("Demonstration of resource limiting approaches.")

    # 1. Demonstrate CPU affinity limiting to core #0 only
    limit_cpu_affinity([0])  # On a multi-core system, this simulates single-core performance
    simulate_limited_cpu()

    # 2. Return CPU affinity to default (all cores) or skip if you prefer
    # On Linux, you can get all available cores with list(range(psutil.cpu_count()))
    # On Windows, typically the same approach
    all_cores = list(range(psutil.cpu_count()))
    limit_cpu_affinity(all_cores)
    print(f"Restored CPU affinity to all cores: {all_cores}")

    # You could also add code to artificially limit memory, but that typically requires cgroups (Linux)
    # or Docker. For memory limiting on Windows or Mac, Docker is the simpler approach:
    #   docker run --cpus="1.0" --memory="1g" your_image
