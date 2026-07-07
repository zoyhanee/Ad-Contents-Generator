import base64

from openai import OpenAI

from app.ml.image_clients.base import ImageModelClient


class OpenAIImageClient(ImageModelClient):
    def __init__(
        self,
        model_name: str,
        api_key: str,
    ):
        self.model_name = model_name
        self.client = OpenAI(
            api_key=api_key,
        )

    def generate(
        self,
        prompt: str,
        source_image_path: str | None = None,
    ) -> bytes:
        if source_image_path is None:
            response = self.client.images.generate(
                model=self.model_name,
                prompt=prompt,
            )
        else:
            with open(source_image_path, "rb") as source_image:
                response = self.client.images.edit(
                    model=self.model_name,
                    image=source_image,
                    prompt=prompt,
                )

        image_base64 = response.data[0].b64_json

        return base64.b64decode(image_base64)