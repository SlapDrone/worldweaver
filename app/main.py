from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.routes import images, music
from app.services.ai import AIModel


# Initialize the AIModel instance and add it to the app's dependency container
@asynccontextmanager
async def lifespan(app: FastAPI):
    # load the model
    ai_model = AIModel()
    yield
    del ai_model


app = FastAPI(lifespan=lifespan)


# Register the API routes
app.include_router(images.router, prefix="/api/v1", tags=["image"])
app.include_router(music.router, prefix="/api/v1", tags=["music"])

# Middleware and additional settings can be added here
