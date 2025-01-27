# Dockerfile

# 1. Start with a slim Python 3.11 base
FROM python:3.11-slim

# 2. Install system dependencies if needed (e.g., git, build tools)
RUN apt-get update && apt-get install -y git

# 3. Create a working directory in the container
WORKDIR /app

# 4. Copy requirements.txt first (so Docker can cache the pip install layer)
COPY requirements.txt /app/

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your project
COPY . /app

# 7. By default, run a simple benchmark with resnet18, 30 iterations
#    You can override this CMD at runtime.
CMD ["python", "benchmark.py", "--model", "resnet18", "--iterations", "30"]
