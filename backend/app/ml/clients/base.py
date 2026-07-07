from abc import ABC, abstractmethod


class TextModelClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text from the given prompt."""
        raise NotImplementedError