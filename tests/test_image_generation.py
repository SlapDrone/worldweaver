import pytest
from tests.conftest import test_app
from app.models.image import CharacterDescription

@pytest.mark.parametrize("description", ["A brave knight", "A cunning thief"])
def test_generate_image(description, test_app):
    response = test_app.post("/api/v1/generate-image", json={"description": description})
    assert response.status_code == 200
    assert "image_url" in response.json()
