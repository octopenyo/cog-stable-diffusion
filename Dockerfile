FROM r8.im/replicate/cog-stable-diffusion:latest

COPY . /src
WORKDIR /src

ENTRYPOINT ["cog", "serve"]
