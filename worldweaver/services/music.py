from worldweaver.models.music import SceneDescription, GeneratedMusic
from worldweaver.services.ai import AIModel

class MusicService:
    def __init__(self, ai_model: AIModel):
        self.ai_model = ai_model

    def generate_music(self, scene_description: SceneDescription) -> GeneratedMusic:
        music_url = self.ai_model.generate_music(scene_description)
        return GeneratedMusic(scene_description=scene_description, music_url=music_url)
