from __future__ import annotations

import base64
import json
import logging
import math
import mimetypes
import os
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
from PIL import Image, ImageFilter, ImageStat
from app.core.config import settings


logger = logging.getLogger("uvicorn.error")


PLATFORM_RULES = {
    "instagram": {
        "label": "인스타그램",
        "min_length": 10,
        "max_length": 100,
        "recommended_hashtags": (1, 3),
        # 음식에만 치우치지 않도록 범용적인 인스타그램 표현으로 구성합니다.
        "keywords": ["감성", "일상", "취향", "스타일", "특별", "경험", "공유"],
    },
    "baemin": {
        "label": "배달의민족",
        "min_length": 10,
        "max_length": 90,
        "recommended_hashtags": (0, 1),
        "keywords": ["주문", "배달", "지금", "혜택", "할인", "선택", "간편"],
    },
    "naver": {
        "label": "네이버",
        "min_length": 15,
        "max_length": 130,
        "recommended_hashtags": (0, 2),
        "keywords": ["추천", "정보", "가격", "특징", "구성", "사용", "후기"],
    },
    "offline": {
        "label": "오프라인 포스터",
        "min_length": 5,
        "max_length": 55,
        "recommended_hashtags": (0, 0),
        "keywords": ["지금", "오늘", "특별", "할인", "신제품", "오픈", "한정"],
    },
}

GOAL_KEYWORDS = {
    "awareness": {
        "strong": [
            "브랜드", "기억", "발견", "주목", "눈길",
            "인상", "떠올", "사로잡", "대표", "눈여겨보세요",
        ],
        "weak": [
            "새로운", "특별한", "관심", "궁금",
            "느껴보세요", "만나보세요", 
        ],
    },
    "sales": {
        "strong": [
            "구매", "주문", "선택", "결제", "장바구니",
            "놓치지", "할인", "혜택",
        ],
        "weak": [
            "지금", "경험", "즐겨보세요",
            "만나보세요", "확인해보세요",
        ],
    },
    "traffic": {
        "strong": [
            "방문", "매장", "예약", "상담",
            "찾아오세요", "들러", "오시는 길",
        ],
        "weak": [
            "체험", "확인해보세요", "구경해보세요",
            "만나보세요",
        ],
    },
    "promotion": {
        "strong": [
            "이벤트", "프로모션", "기간", "한정",
            "증정", "특가", "쿠폰", "할인", "혜택",
        ],
        "weak": [
            "지금", "기회", "놓치지",
            "확인해보세요",
        ],
    },
}

STYLE_KEYWORDS = {
    "warm": ["따뜻", "포근", "정성", "마음", "편안", "부드러"],
    "modern": ["모던", "깔끔", "미니멀", "세련", "감각적"],
    "vivid": ["생생", "강렬", "톡톡", "선명", "활기", "산뜻"],
    "premium": ["프리미엄", "고급", "품격", "특별", "정교", "엄선"],
}

BANNED_OR_RISKY_EXPRESSIONS = [
    "무조건",
    "100%",
    "최고",
    "완벽",
    "절대",
    "기적",
    "즉시 효과",
    "업계 1위",
]

KOREAN_STOPWORDS = {
    "그리고", "하지만", "또한", "에서", "으로", "에게", "하는", "있는",
    "없는", "입니다", "합니다", "하세요", "지금", "오늘", "우리", "당신",
    "위한", "통해", "제품", "상품", "사용", "제공", "더한", "담은",
}

# 형태소 분석기를 추가하지 않고도 기본적인 조사·어미 차이를 완화하기 위한 목록입니다.
KOREAN_PARTICLES = (
    "으로부터", "에게서", "에서는", "으로는", "까지는", "부터는",
    "에게", "에서", "으로", "까지", "부터", "처럼", "보다",
    "은", "는", "이", "가", "을", "를", "에", "의", "와", "과",
    "로", "도", "만", "께", "랑", "이나", "나",
)

KOREAN_ENDINGS = (
    "합니다", "하세요", "됩니다", "있는", "없는", "하는", "되는",
    "스럽게", "스럽고", "적인", "하게", "하고", "하며", "해서",
    "드립니다", "드리는", "느껴지는", "보이는", "채우는", "더하는",
)


@dataclass
class SloganEvaluation:
    product_reflection: float
    platform_fit: float
    goal_reflection: float
    style_reflection: float
    naturalness: float
    advertising_appeal: float
    originality: float
    final_score: float
    details: dict


@dataclass
class LLMImageEvaluation:
    product_visibility: float
    product_fidelity: float
    prompt_alignment: float
    platform_fit: float
    style_alignment: float
    slogan_consistency: float
    text_quality: float
    advertising_appeal: float
    overall_score: float
    feedback: str
    details: dict


