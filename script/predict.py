from cog import BasePredictor, Input
from diffusers import StableDiffusionPipeline
import torch

class Predictor(BasePredictor):
    def setup(self):
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float16
        ).to("cuda")

    def predict(self, prompt: str = Input(description="Text prompt")) -> str:
        image = self.pipe(prompt).images[0]
        output_path = "/tmp/output.png"
        image.save(output_path)
        return output_path
