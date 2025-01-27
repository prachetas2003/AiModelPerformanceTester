# AiModelPerformanceTester

## Overview

The **AI Model Performance Testing Framework** is a comprehensive tool designed to benchmark and analyze the performance of pre-trained AI models across various hardware configurations. This framework captures essential performance metrics such as throughput, latency, and CPU/memory usage, while enabling concurrent executions to simulate real-world AI workloads effectively. Additionally, it offers advanced data analysis and visualization capabilities through interactive dashboards and Jupyter Notebooks, facilitating in-depth performance insights and optimization.

## Features

- **Scalable Benchmarking:** Evaluate multiple AI models (e.g., ResNet-18, MobileNetV2, AlexNet) across diverse hardware setups.
- **Performance Metrics:** Measure key indicators like throughput, latency, CPU utilization, and memory usage.
- **Concurrent Executions:** Simulate real-world AI workloads by running multiple benchmarks in parallel.
- **Data Analysis & Visualization:** Utilize Plotly Dash for interactive dashboards and Jupyter Notebooks for detailed data exploration.
- **Resource Limiting with Docker:** Simulate hardware constraints by limiting CPU and memory resources using Docker containers.
- **Comprehensive Logging:** Generate detailed JSON logs for each benchmark run, enabling thorough analysis and reporting.

## Project Structure


###ai_model_performance_testing/
- ├── hardware_monitor.py        Collects CPU and memory usage metrics before and after model inferences
- ├── benchmark.py               Benchmarks AI models, measures performance, and logs metrics
- ├── parallel_runner.py         Executes multiple benchmark processes concurrently
- ├── dashboard.py               Launches an interactive Plotly Dash dashboard for visualizing benchmark results
- ├── analysis.ipynb             Jupyter Notebook for in-depth data analysis and visualization of benchmark logs
- ├── resource_limiter.py        Simulates hardware constraints by limiting CPU affinity and injecting faults
- ├── Dockerfile                 Defines the Docker image setup for running benchmarks with resource limitations
- ├── requirements.txt           Lists all Python dependencies required for the project
- ├── README.md                  Project documentation and setup instructions
- └── logs/                      Directory to store generated JSON log files from benchmark runs
-    ├── metrics_log_resnet18_20250126_070723.json
-    ├── metrics_log_mobilenet_v2_20250126_070830.json
-    └── metrics_log_alexnet_20250126_070945.json


### File and Directory Descriptions

- **`hardware_monitor.py`**
  - **Purpose:** Collects real-time CPU and memory usage metrics before and after each model inference. This helps in assessing the resource utilization of AI models during benchmarking.
  
- **`benchmark.py`**
  - **Purpose:** Core script that benchmarks specified AI models by measuring their throughput, latency, and resource usage over a defined number of iterations. It logs detailed metrics for each run.
  
- **`parallel_runner.py`**
  - **Purpose:** Facilitates the concurrent execution of multiple benchmark processes. This allows for simulating real-world scenarios where multiple AI models are running simultaneously, thereby testing the system's ability to handle parallel workloads.
  
- **`dashboard.py`**
  - **Purpose:** Launches an interactive web-based dashboard using Plotly Dash. The dashboard visualizes benchmark results, enabling users to easily interpret performance metrics through dynamic graphs and charts.
  
- **`analysis.ipynb`**
  - **Purpose:** A Jupyter Notebook designed for comprehensive data analysis of the generated benchmark logs. It provides detailed visualizations and statistical insights, aiding in the deeper understanding of model performance and resource utilization.
  
- **`resource_limiter.py`**
  - **Purpose:** Simulates hardware constraints by limiting CPU affinity and injecting faults. This is crucial for pre-silicon validation and ensuring that AI workloads can perform reliably under various hardware limitations.
  
- **`Dockerfile`**
  - **Purpose:** Defines the Docker image setup required to run benchmarks within isolated containers. It ensures consistent benchmarking environments by specifying dependencies and resource limitations.
  
- **`requirements.txt`**
  - **Purpose:** Enumerates all Python packages and their respective versions needed to run the project. This ensures that anyone cloning the repository can install the exact dependencies required for the framework to function correctly.
  
- **`README.md`**
  - **Purpose:** Provides an overview of the project, detailed setup instructions, usage guidelines, and other relevant information to help users understand and utilize the framework effectively.
  
- **`logs/` Directory**
  - **Purpose:** Stores all JSON log files generated from benchmark runs. Each log file contains detailed metrics for individual benchmark executions, facilitating easy access and analysis of performance data.

### Example Log File Structure (`metrics_log_resnet18_20250126_070723.json`)

```json
[
  {
    "iteration": 0,
    "before": {
      "cpu_percent": 20.5,
      "memory_percent": 55.3,
      "timestamp": 1682582400.123
    },
    "after": {
      "cpu_percent": 35.2,
      "memory_percent": 55.3,
      "timestamp": 1682582400.456
    },
    "inference_time": 0.333
  },
  {
    "iteration": 1,
    "before": {
      "cpu_percent": 25.1,
      "memory_percent": 55.4,
      "timestamp": 1682582400.789
    },
    "after": {
      "cpu_percent": 37.8,
      "memory_percent": 55.4,
      "timestamp": 1682582401.123
    },
    "inference_time": 0.334
  },
  ...
]

