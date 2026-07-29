from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from uuid import uuid4

from app.ml.clients.factory import create_text_model_client
from app.ml.post_copy_generator import generate_post_copy

from app.ml.segmentation.cache import get_or_create_foreground
from app.ml.planning.product_analysis_gpt import create_creative_brief, CREATIVE_ANGLES
from app.ml.planning.text_placement import apply_text_placement
from app.ml.image_clients.gpt_image_client import generate_transparent_prop
from app.ml.generation.background_generator import generate_verified_background
from app.ml.compositing.layered_composite import composite_full_scene
from app.ml.compositing.lighting_estimator import estimate_lighting
from app.ml.rendering.text_layer_renderer import render_text_layer


CONCEPTS = {
    "A": "제품 중심형: 제품의 형태, 소재, 기능적 특징을 강하게 강조",
    "B": "라이프스타일형: 고객이 제품을 실제로 사용하는 자연스러운 일상 장면을 강조",
    "C": "캠페인형: 광고 슬로건과 브랜드 메시지가 강하게 느껴지는 상징적인 비주얼을 강조",
}


CONCEPT_CREATIVE_MAPPING = {
    "A": {"creative_angle": CREATIVE_ANGLES[1], "scene_type": "studio"},
    "B": {"creative_angle": None, "scene_type": "kitchen_or_cafe_lifestyle"},
    "C": {"creative_angle": CREATIVE_ANGLES[6], "scene_type": None},
}

GENERATED_IMAGE_DIR = Path("storage/generated")


def generate_drafts(
    product_name: str,
    product_description: str | None,
    product_image_path: str | None,
    platform: str,
    style: str | None,
    selected_slogan: str,
    image_width: int,
    image_height: int,
    ad_goal: str | None = None,
    price: str | None = None,
    image_improvement_rules: list[str] | None = None,
) -> list[dict]:
    if not product_image_path:
        raise ValueError(
            "새 파이프라인은 상품 세그멘테이션이 필수라 product_image_path가 반드시 있어야 합니다."
        )

    GENERATED_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    text_client = create_text_model_client()

    fg_path, mask_path = get_or_create_foreground(product_image_path)

    def process_concept(draft_id: str, concept: str) -> dict:
        run_id = uuid4().hex
        mapping = CONCEPT_CREATIVE_MAPPING.get(draft_id, {"creative_angle": None, "scene_type": None})

        brief = create_creative_brief(
            product_image_path,
            product_name=product_name,
            product_description=product_description or "",
            ad_goal=ad_goal or "신상품 홍보",
            style=style or "모던",
            price=price,
            platform=platform,
            selected_slogan=selected_slogan,
            creative_angle=mapping["creative_angle"],
            scene_type=mapping["scene_type"],
        )

        product_category = brief.get("product_visual_analysis", {}).get("category", product_name)

        background_prompt = brief["background_prompt"]
        if image_improvement_rules:
            rules_text = "\n".join(f"- {rule}" for rule in image_improvement_rules)
            background_prompt = f"""{background_prompt}

{rules_text}"""

        bg_path = GENERATED_IMAGE_DIR / f"{run_id}_background.png"
        bg_img, background_objects = generate_verified_background(
            background_prompt, image_width, image_height, bg_path, product_category,
            debug_dir=GENERATED_IMAGE_DIR / "background_attempts" / run_id,
        )

        decoration_paths: dict[str, str] = {}
        valid_decorations = [
            deco for deco in brief.get("decorations", [])
            if isinstance(deco, dict) and "id" in deco and "prompt" in deco
        ]
        for deco in valid_decorations:
            prop_bytes = generate_transparent_prop(deco["prompt"])
            prop_path = GENERATED_IMAGE_DIR / f"{run_id}_prop_{deco['id']}.png"
            prop_path.write_bytes(prop_bytes)
            decoration_paths[deco["id"]] = str(prop_path)

        lighting = estimate_lighting(str(bg_path))

        ad_state = {
            **brief,
            "background_prompt": background_prompt,
            "decorations": valid_decorations,
            "background_path": str(bg_path),
            "background_objects": background_objects,
            "product_fg_path": fg_path,
            "product_mask_path": mask_path,
            "excluded_decoration_ids": [],
            "effective_light_direction": lighting["estimated_light_direction"],
        }

        apply_text_placement(ad_state)

        photo_path = str(GENERATED_IMAGE_DIR / f"{run_id}_composite.png")
        composite_full_scene(
            background_path=ad_state["background_path"],
            product_fg_path=ad_state["product_fg_path"],
            product_mask_path=ad_state["product_mask_path"],
            product_box=ad_state["product_box"],
            light_direction=ad_state["effective_light_direction"],
            decorations=ad_state["decorations"],
            decoration_image_paths=decoration_paths,
            output_path=photo_path,
            surfaces=ad_state.get("surfaces", []),
            protected_regions=ad_state.get("protected_regions", []),
            excluded_decoration_ids=set(),
            needs_contact_shadow=ad_state["product_visual_analysis"]["needs_contact_shadow"],
        )

        final_path = GENERATED_IMAGE_DIR / f"{run_id}_final.png"
        render_text_layer(
            background_image_path=photo_path,
            brief=ad_state,
            output_path=str(final_path),
            canvas_size=(image_width, image_height),
        )

        post_copy = generate_post_copy(
            client=text_client,
            product_name=product_name,
            product_description=product_description,
            platform=platform,
            selected_slogan=selected_slogan,
            concept=CONCEPTS.get(draft_id, concept),
        )

        return {
            "id": draft_id,
            "title": f"시안 {draft_id}",
            "version": 1,
            "image_path": str(final_path),
            "image_prompt": ad_state.get("background_prompt", ""),
            "post_copy": post_copy,
        }

    results: dict[str, dict] = {}

    with ThreadPoolExecutor(max_workers=len(CONCEPTS)) as executor:
        futures = {
            executor.submit(process_concept, draft_id, concept): draft_id
            for draft_id, concept in CONCEPTS.items()
        }
        for future in as_completed(futures):
            draft_id = futures[future]
            results[draft_id] = future.result()

    return [results[draft_id] for draft_id in CONCEPTS if draft_id in results]