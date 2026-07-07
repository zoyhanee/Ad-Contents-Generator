import torch
from diffusers import (
    PipelineQuantizationConfig,
    QwenImageEditPlusPipeline,
)


MODEL_ID = "Qwen/Qwen-Image-Edit-2511"


quantization_config = PipelineQuantizationConfig(
    quant_backend="bitsandbytes_4bit",
    quant_kwargs={
        "load_in_4bit": True,
        "bnb_4bit_quant_type": "nf4",
        "bnb_4bit_compute_dtype": torch.bfloat16,
    },
    components_to_quantize=["transformer"],
)


print("Loading model...")

pipe = QwenImageEditPlusPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.bfloat16,
    quantization_config=quantization_config,
)

print("Pipeline loaded successfully")
print("Pipeline:", type(pipe).__name__)
print("Transformer:", type(pipe.transformer).__name__)