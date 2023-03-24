from fastapi import APIRouter, Depends
from app.models.image import CharacterDescription, GeneratedImage
from app.services.ai import AIModel
from app.services.image import ImageService

router = APIRouter()

def get_image_service(ai_model: AIModel = Depends()) -> ImageService:
    return ImageService(ai_model)

@router.post("/generate-image", response_model=GeneratedImage)
async def generate_image(character_description: CharacterDescription, image_service: ImageService = Depends(get_image_service)):
    generated_image = image_service.generate_image(character_description)
    return generated_image
