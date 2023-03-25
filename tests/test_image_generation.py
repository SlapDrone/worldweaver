import pytest
from tests.conftest import test_app
from app.models.image import CharacterDescription

@pytest.mark.parametrize("description, name", 
    [
        ("A brave knight", "Sir Sweatsalot"),
        ("A cunning thief", "Pokey")
    ]
)
def test_generate_image(description, name, test_app):
    response = test_app.post(
        "/api/v1/generate-image",
        json={
            "description": description,
            "name": name
        }
    )
    assert response.status_code == 200
    assert "image_url" in response.json()
