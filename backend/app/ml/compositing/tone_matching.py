import numpy as np
from PIL import Image


def _rgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    rgb_norm = rgb.astype(np.float32) / 255.0
    mask = rgb_norm > 0.04045
    rgb_linear = np.where(mask, ((rgb_norm + 0.055) / 1.055) ** 2.4, rgb_norm / 12.92)

    M = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ], dtype=np.float32)
    xyz = rgb_linear @ M.T

    xyz_ref = np.array([0.95047, 1.0, 1.08883], dtype=np.float32)
    xyz_norm = xyz / xyz_ref

    delta = 6 / 29
    f = np.where(xyz_norm > delta**3, np.cbrt(xyz_norm), xyz_norm / (3 * delta**2) + 4 / 29)

    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], axis=-1)


def _lab_to_rgb(lab: np.ndarray) -> np.ndarray:
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200

    delta = 6 / 29
    def finv(t):
        return np.where(t > delta, t**3, 3 * delta**2 * (t - 4 / 29))

    xyz_ref = np.array([0.95047, 1.0, 1.08883], dtype=np.float32)
    xyz = np.stack([finv(fx), finv(fy), finv(fz)], axis=-1) * xyz_ref

    M_inv = np.array([
        [3.2404542, -1.5371385, -0.4985314],
        [-0.9692660, 1.8760108, 0.0415560],
        [0.0556434, -0.2040259, 1.0572252],
    ], dtype=np.float32)
    rgb_linear = xyz @ M_inv.T
    rgb_linear = np.clip(rgb_linear, 0, 1)

    mask = rgb_linear > 0.0031308
    rgb_norm = np.where(mask, 1.055 * (rgb_linear ** (1 / 2.4)) - 0.055, rgb_linear * 12.92)
    return np.clip(rgb_norm * 255, 0, 255)


def match_product_tone_to_scene(
    product_rgba: Image.Image,
    background_rgb: Image.Image,
    product_dest_box: tuple[int, int, int, int],
    strength: float = 0.55,
    l_strength: float | None = None,
    ab_strength: float | None = None,
) -> Image.Image:

    if l_strength is None:
        l_strength = strength
    if ab_strength is None:
        ab_strength = strength * 0.5

    px1, py1, px2, py2 = product_dest_box
    bg_arr = np.array(background_rgb.convert("RGB"))
    h, w = bg_arr.shape[:2]

    margin = int((px2 - px1) * 0.4)
    rx1, ry1 = max(0, px1 - margin), max(0, py1 - margin)
    rx2, ry2 = min(w, px2 + margin), min(h, py2 + margin)
    ref_region = bg_arr[ry1:ry2, rx1:rx2]

    ref_lab = _rgb_to_lab(ref_region)
    ref_mean, ref_std = ref_lab.reshape(-1, 3).mean(0), ref_lab.reshape(-1, 3).std(0) + 1e-6

    product_arr = np.array(product_rgba.convert("RGB"))
    alpha = np.array(product_rgba.getchannel("A"))
    product_lab = _rgb_to_lab(product_arr)

    opaque_mask = alpha > 10
    if opaque_mask.sum() == 0:
        return product_rgba

    src_mean = product_lab[opaque_mask].mean(0)
    src_std = product_lab[opaque_mask].std(0) + 1e-6

    transferred = (product_lab - src_mean) * (ref_std / src_std) + ref_mean

    channel_strength = np.array([l_strength, ab_strength, ab_strength], dtype=np.float32)
    blended = product_lab * (1 - channel_strength) + transferred * channel_strength

    result_rgb = _lab_to_rgb(blended).astype(np.uint8)
    result = Image.fromarray(result_rgb, "RGB").convert("RGBA")
    result.putalpha(product_rgba.getchannel("A"))
    return result
