from io import BytesIO

import torch
from diffusers import (
    PipelineQuantizationConfig,
    QwenImageEditPlusPipeline,
)
from PIL import Image

from app.ml.image_clients.base import ImageModelClient


class QwenImageClient(ImageModelClient):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.pipeline = None

    def _load_pipeline(self) -> None:
        if self.pipeline is not None:
            return

        quantization_config = PipelineQuantizationConfig(
            quant_backend="bitsandbytes_4bit",
            quant_kwargs={
                "load_in_4bit": True,
                "bnb_4bit_quant_type": "nf4",
                "bnb_4bit_compute_dtype": torch.bfloat16,
            },
            components_to_quantize=["transformer"],
        )

        self.pipeline = QwenImageEditPlusPipeline.from_pretrained(
            self.model_name,
            torch_dtype=torch.bfloat16,
            quantization_config=quantization_config,
        )

    def generate(
        self,
        prompt: str,
        source_image_path: str | None = None,
    ) -> bytes:
        if source_image_path is None:
            raise ValueError(
                "Qwen image editing requires a source image."
            )

        self._load_pipeline()

        source_image = Image.open(source_image_path).convert("RGB")

        result = self.pipeline(
            image=source_image,
            prompt=prompt,
            num_inference_steps=50,
            true_cfg_scale=4.0,
            output_type="pil",
        )

        generated_image = result.images[0]

        buffer = BytesIO()
        generated_image.save(buffer, format="PNG")

        return buffer.getvalue()