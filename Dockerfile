# Use Cog base image that includes Cog + Torch + Diffusers
FROM r8.im/replicate/cog-stable-diffusion

# Optional: Copy your model weights if needed
# COPY your-model-weights /weights

# Make sure your code is included
COPY . .

# Start the cog server
ENTRYPOINT ["cog", "serve"]
