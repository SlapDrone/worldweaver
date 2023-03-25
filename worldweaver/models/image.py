from pydantic import BaseModel
from typing import Optional

class CharacterDescription(BaseModel):
    name: str
    description: str
    style: Optional[str] = None

class GeneratedImage(BaseModel):
    character_name: str
    image_url: str
