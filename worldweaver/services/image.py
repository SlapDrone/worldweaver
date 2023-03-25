import abc
import base64
import os
import io
import warnings
from dotenv import load_dotenv
from enum import Enum

import pydantic
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

from worldweaver.models.image import CharacterDescription, GeneratedImage
from worldweaver.services.ai import AIModel


class ImageServiceInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate_image(self, character_description: CharacterDescription) -> GeneratedImage:
        pass


class ImageService(ImageServiceInterface):
    def __init__(self, ai_model: AIModel):
        self.ai_model = ai_model

    def generate_image(self, character_description: CharacterDescription) -> GeneratedImage:
        image_url = self.ai_model.generate_image(character_description)
        return GeneratedImage(character_name=character_description.name, image_url=image_url)


class StabilityEngine(str, Enum):
    stable_diffusion_v1: str = "stable-diffusion-v1"
    stable_diffusion_v_1_5: str = "stable-diffusion-v1-5"
    stable_diffusion_512_v2_0: str = "stable-diffusion-512-v2-0"
    stable_diffusion_768_v2_0: str = "stable-diffusion-768-v2-0"
    stable_diffusion_512_v2_1: str = "stable-diffusion-512-v2-1"
    stable_diffusion_768_v2_1: str = "stable-diffusion-768-v2-1"
    stable_inpainting_v1_0: str ="stable-inpainting-v1-0"
    stable_inpainting_512_v2_0: str = "stable-inpainting-512-v2-0"


class StabilitySettings(pydantic.BaseSettings):
    engine: StabilityEngine = pydantic.Field(
        default="stable-diffusion-512-v2-1", env="STABILITY_ENGINE")
    api_host: str = pydantic.Field(
        default="grpc.stability.ai:443", env="STABILITY_HOST")
    api_key: str = pydantic.Field(env="STABILITY_KEY")
    verbose: bool = pydantic.Field(default=False, env="STABILITY_VERBOSE")


def character_description_to_prompt(description: CharacterDescription) -> str:
    return f"{description.name}, {description.description}"


class StabilityException(Exception):
    pass


class TriggeredFilter(StabilityException):
    pass


class UnknownArtifactType(StabilityException):
    pass


class StabilityAI(ImageServiceInterface):
    def __init__(self, config: StabilitySettings):
        self.config = config
        # Set up our connection to the API.
        self.stability_api = client.StabilityInference(
            key=self.config.api_key, # API Key reference.
            verbose=self.config.verbose, # Print debug messages.
            engine=self.config.engine, # Set the engine to use for generation. 
        )

    def generate_image(self, character_description: CharacterDescription) -> GeneratedImage:
        # Set up our initial generation parameters.
        answers = self.stability_api.generate(
            prompt=character_description_to_prompt(character_description),
            seed=992446758, # If a seed is provided, the resulting generated image will be deterministic.
                            # What this means is that as long as all generation parameters remain the same, you can always recall the same image simply by generating it again.
                            # Note: This isn't quite the case for Clip Guided generations, which we'll tackle in a future example notebook.
            steps=30, # Amount of inference steps performed on image generation. Defaults to 30.
            cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                        # Setting this value higher increases the strength in which it tries to match your prompt.
                        # Defaults to 7.0 if not specified.
            width=512, # Generation width, defaults to 512 if not included.
            height=512, # Generation height, defaults to 512 if not included.
            samples=1, # Number of images to generate, defaults to 1 if not included.
            sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
                                                        # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
                                                        # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
        )

        # Set up our warning to print to the console if the adult content classifier is tripped.
        # If adult content classifier is not tripped, save generated images.
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    raise TriggeredFilter(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again."
                    )
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img_bytes = artifact.binary
                    #return img_bytes
                    img = Image.open(io.BytesIO(artifact.binary))
                    target_file = str(artifact.seed)+ ".png"
                    print(f"Saving to {target_file}")
                    img.save(target_file) # Save our generated images with their seed number as the filename.   


if __name__ == "__main__":
    load_dotenv(".env")
    config = StabilitySettings()
    stability_ai = StabilityAI(config)
    desc = CharacterDescription(
        name="Griknir",
        description=(
            "A short, fat, wrinkled goblin character. "
            "Scowling."
            "Standing over a pile of gizmos. "
            "Steampunk aesthetic. Day."
            "RPG class card portrait. Engineer."
        )
    )
    desc = CharacterDescription(
        name="Carlak",
        description=(
            "Robed human-sized crow with arms. Feathered. Female. Maniacal."
            "Standing over a wooden table filled with potions."
            "Clutching coloured vials to its chest."
            "Beside a Cauldron. "
            "Steampunk aesthetic. Outside. Town in background. Day."
            "RPG class card portrait. Alchemist."
        )
    )
    img = stability_ai.generate_image(desc)