@dataclass
class ImageEvaluation:
    resolution_score: float
    aspect_ratio_score: float
    sharpness_score: float
    brightness_score: float
    contrast_score: float
    technical_quality_score: float
    prompt_similarity_score: Optional[float]
    llm_visual_score: Optional[float]
    llm_feedback: Optional[str]
    final_score: float
    details: dict


@dataclass
class IntegratedEvaluation:
    slogan_score: float
    image_score: float
    consistency_score: float
    final_score: float
    details: dict


def _clamp(value: float, low: float = 0.0, high: float = 5.0) -> float:
    return round(max(low, min(high, value)), 2)


def _normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def _strip_korean_affixes(token: str) -> str:
    """간단한 조사와 일부 어미를 제거해 문자열 일치의 과도한 엄격함을 줄입니다."""
    cleaned = _normalize_text(token)

    for ending in sorted(KOREAN_ENDINGS, key=len, reverse=True):
        if cleaned.endswith(ending) and len(cleaned) - len(ending) >= 2:
            cleaned = cleaned[:-len(ending)]
            break

    for particle in sorted(KOREAN_PARTICLES, key=len, reverse=True):
        if cleaned.endswith(particle) and len(cleaned) - len(particle) >= 2:
            cleaned = cleaned[:-len(particle)]
            break

    return cleaned


def _tokenize_korean(text: str) -> list[str]:
    raw_tokens = re.findall(r"[가-힣A-Za-z0-9]+", _normalize_text(text))
    tokens: list[str] = []

    for raw_token in raw_tokens:
        if raw_token in KOREAN_STOPWORDS:
            continue

        token = _strip_korean_affixes(raw_token)
        if len(token) >= 2 and token not in KOREAN_STOPWORDS:
            tokens.append(token)

    return tokens


def _keyword_is_reflected(keyword: str, normalized_text: str) -> bool:
    """정확 일치와 기본적인 어절 변형을 함께 인정합니다."""
    normalized_keyword = _normalize_text(keyword)
    if not normalized_keyword:
        return False

    if normalized_keyword in normalized_text:
        return True

    stripped_keyword = _strip_korean_affixes(normalized_keyword)
    if len(stripped_keyword) >= 2 and stripped_keyword in normalized_text:
        return True

    # 긴 단어는 일부 활용형 차이가 있어도 공통 앞부분이 충분하면 반영으로 인정합니다.
    if len(stripped_keyword) >= 4:
        stem = stripped_keyword[: max(3, len(stripped_keyword) - 1)]
        if stem in normalized_text:
            return True

    return False


def _keyword_match_score(text: str, keywords: Iterable[str]) -> tuple[float, list[str]]:
    normalized = _normalize_text(text)
    keyword_list = [k for k in keywords if k]
    matched = [k for k in keyword_list if _keyword_is_reflected(k, normalized)]

    if not keyword_list:
        return 3.0, matched

    ratio = len(matched) / len(keyword_list)
    score = 1.0 + min(4.0, ratio * 6.0)
    return _clamp(score), matched


def _goal_reflection_score(
    text: str,
    goal: str,
) -> tuple[float, list[str]]:
    """
    광고 목표를 강한 표현과 약한 표현으로 나누어 평가합니다.

    - 강한 표현 2개 이상: 5점
    - 강한 표현 1개: 4.5점
    - 약한 표현 2개 이상: 4점
    - 약한 표현 1개: 3점
    - 일치 없음: 1점
    - 정의되지 않은 목표: 3점
    """
    normalized = _normalize_text(text)
    rules = GOAL_KEYWORDS.get(goal)

    if not rules:
        return 3.0, []

    strong_matches = [
        keyword
        for keyword in rules.get("strong", [])
        if _keyword_is_reflected(keyword, normalized)
    ]

    weak_matches = [
        keyword
        for keyword in rules.get("weak", [])
        if _keyword_is_reflected(keyword, normalized)
    ]

    matched = strong_matches + weak_matches

    if len(strong_matches) >= 2:
        score = 5.0
    elif len(strong_matches) == 1:
        score = 4.5
    elif len(weak_matches) >= 2:
        score = 4.0
    elif len(weak_matches) == 1:
        score = 3.0
    else:
        score = 1.0

    return _clamp(score), matched


def _keyword_presence_score(
    text: str,
    keywords: Iterable[str],
) -> tuple[float, list[str]]:
    """
    스타일처럼 대표 표현 하나만 자연스럽게 포함돼도
    충분히 반영된 항목을 평가합니다.
    """
    normalized = _normalize_text(text)
    keyword_list = [keyword for keyword in keywords if keyword]
    matched = [
        keyword
        for keyword in keyword_list
        if _keyword_is_reflected(keyword, normalized)
    ]

    if not keyword_list:
        return 3.0, matched
    if len(matched) == 0:
        score = 1.0
    elif len(matched) == 1:
        score = 4.0
    else:
        score = 5.0

    return _clamp(score), matched


