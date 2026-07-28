from pathlib import Path
from uuid import uuid4

from app.ml.image_clients.factory import create_image_model_client
from app.services.edit_planner import EditPlan


class ImageEditService:

    def __init__(self):
        self.image_client = create_image_model_client()

    def edit(
        self,
        image_path: str,
        plan: EditPlan,
    ) -> str:

        original = Path(image_path)

        if not original.exists():
            raise FileNotFoundError(
                f"이미지를 찾을 수 없습니다: {image_path}"
            )

        image_bytes = self.image_client.generate(
            prompt=plan.prompt,
            source_image_path=str(original),
        )

        save_dir = Path("storage/generated")
        save_dir.mkdir(parents=True, exist_ok=True)

        save_path = save_dir / f"{uuid4().hex}.png"

        save_path.write_bytes(image_bytes)

        return str(save_path)