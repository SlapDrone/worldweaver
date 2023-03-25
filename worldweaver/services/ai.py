from typing import Union
from worldweaver.models.image import CharacterDescription
from worldweaver.models.music import SceneDescription

class AIModel:
    def generate_image(self, character_description: CharacterDescription) -> str:
        # Placeholder method for AI image generation
        image_url = "https://example.com/generated-image.png"
        return image_url

    def generate_music(self, scene_description: SceneDescription) -> str:
        # Placeholder method for AI music generation
        music_url = "https://example.com/generated-music.mp3"
        return music_url

    def generate_content(self, description: Union[CharacterDescription, SceneDescription]) -> str:
        if isinstance(description, CharacterDescription):
            return self.generate_image(description)
        elif isinstance(description, SceneDescription):
            return self.generate_music(description)
        else:
            raise ValueError("Invalid description type")
