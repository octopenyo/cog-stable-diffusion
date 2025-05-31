# Use lightweight Python 3.10 base image (no Cog dependency)
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git gcc python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /code

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Set environment variables for CPU-only operation
ENV COG_WEIGHTS_CACHE="/code/weights" \
    COG_MODEL_CACHE="/code/model-cache" \
    TORCH_DEVICE="cpu"

# Start the server (fixed typo from EVERYPOINT to ENTRYPOINT)
ENTRYPOINT ["cog", "serve"]
