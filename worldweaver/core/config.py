from pydantic import BaseSettings


class Settings(BaseSettings):
    API_VERSION: str = "v1"
    API_TITLE: str = "WorldWeaver API"
    API_DESCRIPTION: str = "API for generating art and music for tabletop RPG experiences."
    BASE_URL: str = "/api"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
