def generate_drafts(
    product_name: str,
    product_description: str | None,
    platform: str,
    style: str | None,
    selected_slogan: str,
) -> list[dict]:
    """
    Generate advertising draft images.

    This function currently returns mock results.
    The actual AI generation pipeline will replace this implementation.
    """

    return [
        {
            "id": "A",
            "title": "시안 A",
            "version": 1,
            "image_path": None,
        },
        {
            "id": "B",
            "title": "시안 B",
            "version": 1,
            "image_path": None,
        },
        {
            "id": "C",
            "title": "시안 C",
            "version": 1,
            "image_path": None,
        },
    ]