def _length_score(length: int, min_length: int, max_length: int) -> float:
    if min_length <= length <= max_length:
        return 5.0

    if length < min_length:
        ratio = length / max(min_length, 1)
        return _clamp(1.0 + 4.0 * ratio)

    overflow_ratio = (length - max_length) / max(max_length, 1)
    return _clamp(5.0 - overflow_ratio * 8.0)


def _jaccard_similarity(text_a: str, text_b: str) -> float:
    set_a = set(_tokenize_korean(text_a))
    set_b = set(_tokenize_korean(text_b))

    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0

    return len(set_a & set_b) / len(set_a | set_b)


def evaluate_slogan(
    slogan: str,
    *,
    product_name: str,
    product_description: str = "",
    platform: str,
    goal: str,
    style: str,
    previous_slogans: Optional[list[str]] = None,
) -> SloganEvaluation:
    """
    슬로건을 1~5점 척도로 평가하고 최종 점수를 100점으로 반환합니다.
    """
    previous_slogans = previous_slogans or []
    normalized = _normalize_text(slogan)
    platform_rule = PLATFORM_RULES.get(platform, PLATFORM_RULES["instagram"])

    # 상품명 포함 여부와 상품 특징 반영도를 분리합니다.
    # 상품명이 없다는 이유만으로 상품 반영도를 1점으로 고정하지 않습니다.
    normalized_product_name = _normalize_text(product_name)
    product_name_included = bool(normalized_product_name) and (
        normalized_product_name in normalized
    )

    name_keywords = _tokenize_korean(product_name)
    description_keywords = _tokenize_korean(product_description)
    product_keywords = list(dict.fromkeys(name_keywords + description_keywords))[:8]
    matched_product_keywords = [
        keyword
        for keyword in product_keywords
        if _keyword_is_reflected(keyword, normalized)
    ]

    matched_count = len(matched_product_keywords)

    if not product_keywords:
        # 설명이 없을 때는 상품명 포함 여부만으로 과도한 고득점을 주지 않습니다.
        product_score = 2.0 if product_name_included else 1.0
    elif product_name_included and matched_count >= 3:
        product_score = 5.0
    elif matched_count >= 3:
        product_score = 4.0
    elif matched_count == 2:
        product_score = 3.0
    elif matched_count == 1:
        product_score = 2.0
    elif product_name_included:
        product_score = 2.0
    else:
        product_score = 1.0

    length_score = _length_score(
        len(slogan),
        platform_rule["min_length"],
        platform_rule["max_length"],
    )

    hashtag_count = len(re.findall(r"#\w+", slogan))
    min_hashtag, max_hashtag = platform_rule["recommended_hashtags"]

    if min_hashtag <= hashtag_count <= max_hashtag:
        hashtag_score = 5.0
    elif hashtag_count > max_hashtag:
        hashtag_score = _clamp(5.0 - (hashtag_count - max_hashtag) * 1.5)
    else:
        hashtag_score = _clamp(3.0 + hashtag_count)

    platform_keyword_score, matched_platform_keywords = _keyword_match_score(
        normalized,
        platform_rule["keywords"],
    )

    platform_fit = _clamp(
        length_score * 0.45
        + hashtag_score * 0.20
        + platform_keyword_score * 0.35
    )

    goal_score, matched_goal_keywords = _goal_reflection_score(
        normalized,
        goal,
    )

    style_score, matched_style_keywords = _keyword_presence_score(
        normalized,
        STYLE_KEYWORDS.get(style, []),
    )

    risky_matches = [
        expression
        for expression in BANNED_OR_RISKY_EXPRESSIONS
        if expression.lower() in normalized
    ]

    sentence_count = len([s for s in re.split(r"[.!?]+", slogan) if s.strip()])
    special_char_ratio = len(re.findall(r"[^가-힣A-Za-z0-9\s#,.!?]", slogan)) / max(
        len(slogan), 1
    )

    naturalness = 5.0
    if sentence_count > 3:
        naturalness -= min(2.0, (sentence_count - 3) * 0.5)
    if special_char_ratio > 0.10:
        naturalness -= 1.0
    if len(slogan.strip()) < 5:
        naturalness -= 2.0
    naturalness = _clamp(naturalness)

    call_to_action_keywords = [
        "주문", "구매", "방문", "만나보세요", "확인", "즐겨보세요",
        "놓치지", "지금", "경험", "선택", "사용해보세요", "시작해보세요",
    ]
    cta_matches = [k for k in call_to_action_keywords if k in normalized]

    appeal = 3.0
    appeal += min(1.0, len(cta_matches) * 0.4)
    appeal += min(0.7, len(matched_product_keywords) * 0.2)
    appeal -= min(1.5, len(risky_matches) * 0.5)
    advertising_appeal = _clamp(appeal)

    tokens = _tokenize_korean(slogan)
    counts = Counter(tokens)
    repeated_token_count = sum(1 for count in counts.values() if count >= 2)

    max_previous_similarity = 0.0
    if previous_slogans:
        max_previous_similarity = max(
            _jaccard_similarity(slogan, old)
            for old in previous_slogans
        )

    originality = 5.0
    originality -= min(1.5, repeated_token_count * 0.4)
    originality -= min(3.0, max_previous_similarity * 3.0)
    originality = _clamp(originality)

    weighted_five_point_score = (
        product_score * 0.20
        + platform_fit * 0.20
        + goal_score * 0.15
        + style_score * 0.15
        + naturalness * 0.10
        + advertising_appeal * 0.10
        + originality * 0.10
    )

    final_score = round(weighted_five_point_score * 20, 2)

    return SloganEvaluation(
        product_reflection=product_score,
        platform_fit=platform_fit,
        goal_reflection=goal_score,
        style_reflection=style_score,
        naturalness=naturalness,
        advertising_appeal=advertising_appeal,
        originality=originality,
        final_score=final_score,
        details={
            "product_name_included": product_name_included,
            "product_keywords": product_keywords,
            "matched_product_keywords": matched_product_keywords,
            "matched_product_keyword_count": matched_count,
            "matched_platform_keywords": matched_platform_keywords,
            "matched_goal_keywords": matched_goal_keywords,
            "matched_style_keywords": matched_style_keywords,
            "risky_expressions": risky_matches,
            "hashtag_count": hashtag_count,
            "length": len(slogan),
            "sentence_count": sentence_count,
            "max_previous_similarity": round(max_previous_similarity, 3),
            "repeated_tokens": [
                token for token, count in counts.items() if count >= 2
            ],
        },
    )


