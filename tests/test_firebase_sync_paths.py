from pathlib import Path

from src.camera import Camera
from src.firebase_sync import FirebaseSync


def test_requirements_use_rpi_gpio_not_jetson_gpio():
    text = Path(__file__).resolve().parents[1].joinpath("requirements.txt").read_text()
    assert "RPi.GPIO" in text
    assert "Jetson.GPIO" not in text


def test_build_remote_image_path_uses_device_root_and_separated_categories():
    sync = FirebaseSync.__new__(FirebaseSync)
    sync.device_id = "raspPi4"

    assert sync._build_image_remote_path("checkin_plant", "plant_checkin_20260101_010203.jpg") == (
        "grows/raspPi4/image3/plant/plant_checkin_20260101_010203.jpg"
    )
    assert sync._build_image_remote_path("checkin_dashboard", "dashboard_checkin_20260101_010203.jpg") == (
        "grows/raspPi4/image3/dashboard/dashboard_checkin_20260101_010203.jpg"
    )


def test_camera_returns_blank_image_when_no_real_image_exists(tmp_path):
    camera = Camera({"camera": {"image_dir": str(tmp_path / "images")}})

    blank_image = camera.get_blank_image_path()
    assert blank_image.exists()
    assert camera.get_latest_image("plant") == str(blank_image)
    assert camera.get_latest_image("dashboard") == str(blank_image)
