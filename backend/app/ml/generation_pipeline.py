from app.ml.clients.factory import create_text_model_client
from app.ml.prompt_generator import generate_image_prompt


CONCEPTS = {
    "A": "제품 중심형: 제품의 형태, 소재, 기능적 특징을 강하게 강조",
    "B": "라이프스타일형: 고객이 제품을 실제로 사용하는 자연스러운 일상 장면을 강조",
    "C": "캠페인형: 광고 슬로건과 브랜드 메시지가 강하게 느껴지는 상징적인 비주얼을 강조",
}


def generate_drafts(
    product_name: str,
    product_description: str | None,
    product_image_path: str | None,
    platform: str,
    style: str | None,
    selected_slogan: str,
) -> list[dict]:
    client = create_text_model_client()

    drafts = []

    for draft_id, concept in CONCEPTS.items():
        image_prompt = generate_image_prompt(
            client=client,
            product_name=product_name,
            product_description=product_description,
            platform=platform,
            style=style,
            selected_slogan=selected_slogan,
            concept=concept,
        )

        drafts.append(
            {
                "id": draft_id,
                "title": f"시안 {draft_id}",
                "version": 1,
                "image_path": None,
                "image_prompt": image_prompt,
            }
        )

    return drafts