def _score_resolution(width: int, height: int) -> float:
    min_side = min(width, height)

    if min_side >= 1024:
        return 5.0
    if min_side >= 768:
        return 4.5
    if min_side >= 512:
        return 4.0
    if min_side >= 384:
        return 3.0
    if min_side >= 256:
        return 2.0
    return 1.0


def _score_aspect_ratio(width: int, height: int, platform: str) -> tuple[float, float]:
    ratio = width / max(height, 1)

    target_ratios = {
        "instagram": [1.0, 0.8, 1.91],
        "baemin": [1.0, 1.33],
        "naver": [1.0, 1.5, 1.91],
        "offline": [0.707, 1.414],
    }

    targets = target_ratios.get(platform, [1.0])
    distance = min(abs(math.log(ratio / target)) for target in targets)

    score = 5.0 - distance * 6.0
    return _clamp(score), round(ratio, 3)


def _sharpness_measure(image: Image.Image) -> float:
    gray = image.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    return float(ImageStat.Stat(edges).var[0])


def _sharpness_score(measure: float) -> float:
    if measure >= 1800:
        return 5.0
    if measure >= 1000:
        return 4.5
    if measure >= 500:
        return 4.0
    if measure >= 250:
        return 3.0
    if measure >= 100:
        return 2.0
    return 1.0


def _brightness_score(mean_brightness: float) -> float:
    # 지나치게 어둡거나 밝은 이미지를 감점
    ideal = 135.0
    distance = abs(mean_brightness - ideal)
    return _clamp(5.0 - distance / 35.0)


def _contrast_score(std_brightness: float) -> float:
    if 45 <= std_brightness <= 85:
        return 5.0
    if 30 <= std_brightness < 45 or 85 < std_brightness <= 100:
        return 4.0
    if 20 <= std_brightness < 30 or 100 < std_brightness <= 115:
        return 3.0
    return 2.0


def _clip_similarity(
    image: Image.Image,
    prompt: str,
    *,
    model_name: str = "openai/clip-vit-base-patch32",
) -> Optional[float]:
    """
    transformers와 torch가 설치되어 있고 모델을 다운로드할 수 있을 때만 실행됩니다.
    결과는 1~5점입니다.
    """
    try:
        import torch
        from transformers import CLIPModel, CLIPProcessor
    except ImportError:
        return None

    try:
        processor = CLIPProcessor.from_pretrained(model_name)
        model = CLIPModel.from_pretrained(model_name)
        model.eval()

        inputs = processor(
            text=[prompt],
            images=[image.convert("RGB")],
            return_tensors="pt",
            padding=True,
        )

        with torch.no_grad():
            outputs = model(**inputs)
            similarity = torch.cosine_similarity(
                outputs.image_embeds,
                outputs.text_embeds,
            ).item()

        # CLIP cosine similarity를 프로젝트용 1~5 점수로 변환
        score = 1.0 + max(0.0, min(1.0, (similarity - 0.15) / 0.25)) * 4.0
        return _clamp(score)

    except Exception:
        return None


