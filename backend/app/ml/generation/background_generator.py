# 배경 생성 + 검증 + 재시도 로직.
from io import BytesIO
from typing import Callable

from PIL import Image

from app.ml.image_clients.gpt_image_client import generate_image, edit_image_region
from app.ml.planning.product_analysis_gpt import analyze_background_objects
from app.ml.compositing.mask_utils import build_edit_mask


def _crop_to_aspect(image: Image.Image, target_w: int, target_h: int) -> Image.Image:
    target_ratio = target_w / target_h
    src_w, src_h = image.size
    src_ratio = src_w / src_h
    if abs(src_ratio - target_ratio) < 1e-3:
        return image
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        return image.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        return image.crop((0, top, src_w, top + new_h))


def gen_size_for(output_w: int, output_h: int) -> str:
    if output_w == output_h:
        return "1024x1024"
    if output_h > output_w:
        return "1024x1536"
    return "1536x1024"


def _generate_background(prompt: str, output_w: int, output_h: int) -> tuple[Image.Image, str]:
    gen_size = gen_size_for(output_w, output_h)
    bg_bytes = generate_image(prompt, size=gen_size)
    cropped = _crop_to_aspect(Image.open(BytesIO(bg_bytes)), output_w, output_h)
    return cropped, gen_size


def generate_verified_background(
    prompt: str,
    output_w: int,
    output_h: int,
    save_path,
    product_category: str,
    debug_dir,
    max_full_regenerations: int = 2,
    max_inpaint_attempts: int = 3,
    on_warning: Callable[[str], None] = print,
    on_success: Callable[[str], None] = print,
) -> tuple[Image.Image, list[dict]]:

    debug_dir.mkdir(parents=True, exist_ok=True)

    current_prompt = prompt
    detected_labels: list[str] = []
    analysis = None
    bg_img = None

    for regen_attempt in range(1, max_full_regenerations + 1):
        bg_img, _ = _generate_background(current_prompt, output_w, output_h)
        bg_img.save(save_path)
        bg_img.save(debug_dir / f"regen_{regen_attempt}.png")

        analysis = analyze_background_objects(str(save_path), product_category)
        if not analysis.contains_forbidden_object:
            if regen_attempt > 1:
                on_success(f"{regen_attempt}번째 전체 재생성에서 깨끗한 배경 확보")
            return bg_img, [obj.model_dump() for obj in analysis.objects]

        detected_labels.append(analysis.detected_object_description)
        on_warning(
            f"⚠️ 배경에 상품과 혼동될 물체 발견 (전체 재생성 {regen_attempt}회차): "
            f"{analysis.detected_object_description}"
        )

        forbidden_objects = [o for o in analysis.objects if o.same_domain_as_product]
        for inpaint_attempt in range(1, max_inpaint_attempts + 1):
            if not forbidden_objects:
                break
            target = forbidden_objects[0]
            on_warning(f"　→ 국소 인페인팅으로 제거 시도 ({inpaint_attempt}/{max_inpaint_attempts}): {target.label}")

            mask = build_edit_mask(bg_img.size, target.bbox)
            mask_path = debug_dir / f"mask_{regen_attempt}_{inpaint_attempt}.png"
            mask.save(mask_path)

            gen_size = gen_size_for(output_w, output_h)
            edited_bytes = edit_image_region(
                str(save_path), str(mask_path),
                f"remove the {target.label} completely and fill this area naturally "
                f"with the surrounding scene, matching its color and texture",
                size=gen_size,
            )
            bg_img = Image.open(BytesIO(edited_bytes)).resize((output_w, output_h), Image.LANCZOS)
            bg_img.save(save_path)
            bg_img.save(debug_dir / f"regen_{regen_attempt}_inpaint_{inpaint_attempt}.png")

            analysis = analyze_background_objects(str(save_path), product_category)
            if not analysis.contains_forbidden_object:
                on_success(
                    f"국소 인페인팅으로 깨끗한 배경 확보 "
                    f"(전체 재생성 {regen_attempt}회차, 인페인팅 {inpaint_attempt}회차)"
                )
                return bg_img, [obj.model_dump() for obj in analysis.objects]

            detected_labels.append(analysis.detected_object_description)
            forbidden_objects = [o for o in analysis.objects if o.same_domain_as_product]

        if regen_attempt < max_full_regenerations:
            forbidden_list = "; ".join(dict.fromkeys(detected_labels))  # 중복 제거, 순서 유지
            current_prompt = (
                prompt
                + f" CRITICAL: the scene must be completely empty, absolutely no "
                  f"product-like objects of any kind. Specifically do NOT include "
                  f"anything resembling: {forbidden_list}."
            )

    on_warning(
        f"⚠️ 전체 재생성 {max_full_regenerations}회 + 국소 인페인팅으로도 완전히 못 지웠어요: "
        f"{analysis.detected_object_description if analysis else ''} — 이번 결과 그대로 진행해요"
    )
    return bg_img, [obj.model_dump() for obj in analysis.objects]
