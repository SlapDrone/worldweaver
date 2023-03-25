from fastapi import APIRouter, Depends
from worldweaver.models.music import SceneDescription, GeneratedMusic
from worldweaver.services.ai import AIModel
from worldweaver.services.music import MusicService

router = APIRouter()

def get_music_service(ai_model: AIModel = Depends()) -> MusicService:
    return MusicService(ai_model)

@router.post("/generate-music", response_model=GeneratedMusic)
async def generate_music(scene_description: SceneDescription, music_service: MusicService = Depends(get_music_service)):
    generated_music = music_service.generate_music(scene_description)
    return generated_music