def _encode_image_as_data_url(image_path: str | Path) -> str:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {path}")

    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def _parse_json_response(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def evaluate_image_with_llm(
    *,
    image_path: str | Path,
    product_name: str = "",
    product_description: str = "",
    platform: str = "",
    goal: str = "",
    style: str = "",
    slogan: str = "",
    image_prompt: str = "",
    model: str | None = None,
) -> LLMImageEvaluation:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "LLM 이미지 평가를 사용하려면 openai 패키지가 필요합니다."
        ) from exc

    api_key = settings.OPENAI_API_KEY

    if not api_key:
        raise RuntimeError(
            "LLM 이미지 평가를 사용하려면 OPENAI_API_KEY가 필요합니다."
        )

    client = OpenAI(api_key=api_key)

    model_name = (
        model
        or getattr(settings, "IMAGE_EVAL_MODEL", None)
        or "gpt-5-mini"
    )
    image_data_url = _encode_image_as_data_url(image_path)

    evaluation_prompt = f"""
당신은 광고 이미지 품질 평가자입니다.
첨부된 이미지에서 직접 확인할 수 있는 내용만 평가하세요.

[상품 정보]
상품명: {product_name or "미입력"}
상품 설명: {product_description or "미입력"}

[광고 설정]
플랫폼: {platform or "미지정"}
광고 목표: {goal or "미지정"}
스타일: {style or "미지정"}
선택 슬로건: {slogan or "미입력"}

[이미지 생성 프롬프트]
{image_prompt or "미입력"}

[평가 원칙]
- 각 항목은 1점에서 5점 사이로 평가하세요.
- 이미지에서 직접 확인되지 않는 정보는 추측하지 마세요.
- 이미지에 글자가 없다면 text_quality는 5점으로 평가하세요.
- 글자가 있다면 잘림, 깨짐, 오탈자와 가독성을 확인하세요.

다음 JSON 형식만 출력하세요.
{{
  "product_visibility": 1.0,
  "product_fidelity": 1.0,
  "prompt_alignment": 1.0,
  "platform_fit": 1.0,
  "style_alignment": 1.0,
  "slogan_consistency": 1.0,
  "text_quality": 1.0,
  "advertising_appeal": 1.0,
  "feedback": "핵심 장점과 개선점"
}}
""".strip()

    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": evaluation_prompt},
                    {
                        "type": "input_image",
                        "image_url": image_data_url,
                        "detail": "high",
                    },
                ],
            }
        ],
    )

    parsed = _parse_json_response(response.output_text)
    score_names = [
        "product_visibility",
        "product_fidelity",
        "prompt_alignment",
        "platform_fit",
        "style_alignment",
        "slogan_consistency",
        "text_quality",
        "advertising_appeal",
    ]
    scores = {
        name: _clamp(float(parsed.get(name, 1.0)), low=1.0, high=5.0)
        for name in score_names
    }

    overall_score = _clamp(
        scores["product_visibility"] * 0.15
        + scores["product_fidelity"] * 0.10
        + scores["prompt_alignment"] * 0.15
        + scores["platform_fit"] * 0.10
        + scores["style_alignment"] * 0.10
        + scores["slogan_consistency"] * 0.10
        + scores["text_quality"] * 0.10
        + scores["advertising_appeal"] * 0.20,
        low=1.0,
        high=5.0,
    )

    return LLMImageEvaluation(
        **scores,
        overall_score=overall_score,
        feedback=str(parsed.get("feedback", "")).strip(),
        details={"model": model_name, "raw_response": parsed},
    )


