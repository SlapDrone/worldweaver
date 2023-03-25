from contextlib import asynccontextmanager

from fastapi import FastAPI
from worldweaver.api.routes import images, music
from worldweaver.services.ai import AIModel


# Initialize the AIModel instance and add it to the app's dependency container
@asynccontextmanager
async def lifespan(app: FastAPI):
    # load the model
    ai_model = AIModel()
    yield
    del ai_model


app = FastAPI(lifespan=lifespan)


# Register the API routes
worldweaver.include_router(images.router, prefix="/api/v1", tags=["image"])
worldweaver.include_router(music.router, prefix="/api/v1", tags=["music"])

# Middleware and additional settings can be added here
