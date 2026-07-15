from abc import ABC, abstractmethod


class ImageModelClient(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        source_image_path: str | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> bytes:
        """Generate an image and return the image data as bytes."""
        raise NotImplementedError