from app.ml.clients.base import TextModelClient


def generate_image_prompt(
    client: TextModelClient,
    product_name: str,
    product_description: str | None,
    platform: str,
    style: str | None,
    selected_slogan: str,
    concept: str,
    improvement_rules: list[str] | None = None,
) -> str:
    improvement_rules = improvement_rules or []
    improvement_guide = ""

    if improvement_rules:
        rules_text = "\n".join(
            f"- {rule}"
            for rule in improvement_rules
        )

        improvement_guide = f"""

Accumulated evaluation-based image improvement guidance:
The following guidance comes from recurring weaknesses found in previous generated ad evaluations.
Apply it only when it is relevant to the current product, strategy, slogan, and concept.

{rules_text}
""".rstrip()

    prompt = f"""
You are an expert advertising creative director.

Create one detailed image-generation prompt for a promotional advertisement.

Product name:
{product_name}

Product description:
{product_description or "Not provided"}

Target platform:
{platform}

Visual style:
{style or "Not specified"}

Advertising slogan:
{selected_slogan}

Creative concept:
{concept}
{improvement_guide}

Requirements:
- Follow the creative concept clearly.
- Focus on the product.
- Reflect the target platform.
- Reflect the requested visual style.
- Create a visually specific scene suitable for an image-generation model.
- Do not invent product colors, materials, logos, structural details, or features that were not provided.
- Do not add unsupported technical features or internal product components.
- Treat the original product image as the source of truth for the product's appearance.
- Preserve the product's shape, color, logo, proportions, and visible details.
- You may creatively design only the background, lighting, composition, atmosphere, and advertising presentation.
- Do not explain your reasoning.
- Return only the final image-generation prompt.
""".strip()

    return client.generate(prompt)
