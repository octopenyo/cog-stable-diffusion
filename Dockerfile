# Use a public base image
FROM python:3.10-slim

# Install system packages
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run Cog
CMD ["cog", "serve"]