def evaluate_image(
    image_path: str | Path,
    *,
    platform: str,
    prompt: str = "",
    use_clip: bool = False,
    use_llm: bool = False,
    product_name: str = "",
    product_description: str = "",
    goal: str = "",
    style: str = "",
    slogan: str = "",
    llm_model: str | None = None,
) -> ImageEvaluation:
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    with Image.open(image_path) as opened:
        image = opened.convert("RGB")

    width, height = image.size
    grayscale = image.convert("L")
    stat = ImageStat.Stat(grayscale)
    mean_brightness = float(stat.mean[0])
    std_brightness = float(stat.stddev[0])
    sharpness_measure = _sharpness_measure(image)

    resolution_score = _score_resolution(width, height)
    aspect_ratio_score, actual_ratio = _score_aspect_ratio(
        width,
        height,
        platform,
    )
    sharpness_score = _sharpness_score(sharpness_measure)
    brightness_score = _brightness_score(mean_brightness)
    contrast_score = _contrast_score(std_brightness)

    technical_quality_score = _clamp(
        resolution_score * 0.25
        + aspect_ratio_score * 0.20
        + sharpness_score * 0.25
        + brightness_score * 0.15
        + contrast_score * 0.15
    )

    prompt_similarity_score = None
    if use_clip and prompt.strip():
        prompt_similarity_score = _clip_similarity(image, prompt)

    if prompt_similarity_score is None:
        base_five_point_score = technical_quality_score
    else:
        base_five_point_score = _clamp(
            technical_quality_score * 0.60
            + prompt_similarity_score * 0.40
        )

    llm_result = None
    if use_llm:
        llm_result = evaluate_image_with_llm(
            image_path=image_path,
            product_name=product_name,
            product_description=product_description,
            platform=platform,
            goal=goal,
            style=style,
            slogan=slogan,
            image_prompt=prompt,
            model=llm_model,
        )
        final_five_point_score = _clamp(
            base_five_point_score * 0.40
            + llm_result.overall_score * 0.60
        )
    else:
        final_five_point_score = base_five_point_score

    return ImageEvaluation(
        resolution_score=resolution_score,
        aspect_ratio_score=aspect_ratio_score,
        sharpness_score=sharpness_score,
        brightness_score=brightness_score,
        contrast_score=contrast_score,
        technical_quality_score=technical_quality_score,
        prompt_similarity_score=prompt_similarity_score,
        llm_visual_score=(
            llm_result.overall_score
            if llm_result is not None
            else None
        ),
        llm_feedback=(
            llm_result.feedback
            if llm_result is not None
            else None
        ),
        final_score=round(final_five_point_score * 20, 2),
        details={
            "width": width,
            "height": height,
            "aspect_ratio": actual_ratio,
            "mean_brightness": round(mean_brightness, 2),
            "contrast_std": round(std_brightness, 2),
            "sharpness_measure": round(sharpness_measure, 2),
            "clip_used": prompt_similarity_score is not None,
            "llm_used": llm_result is not None,
            "llm": asdict(llm_result) if llm_result is not None else None,
        },
    )


def calculate_consistency_score(
    slogan: str,
    image_prompt: str,
    *,
    product_name: str,
    style: str,
    goal: str,
) -> tuple[float, dict]:
    """
    슬로건과 이미지 프롬프트의 키워드 일치도를 기반으로
    통합 일관성을 1~5점으로 평가합니다.
    """
    goal_rules = GOAL_KEYWORDS.get(goal, {})
    goal_keywords = (
        goal_rules.get("strong", [])
        + goal_rules.get("weak", [])
    )

    combined_keywords = (
        [product_name]
        + STYLE_KEYWORDS.get(style, [])
        + goal_keywords
    )

    slogan_matches = {
        keyword for keyword in combined_keywords
        if keyword and keyword.lower() in _normalize_text(slogan)
    }
    prompt_matches = {
        keyword for keyword in combined_keywords
        if keyword and keyword.lower() in _normalize_text(image_prompt)
    }

    union = slogan_matches | prompt_matches
    intersection = slogan_matches & prompt_matches

    if not union:
        score = 3.0
    else:
        overlap_ratio = len(intersection) / len(union)
        score = 1.0 + overlap_ratio * 4.0

    if product_name.lower() in _normalize_text(slogan) and product_name.lower() in _normalize_text(image_prompt):
        score += 0.5

    return _clamp(score), {
        "slogan_matches": sorted(slogan_matches),
        "prompt_matches": sorted(prompt_matches),
        "shared_matches": sorted(intersection),
    }


def evaluate_ad_result(
    *,
    slogan: str,
    image_path: str | Path,
    image_prompt: str,
    product_name: str,
    product_description: str,
    platform: str,
    goal: str,
    style: str,
    previous_slogans: Optional[list[str]] = None,
    use_clip: bool = False,
    use_llm: bool = False,
    llm_model: str | None = None,
) -> IntegratedEvaluation:
    slogan_result = evaluate_slogan(
        slogan,
        product_name=product_name,
        product_description=product_description,
        platform=platform,
        goal=goal,
        style=style,
        previous_slogans=previous_slogans,
    )

    image_result = evaluate_image(
        image_path,
        platform=platform,
        prompt=image_prompt,
        use_clip=use_clip,
        use_llm=use_llm,
        product_name=product_name,
        product_description=product_description,
        goal=goal,
        style=style,
        slogan=slogan,
        llm_model=llm_model,
    )

    consistency_score, consistency_details = calculate_consistency_score(
        slogan,
        image_prompt,
        product_name=product_name,
        style=style,
        goal=goal,
    )

    final_score = (
        slogan_result.final_score * 0.40
        + image_result.final_score * 0.40
        + consistency_score * 20 * 0.20
    )

    return IntegratedEvaluation(
        slogan_score=slogan_result.final_score,
        image_score=image_result.final_score,
        consistency_score=round(consistency_score * 20, 2),
        final_score=round(final_score, 2),
        details={
            "slogan": asdict(slogan_result),
            "image": asdict(image_result),
            "consistency": consistency_details,
        },
    )


