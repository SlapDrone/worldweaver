import pytest
from tests.conftest import test_app
from app.models.music import SceneDescription

@pytest.mark.parametrize("scene", ["Entering a dungeon", "Walking through a forest"])
def test_generate_music(scene, test_app):
    response = test_app.post("/api/v1/generate-music", json={"scene": scene})
    assert response.status_code == 200
    assert "music_url" in response.json()
