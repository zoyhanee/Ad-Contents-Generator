# 배경 이미지를 분석해 실제 광원 방향/색온도/세기를 추정
import numpy as np
from PIL import Image


def estimate_lighting(background_path: str) -> dict:
    img = Image.open(background_path).convert("RGB")
    arr = np.array(img).astype(np.float32)
    h, w = arr.shape[:2]
    luminance = arr.mean(axis=2)

    def region_mean(y0: float, y1: float, x0: float, x1: float) -> float:
        return float(luminance[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)].mean())

    # 방향 후보 영역의 평균 밝기를 비교해서, 가장 밝은 쪽을 광원 방향으로 추정
    # (빛이 오는 쪽이 카메라에서 더 밝게 찍히는 경향을 이용한 단순 근사치)
    regions = {
        "upper_left": region_mean(0.0, 0.5, 0.0, 0.5),
        "upper_right": region_mean(0.0, 0.5, 0.5, 1.0),
        "left": region_mean(0.25, 0.75, 0.0, 0.4),
        "right": region_mean(0.25, 0.75, 0.6, 1.0),
        "front": region_mean(0.6, 1.0, 0.3, 0.7),
    }
    estimated_direction = max(regions, key=regions.get)

    r_mean, g_mean, b_mean = float(arr[..., 0].mean()), float(arr[..., 1].mean()), float(arr[..., 2].mean())
    warmth = r_mean - b_mean
    if warmth > 8:
        temperature = "warm"
    elif warmth < -8:
        temperature = "cool"
    else:
        temperature = "neutral"

    # 광량(대비): 밝기의 표준편차. 낮으면 은은하고 평평한 조명, 높으면 명암이 강한 조명.
    contrast = float(luminance.std())
    if contrast > 45:
        strength = "strong"
    elif contrast < 20:
        strength = "soft"
    else:
        strength = "moderate"

    return {
        "estimated_light_direction": estimated_direction,
        "estimated_color_temperature": temperature,
        "estimated_strength": strength,
        "contrast_std": contrast,
        "region_brightness": regions,
        "mean_rgb": [r_mean, g_mean, b_mean],
    }
