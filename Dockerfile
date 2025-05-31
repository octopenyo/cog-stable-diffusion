# Use Cog’s prebuilt base image that includes everything: Cog + Python + Torch + Diffusers
FROM r8.im/replicate/cog-stable-diffusion

# Optional: switch to your model weights if needed
# COPY your-model-weights /weights

# Default: run cog serve
ENTRYPOINT ["cog", "serve"]
