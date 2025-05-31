import os
from typing import List

import torch
from cog import BasePredictor, Input, Path
from diffusers import (
    StableDiffusionPipeline,
    DPMSolverMultistepScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    LMSDiscreteScheduler,
    PNDMScheduler,
    DDIMScheduler,
)

# Updated for 2025 - Uses OpenJourney model with safe, modern pipeline
MODEL_ID = "prompthero/openjourney"

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory"""
        print("Loading pipeline...")
        self.pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            revision="fp16",
            use_safetensors=True
        ).to("cuda")

    @torch.inference_mode()
    def predict(
        self,
        prompt: str = Input(
            description="Input prompt",
            default="a photo of an astronaut riding a horse on mars",
        ),
        negative_prompt: str = Input(
            description="Things to avoid in the output",
            default=None,
        ),
        width: int = Input(
            description="Width of the image.",
            default=768,
            choices=[128, 256, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024],
        ),
        height: int = Input(
            description="Height of the image.",
            default=768,
            choices=[128, 256, 384, 448, 512, 576, 640, 704, 768, 832, 896, 960, 1024],
        ),
        num_outputs: int = Input(
            description="Number of images to generate",
            default=1,
            ge=1,
            le=4,
        ),
        num_inference_steps: int = Input(
            description="Steps to run the model",
            default=30,
            ge=1,
            le=100,
        ),
        guidance_scale: float = Input(
            description="Classifier-free guidance scale",
            default=7.5,
            ge=1,
            le=20,
        ),
        scheduler: str = Input(
            description="Sampling scheduler",
            default="DPMSolverMultistep",
            choices=[
                "DDIM",
                "K_EULER",
                "DPMSolverMultistep",
                "K_EULER_ANCESTRAL",
                "PNDM",
                "KLMS",
            ],
        ),
        seed: int = Input(
            description="Seed (leave blank for random)",
            default=None,
        ),
    ) -> List[Path]:

        if seed is None:
            seed = int.from_bytes(os.urandom(2), "big")
        print(f"Using seed: {seed}")

        if width * height > 786432:
            raise ValueError("Max size is 1024x768 or 768x1024 pixels")

        self.pipe.scheduler = make_scheduler(scheduler, self.pipe.scheduler.config)

        generator = torch.Generator("cuda").manual_seed(seed)
        output = self.pipe(
            prompt=[prompt] * num_outputs,
            negative_prompt=[negative_prompt] * num_outputs if negative_prompt else None,
            width=width,
            height=height,
            guidance_scale=guidance_scale,
            generator=generator,
            num_inference_steps=num_inference_steps,
        )

        output_paths = []
        for i, img in enumerate(output.images):
            output_path = f"/tmp/output-{i}.png"
            img.save(output_path)
            output_paths.append(Path(output_path))

        return output_paths

def make_scheduler(name, config):
    return {
        "PNDM": PNDMScheduler.from_config(config),
        "KLMS": LMSDiscreteScheduler.from_config(config),
        "DDIM": DDIMScheduler.from_config(config),
        "K_EULER": EulerDiscreteScheduler.from_config(config),
        "K_EULER_ANCESTRAL": EulerAncestralDiscreteScheduler.from_config(config),
        "DPMSolverMultistep": DPMSolverMultistepScheduler.from_config(config),
    }[name]
