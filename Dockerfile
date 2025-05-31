# Use a slim Python image as base
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
 && rm -rf /var/lib/apt/lists/*

# Install Cog CLI
RUN pip install cog

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start cog server
CMD ["cog", "serve"]
