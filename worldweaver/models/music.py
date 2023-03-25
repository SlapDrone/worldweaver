from pydantic import BaseModel, Field
from typing import Optional

class SceneDescription(BaseModel):
    scene: str
    mood: Optional[str] = None
    genre: Optional[str] = None

class GeneratedMusic(BaseModel):
    scene_description: SceneDescription
    music_url: str

