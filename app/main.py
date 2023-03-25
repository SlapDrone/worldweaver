from fastapi import FastAPI
from app.api.routes import image, music
from app.services.ai import AIModel

app = FastAPI()

# Initialize the AIModel instance and add it to the app's dependency container
@app.on_event("startup")
async def startup_event():
    ai_model = AIModel()
    app.container.bind(AIModel, ai_model)

# Register the API routes
app.include_router(image.router, prefix="/api/v1", tags=["image"])
app.include_router(music.router, prefix="/api/v1", tags=["music"])

# Middleware and additional settings can be added here
