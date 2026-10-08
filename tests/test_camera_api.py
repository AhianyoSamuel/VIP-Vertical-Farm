from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from src import api_server
from src.camera import Camera


def test_relative_image_dir_is_rooted_at_project_directory(tmp_path):
    camera = Camera(
        {"camera": {"image_dir": "data/images"}},
        base_dir=tmp_path,
    )

    assert camera.image_dir == tmp_path / "data" / "images"
    assert camera.image_dir.is_dir()


@pytest.mark.parametrize(
    ("camera_type", "endpoint"),
    [
        ("plant", "/api/camera/plant/latest"),
        ("dashboard", "/api/camera/dashboard/latest"),
    ],
)
def test_website_camera_endpoint_serves_latest_image(
    tmp_path, monkeypatch, camera_type, endpoint
):
    image_path = tmp_path / f"{camera_type}_latest.jpg"
    image_bytes = b"camera image bytes"
    image_path.write_bytes(image_bytes)
    grower = SimpleNamespace(
        camera=SimpleNamespace(
            get_latest_image=lambda requested_type: (
                str(image_path) if requested_type == camera_type else None
            )
        )
    )
    monkeypatch.setattr(api_server, "_grower", grower)

    with TestClient(api_server.app) as client:
        response = client.get(endpoint)

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    assert response.content == image_bytes
