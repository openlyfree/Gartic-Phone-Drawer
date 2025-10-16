from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from PIL import Image

from gartic_phone_drawer.automation import CanvasConfig, draw_image_mask, draw_point, draw_points, draw_random_walk


@dataclass
class FakeMouse:
    moves: List[tuple[int, int]]
    clicks: int = 0

    def move(self, x: int, y: int) -> None:
        self.moves.append((x, y))

    def click(self) -> None:
        self.clicks += 1


def _build_image(path: Path) -> None:
    image = Image.new("RGBA", (2, 2), (255, 255, 255, 255))
    pixels = image.load()
    assert pixels is not None
    pixels[0, 0] = (0, 0, 0, 255)
    image.save(path)


def test_draw_point_within_bounds() -> None:
    mouse = FakeMouse([])
    canvas = CanvasConfig(offset=(0, 0), max_point=(10, 10))

    result = draw_point((5, 5), canvas=canvas, mouse=mouse)

    assert result is True
    assert mouse.moves == [(5, 5)]
    assert mouse.clicks == 1


def test_draw_point_out_of_bounds() -> None:
    mouse = FakeMouse([])
    canvas = CanvasConfig(offset=(0, 0), max_point=(10, 10))

    result = draw_point((20, 20), canvas=canvas, mouse=mouse)

    assert result is False
    assert mouse.moves == []
    assert mouse.clicks == 0


def test_draw_points_respects_sample_rate() -> None:
    mouse = FakeMouse([])
    canvas = CanvasConfig(offset=(0, 0), max_point=(10, 10))

    count = draw_points([(x, 0) for x in range(5)], canvas=canvas, mouse=mouse, sample_rate=2)

    assert count == 3  # indices 0, 2, 4
    assert mouse.clicks == 3


def test_draw_random_walk_uses_ranges() -> None:
    mouse = FakeMouse([])
    canvas = CanvasConfig(offset=(0, 0), max_point=(100, 100))

    count = draw_random_walk(start=(0, 0), steps=3, dx_range=(0, 0), dy_range=(0, 0), canvas=canvas, mouse=mouse)

    assert count == 3
    assert mouse.moves == [(0, 0), (0, 0), (0, 0)]


def test_draw_image_mask(tmp_path: Path) -> None:
    image_path = tmp_path / "mask.png"
    _build_image(image_path)

    mouse = FakeMouse([])
    canvas = CanvasConfig(offset=(0, 0), max_point=(10, 10))

    count = draw_image_mask(str(image_path), canvas=canvas, mouse=mouse, sample_rate=1)

    assert count == 1
    assert mouse.moves == [(0, 0)]
    assert mouse.clicks == 1
