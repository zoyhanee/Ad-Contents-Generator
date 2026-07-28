import torch
from transformers import AutoModelForImageSegmentation

MODEL_NAME = "ZhengPeng7/BiRefNet"


def load_birefnet():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForImageSegmentation.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
        dtype=torch.float32,
        low_cpu_mem_usage=True,
    )
    model.to(device)
    model.eval()
    return model
