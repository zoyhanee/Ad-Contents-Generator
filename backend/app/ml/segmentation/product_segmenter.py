import numpy as np
import torch
from PIL import Image, ImageFilter
from torchvision import transforms

from app.ml.model_loader import ManagedModel
from app.ml.segmentation.birefnet_loader import load_birefnet

_TRANSFORM = transforms.Compose([
    transforms.Resize((1024, 1024)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def _crop_to_content_bbox(
    foreground: Image.Image, mask_img: Image.Image, padding_px: int,
) -> tuple[Image.Image, Image.Image]:

    alpha = np.array(mask_img)
    ys, xs = np.where(alpha > 10)

    if len(xs) == 0 or len(ys) == 0:
        return foreground, mask_img

    x1, x2 = int(xs.min()), int(xs.max()) + 1
    y1, y2 = int(ys.min()), int(ys.max()) + 1

    x1 = max(0, x1 - padding_px)
    y1 = max(0, y1 - padding_px)
    x2 = min(foreground.width, x2 + padding_px)
    y2 = min(foreground.height, y2 + padding_px)

    return foreground.crop((x1, y1, x2, y2)), mask_img.crop((x1, y1, x2, y2))


def extract_product_foreground(
    image_path: str,
    output_path: str,
    mask_path: str,
    edge_erode_px: int = 5,
    model=None,
    tight_crop: bool = True,
) -> None:

    original = Image.open(image_path).convert("RGB")
    device = "cuda" if torch.cuda.is_available() else "cpu"

    def _run_inference(loaded_model):
        input_tensor = _TRANSFORM(original).unsqueeze(0).to(device)
        with torch.no_grad():
            preds = loaded_model(input_tensor)[-1].sigmoid().cpu()
        return preds[0].squeeze()

    if model is not None:
        mask = _run_inference(model)
    else:
        with ManagedModel(load_birefnet, name="birefnet") as loaded_model:
            mask = _run_inference(loaded_model)

    mask_img = transforms.ToPILImage()(mask).resize(original.size)

    if edge_erode_px > 0:
        mask_img = mask_img.filter(ImageFilter.MinFilter(edge_erode_px * 2 + 1))

    foreground = original.copy()
    foreground.putalpha(mask_img)

    if tight_crop:
        foreground, mask_img = _crop_to_content_bbox(
            foreground, mask_img, padding_px=edge_erode_px * 3,
        )

    mask_img.save(mask_path)
    foreground.save(output_path)