def result_to_dict(result) -> dict:
    return asdict(result)



def evaluate_and_log_slogans(
    *,
    slogans: list[str],
    product_name: str,
    product_description: str,
    platform: str,
    goal: str | None,
    style: str | None,
) -> None:
    """생성된 슬로건을 각각 평가하고 서버 로그에만 출력합니다."""
    for index, slogan in enumerate(slogans, start=1):
        try:
            result = evaluate_slogan(
                slogan=slogan,
                product_name=product_name,
                product_description=product_description or "",
                platform=platform or "instagram",
                goal=goal or "awareness",
                style=style or "warm",
                previous_slogans=slogans[: index - 1],
            )

            logger.info(
                "\n"
                "========== 슬로건 %d 평가 ==========\n"
                "슬로건: %s\n"
                "상품 반영도: %.2f / 5\n"
                "상품명 포함 여부: %s\n"
                "상품 평가 키워드: %s\n"
                "일치 상품 키워드: %s\n"
                "플랫폼 적합성: %.2f / 5\n"
                "목표 반영도: %.2f / 5\n"
                "일치 목표 키워드: %s\n"
                "스타일 반영도: %.2f / 5\n"
                "일치 스타일 키워드: %s\n"
                "자연스러움: %.2f / 5\n"
                "광고 매력도: %.2f / 5\n"
                "독창성: %.2f / 5\n"
                "슬로건 종합점수: %.2f / 100\n"
                "====================================",
                index,
                slogan,
                result.product_reflection,
                result.details["product_name_included"],
                result.details["product_keywords"],
                result.details["matched_product_keywords"],
                result.platform_fit,
                result.goal_reflection,
                result.details["matched_goal_keywords"],
                result.style_reflection,
                result.details["matched_style_keywords"],
                result.naturalness,
                result.advertising_appeal,
                result.originality,
                result.final_score,
            )
        except Exception:
            logger.exception(
                "슬로건 %d 평가 중 오류가 발생했습니다. 생성 결과에는 영향을 주지 않습니다.",
                index,
            )


def evaluate_and_log_images(
    *,
    drafts: list[dict],
    platform: str,
    use_clip: bool = False,
    use_llm: bool = False,
    product_name: str = "",
    product_description: str = "",
    goal: str = "",
    style: str = "",
    slogan: str = "",
    llm_model: str | None = None,
) -> None:
    """생성된 이미지를 각각 평가하고 서버 로그에만 출력합니다."""
    for index, draft in enumerate(drafts, start=1):
        draft_label = draft.get("id", index)

        try:
            result = evaluate_image(
                image_path=draft["image_path"],
                platform=platform or "instagram",
                prompt=draft.get("image_prompt", ""),
                use_clip=use_clip,
                use_llm=use_llm,
                product_name=product_name,
                product_description=product_description,
                goal=goal,
                style=style,
                slogan=(
                    draft.get("slogan")
                    or draft.get("selected_slogan")
                    or slogan
                ),
                llm_model=llm_model,
            )

            prompt_similarity = (
                f"{result.prompt_similarity_score:.2f} / 5"
                if result.prompt_similarity_score is not None
                else "미사용"
            )

            logger.info(
                "\n"
                "========== 이미지 %s 평가 ==========\n"
                "이미지 경로: %s\n"
                "해상도: %.2f / 5\n"
                "화면 비율: %.2f / 5\n"
                "선명도: %.2f / 5\n"
                "밝기: %.2f / 5\n"
                "대비: %.2f / 5\n"
                "기술 품질: %.2f / 5\n"
                "프롬프트 유사도: %s\n"
                "LLM 시각 평가: %s\n"
                "LLM 피드백: %s\n"
                "이미지 종합점수: %.2f / 100\n"
                "====================================",
                draft_label,
                draft["image_path"],
                result.resolution_score,
                result.aspect_ratio_score,
                result.sharpness_score,
                result.brightness_score,
                result.contrast_score,
                result.technical_quality_score,
                prompt_similarity,
                (
                    f"{result.llm_visual_score:.2f} / 5"
                    if result.llm_visual_score is not None
                    else "미사용"
                ),
                result.llm_feedback or "미사용",
                result.final_score,
            )
        except Exception:
            logger.exception(
                "이미지 %s 평가 중 오류가 발생했습니다. 생성 결과에는 영향을 주지 않습니다.",
                draft_label,
            )

