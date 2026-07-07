from openai import OpenAI

from app.ml.clients.base import TextModelClient


class OpenAITextClient(TextModelClient):
    def __init__(
        self,
        model_name: str,
        api_key: str,
    ):
        self.model_name = model_name
        self.client = OpenAI(
            api_key=api_key,
        )

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model_name,
            input=prompt,
        )

        return response.output_text