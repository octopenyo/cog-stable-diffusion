# Use official Cog base image with cog pre-installed
FROM r8.im/cog/cog:0.7.2

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
