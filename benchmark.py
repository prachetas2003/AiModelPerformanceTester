# benchmark.py
import argparse
import json
import time
import torch
import torchvision.models as models

from hardware_monitor import get_system_metrics

# Dictionary of supported TorchVision models you can expand as needed
AVAILABLE_MODELS = {
    'resnet18': models.resnet18,
    'mobilenet_v2': models.mobilenet_v2,
    'alexnet': models.alexnet
    # Add more models as you like (e.g., models.vgg16, models.squeezenet1_0, etc.)
}


def benchmark_model(model, input_size=(1, 3, 224, 224), num_iterations=50, mock_delay=0.0):
    """
    Benchmarks a given PyTorch model by measuring inference latency and throughput.
    Optionally adds a mock_delay (in seconds) to each iteration to simulate slower hardware.

    Args:
        model (torch.nn.Module): The loaded PyTorch model in eval mode.
        input_size (tuple): Shape of the input (batch_size, channels, height, width).
        num_iterations (int): Number of forward passes to time.
        mock_delay (float): Optional artificial delay (in seconds) added before each inference.

    Returns:
        avg_time (float): Average inference time (seconds per forward pass, at batch_size=1 if relevant).
        throughput (float): Number of inferences per second (1 / avg_time if batch_size=1).
        metrics_log (list of dict): Detailed metrics for each iteration, including CPU/mem usage.
    """
    # Create a random input tensor for inference
    dummy_input = torch.randn(*input_size)

    # Warm-up pass to avoid cold-start overhead
    _ = model(dummy_input)

    times = []
    metrics_log = []

    for i in range(num_iterations):
        # Artificial delay to simulate slower hardware
        time.sleep(mock_delay)

        # Metrics before inference
        metrics_before = get_system_metrics()

        start_time = time.time()
        _ = model(dummy_input)
        end_time = time.time()

        # Metrics after inference
        metrics_after = get_system_metrics()

        elapsed_time = end_time - start_time
        times.append(elapsed_time)

        metrics_log.append({
            'iteration': i,
            'before': metrics_before,
            'after': metrics_after,
            'inference_time': elapsed_time
        })

    # Calculate average inference time
    avg_time = sum(times) / len(times) if len(times) > 0 else 0.0

    # If batch_size=1, throughput = 1 / avg_time
    throughput = 1.0 / avg_time if avg_time != 0 else float('inf')

    return avg_time, throughput, metrics_log


def main():
    """
    Parse CLI arguments, load the requested model, run benchmarks, and optionally save logs.
    """
    parser = argparse.ArgumentParser(
        description="Benchmark PyTorch models and collect CPU/memory usage."
    )

    parser.add_argument(
        '--model',
        type=str,
        default='resnet18',
        help=f"Choose a model from: {list(AVAILABLE_MODELS.keys())}"
    )
    parser.add_argument(
        '--iterations',
        type=int,
        default=50,
        help="Number of inference iterations to measure."
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=1,
        help="Batch size for the input tensor (default=1)."
    )
    parser.add_argument(
        '--mock-delay',
        type=float,
        default=0.0,
        help="Artificial delay in seconds to add before each inference."
    )
    parser.add_argument(
        '--save-logs',
        action='store_true',
        help="If set, save detailed metrics to a JSON file in the logs/ folder."
    )

    args = parser.parse_args()

    model_name = args.model.lower()
    iterations = args.iterations
    batch_size = args.batch_size
    mock_delay = args.mock_delay

    # Validate the chosen model
    if model_name not in AVAILABLE_MODELS:
        print(f"Error: '{model_name}' is not a supported model.")
        print(f"Please choose from {list(AVAILABLE_MODELS.keys())}")
        return

    # Load the chosen pretrained model
    print(f"\nLoading {model_name} model (pretrained=True).")
    model_fn = AVAILABLE_MODELS[model_name]
    model = model_fn(pretrained=True)
    model.eval()

    # Adjust input size for chosen batch size
    # Typically: (batch_size, 3, 224, 224) for most TorchVision classification models
    input_size = (batch_size, 3, 224, 224)

    # Run the benchmark
    avg_time, throughput, log_data = benchmark_model(
        model,
        input_size=input_size,
        num_iterations=iterations,
        mock_delay=mock_delay
    )

    # Print results
    print("-" * 50)
    print(f"Model: {model_name}")
    print(f"Iterations: {iterations}")
    print(f"Batch Size: {batch_size}")
    if mock_delay > 0:
        print(f"Mock Delay: {mock_delay} sec per iteration")
    print(f"Average Inference Time: {avg_time:.4f} seconds")
    print(f"Throughput: {throughput:.2f} inferences/sec")
    print("-" * 50, "\n")

    # (Optional) Save logs to a JSON file
    if args.save_logs:
        # Create logs folder if it doesn't exist
        import os
        if not os.path.exists("logs"):
            os.makedirs("logs")

        timestamp_str = time.strftime("%Y%m%d_%H%M%S")
        filename = f"metrics_log_{model_name}_{timestamp_str}.json"
        file_path = os.path.join("logs", filename)

        with open(file_path, "w") as f:
            json.dump(log_data, f, indent=2)

        print(f"Detailed logs saved to {file_path}")


if __name__ == "__main__":
    main()
