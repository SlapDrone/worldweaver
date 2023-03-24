from app.models.image import CharacterDescription, GeneratedImage
from app.services.ai import AIModel

class ImageService:
    def __init__(self, ai_model: AIModel):
        self.ai_model = ai_model

    def generate_image(self, character_description: CharacterDescription) -> GeneratedImage:
        image_url = self.ai_model.generate_image(character_description)
        return GeneratedImage(character_name=character_description.name, image_url=image_url)
