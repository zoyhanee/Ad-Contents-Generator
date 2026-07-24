from types import ModuleType

from app.core.config import settings
from app.services import v1, v2
from app.schemas.prompt import ImagePromptInput, SloganPromptInput


_PROMPT_VERSIONS: dict[str, ModuleType] = {
    "v1": v1,
    "v2": v2,
}


def get_prompt_version(version: str | None = None) -> str:
    """요청 버전 또는 .env의 기본 프롬프트 버전을 정규화해 반환합니다."""
    selected_version = version or settings.PROMPT_VERSION
    return str(selected_version).strip().lower()


def get_prompt_builder(version: str | None = None) -> ModuleType:
    """선택된 버전에 해당하는 프롬프트 모듈을 반환합니다."""
    selected_version = get_prompt_version(version)

    try:
        return _PROMPT_VERSIONS[selected_version]
    except KeyError as exc:
        supported_versions = ", ".join(_PROMPT_VERSIONS)
        raise ValueError(
            f"지원하지 않는 프롬프트 버전입니다: {selected_version}. "
            f"지원 버전: {supported_versions}"
        ) from exc


def build_slogan_prompt(
    prompt_input: SloganPromptInput,
    version: str | None = None,
) -> str:
    """선택된 버전의 슬로건 프롬프트를 생성합니다."""
    builder = get_prompt_builder(version)
    return builder.build_slogan_prompt(prompt_input)


def build_image_prompt(
    prompt_input: ImagePromptInput,
    version: str | None = None,
) -> str:
    """선택된 버전의 이미지 프롬프트를 생성합니다."""
    builder = get_prompt_builder(version)
    return builder.build_image_prompt(prompt_input)