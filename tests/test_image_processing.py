from __future__ import annotations

from pathlib import Path

from PIL import Image

from gartic_phone_drawer.image_processing import (
    create_outline_image,
    find_pixels_matching_color,
    make_transparent_background,
)


def _create_test_image(path: Path) -> None:
    image = Image.new("RGBA", (4, 4), (255, 0, 0, 255))
    pixels = image.load()
    assert pixels is not None
    pixels[1, 1] = (0, 0, 0, 255)
    pixels[2, 2] = (0, 0, 0, 0)
    image.save(path)


def test_find_pixels_matching_color(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    _create_test_image(source)

    matches = find_pixels_matching_color(source, target_color=(0, 0, 0), tolerance=0)
    assert (1, 1) in matches
    assert (2, 2) not in matches  # Fully transparent pixel should be ignored by default


def test_make_transparent_background(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    _create_test_image(source)
    out_file = tmp_path / "transparent.png"

    result = make_transparent_background(source, out_file, target_color=(255, 0, 0), tolerance=0)
    assert result == out_file
    with Image.open(result) as img:
        img.load()
        assert img.mode == "RGBA"
    pixel0 = img.getpixel((0, 0))
    assert isinstance(pixel0, tuple)
    assert pixel0[3] == 0
    pixel1 = img.getpixel((1, 1))
    assert isinstance(pixel1, tuple)
    assert pixel1[3] == 255  # Black pixel remains solid


def test_create_outline_image(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    _create_test_image(source)
    out_file = tmp_path / "outline.png"

    result = create_outline_image(source, out_file)
    assert result == out_file
    assert out_file.exists()
    assert out_file.stat().st_size > 0