def evaluate_and_log_ad_result(
    *,
    slogan: str,
    image_path: str | Path,
    image_prompt: str,
    product_name: str,
    product_description: str,
    platform: str,
    goal: str,
    style: str,
    previous_slogans: Optional[list[str]] = None,
    use_clip: bool = False,
    use_llm: bool = False,
    llm_model: str | None = None,
) -> None:
    """광고 결과를 평가하고 서버 로그에만 출력합니다."""
    try:
        evaluation = evaluate_ad_result(
            slogan=slogan,
            image_path=image_path,
            image_prompt=image_prompt,
            product_name=product_name,
            product_description=product_description,
            platform=platform,
            goal=goal,
            style=style,
            previous_slogans=previous_slogans,
            use_clip=use_clip,
            use_llm=use_llm,
            llm_model=llm_model,
        )

        slogan_detail = evaluation.details["slogan"]
        image_detail = evaluation.details["image"]

        logger.info(
            "\n"
            "========== 광고 생성 평가 ==========\n"
            "상품명: %s\n"
            "플랫폼: %s\n"
            "광고 목표: %s\n"
            "스타일: %s\n"
            "생성 슬로건: %s\n"
            "------------------------------------\n"
            "[슬로건 평가]\n"
            "상품 반영도: %.2f / 5\n"
            "상품명 포함 여부: %s\n"
            "상품 평가 키워드: %s\n"
            "일치 상품 키워드: %s\n"
            "플랫폼 적합성: %.2f / 5\n"
            "목표 반영도: %.2f / 5\n"
            "스타일 반영도: %.2f / 5\n"
            "자연스러움: %.2f / 5\n"
            "광고 매력도: %.2f / 5\n"
            "독창성: %.2f / 5\n"
            "슬로건 종합점수: %.2f / 100\n"
            "------------------------------------\n"
            "[이미지 평가]\n"
            "해상도: %.2f / 5\n"
            "화면 비율: %.2f / 5\n"
            "선명도: %.2f / 5\n"
            "밝기: %.2f / 5\n"
            "대비: %.2f / 5\n"
            "기술 품질: %.2f / 5\n"
            "프롬프트 유사도: %s\n"
            "LLM 시각 평가: %s\n"
            "LLM 피드백: %s\n"
            "이미지 종합점수: %.2f / 100\n"
            "------------------------------------\n"
            "슬로건-이미지 일관성: %.2f / 100\n"
            "최종 평가점수: %.2f / 100\n"
            "====================================",
            product_name,
            platform,
            goal,
            style,
            slogan,
            slogan_detail["product_reflection"],
            slogan_detail["details"]["product_name_included"],
            slogan_detail["details"]["product_keywords"],
            slogan_detail["details"]["matched_product_keywords"],
            slogan_detail["platform_fit"],
            slogan_detail["goal_reflection"],
            slogan_detail["style_reflection"],
            slogan_detail["naturalness"],
            slogan_detail["advertising_appeal"],
            slogan_detail["originality"],
            evaluation.slogan_score,
            image_detail["resolution_score"],
            image_detail["aspect_ratio_score"],
            image_detail["sharpness_score"],
            image_detail["brightness_score"],
            image_detail["contrast_score"],
            image_detail["technical_quality_score"],
            (
                f'{image_detail["prompt_similarity_score"]:.2f} / 5'
                if image_detail["prompt_similarity_score"] is not None
                else "미사용"
            ),
            (
                f'{image_detail["llm_visual_score"]:.2f} / 5'
                if image_detail["llm_visual_score"] is not None
                else "미사용"
            ),
            image_detail["llm_feedback"] or "미사용",
            evaluation.image_score,
            evaluation.consistency_score,
            evaluation.final_score,
        )

    except Exception:
        logger.exception(
            "광고 평가 중 오류가 발생했습니다. "
            "평가 실패와 관계없이 광고 생성 결과는 정상 반환됩니다."
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    sample = evaluate_slogan(
        "육즙 가득한 함박스테이크, 오늘 저녁 바로 주문하세요!",
        product_name="함박스테이크",
        product_description="두툼한 패티와 진한 데미그라스 소스",
        platform="baemin",
        goal="sales",
        style="warm",
        previous_slogans=[
            "육즙 가득 함박스테이크로 따뜻한 저녁을 즐겨보세요."
        ],
    )

    print(result_to_dict(sample))