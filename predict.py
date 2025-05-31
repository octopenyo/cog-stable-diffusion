import os
import torch
from cog import BasePredictor, Input, Path
from diffusers import StableDiffusionPipeline

MODEL_ID = "prompthero/openjourney-v4"
torch_dtype = torch.float32  # CPU-safe

class Predictor(BasePredictor):
    def setup(self):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch_dtype,
            safety_checker=None
        )
        self.pipe.to("cpu")

    def predict(
        self,
        prompt: str = Input(description="Prompt to generate image from"),
        negative_prompt: str = Input(description="What to avoid in the image", default=""),
        guidance_scale: float = Input(description="Prompt strength (CFG)", default=7.5),
        num_inference_steps: int = Input(description="How many denoising steps", default=30),
        seed: int = Input(description="Random seed (for reproducibility)", default=0),
        width: int = Input(description="Image width", default=512),
        height: int = Input(description="Image height", default=512),
    ) -> Path:
        generator = torch.manual_seed(seed)
        output = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            generator=generator,
            width=width,
            height=height
        )
        image = output.images[0]
        out_path = "/tmp/output.png"
        image.save(out_path)
        return Path(out_path)
