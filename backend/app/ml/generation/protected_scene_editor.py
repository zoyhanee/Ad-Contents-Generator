from io import BytesIO

import numpy as np
from PIL import Image, ImageFilter

from app.ml.image_clients.gpt_image_client import edit_image_region


def _letterbox_place(
    product_fg: Image.Image,
    product_mask: Image.Image,
    canvas_size: tuple[int, int],
    product_box: dict,
) -> tuple[Image.Image, Image.Image, tuple[int, int, int, int]]:
    canvas_w, canvas_h = canvas_size
    px = int(product_box["x"] * canvas_w)
    py = int(product_box["y"] * canvas_h)
    pw = int(product_box["width"] * canvas_w)
    ph = int(product_box["height"] * canvas_h)

    orig_w, orig_h = product_fg.size
    scale = min(pw / orig_w, ph / orig_h)
    new_w, new_h = max(1, int(orig_w * scale)), max(1, int(orig_h * scale))

    fg_resized = product_fg.resize((new_w, new_h), Image.LANCZOS)
    mask_resized = product_mask.resize((new_w, new_h), Image.LANCZOS)

    offset_x = px + (pw - new_w) // 2
    offset_y = py + (ph - new_h) // 2

    placed_fg = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    placed_mask = Image.new("L", canvas_size, 0)
    placed_fg.paste(fg_resized, (offset_x, offset_y), fg_resized)
    placed_mask.paste(mask_resized, (offset_x, offset_y))

    bbox = (offset_x, offset_y, offset_x + new_w, offset_y + new_h)
    return placed_fg, placed_mask, bbox


def _build_zone_masks(
    placed_mask: Image.Image, core_erode_px: int, edge_dilate_px: int
) -> tuple[Image.Image, Image.Image]:
    core_mask = placed_mask.filter(ImageFilter.MinFilter(core_erode_px * 2 + 1))
    outer_mask = placed_mask.filter(ImageFilter.MaxFilter(edge_dilate_px * 2 + 1))
    return core_mask, outer_mask


def _build_environment_edit_mask(outer_mask: Image.Image) -> Image.Image:
    outer_arr = np.array(outer_mask)
    h, w = outer_arr.shape
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = outer_arr
    return Image.fromarray(rgba, "RGBA")


def generate_protected_scene(
    product_fg_path: str,
    product_mask_path: str,
    canvas_size: tuple[int, int],
    product_box: dict,
    scene_prompt: str,
    output_path: str,
    core_erode_px: int = 12,
    edge_dilate_px: int = 30,
    feather_px: int = 8,
    size: str = "1024x1024",
) -> tuple[str, tuple[int, int, int, int]]:

    product_fg = Image.open(product_fg_path).convert("RGBA")
    product_mask = Image.open(product_mask_path).convert("L")

    placed_fg, placed_mask, bbox = _letterbox_place(product_fg, product_mask, canvas_size, product_box)
    core_mask, outer_mask = _build_zone_masks(placed_mask, core_erode_px, edge_dilate_px)

    canvas = Image.new("RGBA", canvas_size, (235, 235, 235, 255))
    canvas.alpha_composite(placed_fg)
    canvas_rgb = canvas.convert("RGB")

    canvas_path = output_path + ".input_canvas.png"
    canvas_rgb.save(canvas_path)

    edit_mask = _build_environment_edit_mask(outer_mask)
    mask_path = output_path + ".edit_mask.png"
    edit_mask.save(mask_path)

    edited_bytes = edit_image_region(canvas_path, mask_path, scene_prompt, size=size)
    generated = Image.open(BytesIO(edited_bytes)).convert("RGB").resize(canvas_size, Image.LANCZOS)

    generated_arr = np.array(generated, dtype=np.float32)
    original_arr = np.array(canvas_rgb, dtype=np.float32)

    restore_strength = np.array(
        outer_mask.filter(ImageFilter.GaussianBlur(feather_px)), dtype=np.float32
    ) / 255.0

    core_strength = np.array(core_mask, dtype=np.float32) / 255.0
    restore_strength = np.maximum(restore_strength, core_strength)

    blended = (
        original_arr * restore_strength[..., None]
        + generated_arr * (1.0 - restore_strength[..., None])
    )
    result = Image.fromarray(np.clip(blended, 0, 255).astype(np.uint8), "RGB")
    result.save(output_path)

    return output_path, bbox
