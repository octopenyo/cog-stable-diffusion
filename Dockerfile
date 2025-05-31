# Use official Cog base image with cog pre-installed
FROM python:3.10-slim  # Lightweight alternative to Cog

# Install any system packages you need
RUN apt-get update && apt-get install -y git

# Install your Python dependencies
COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

# Copy in everything else (including cog.yaml and predict.py)
COPY . /code
WORKDIR /code

# Start the cog server
ENTRYPOINT ["cog", "serve"]
