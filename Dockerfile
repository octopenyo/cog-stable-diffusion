# Use a prebuilt Docker image for cog-stable-diffusion
FROM r8.im/octopenyo/cog-stable-diffusion:gpu

# Set the default command to run the Cog server
ENTRYPOINT ["cog", "serve"]
