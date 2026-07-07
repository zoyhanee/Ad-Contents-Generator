import torch
from diffusers import (
    PipelineQuantizationConfig,
    QwenImageEditPlusPipeline,
)

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
        raise NotImplementedError(
            "Qwen image generation is not implemented yet."
        )