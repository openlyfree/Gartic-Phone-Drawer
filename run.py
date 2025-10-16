"""Simple configuration-based runner for the Gartic Phone drawer.

Edit the variables below, then run this file with ``python run_with_config.py``.
"""
from __future__ import annotations

from pathlib import Path

from gartic_phone_drawer import CanvasConfig, draw_image_mask

# --- Configuration --------------------------------------------------------
IMAGE_PATH: Path = Path("examples/goomba.png")
TARGET_COLOR: tuple[int, int, int] = (0, 0, 0)
COLOR_TOLERANCE: int = 0
MIN_ALPHA: int = 1
SAMPLE_RATE: int = 10
CANVAS_OFFSET: tuple[int, int] = (530, 334)
MAX_SCREEN_POINT: tuple[int, int] = (1120, 695)
# -------------------------------------------------------------------------


def _validate_image(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Image not found: {resolved}")
    return resolved


def main() -> None:
    image = _validate_image(IMAGE_PATH)
    canvas = CanvasConfig(offset=CANVAS_OFFSET, max_point=MAX_SCREEN_POINT)

    print(f"Preparing to draw {image}")
    drawn = draw_image_mask(
        str(image),
        target_color=TARGET_COLOR,
        tolerance=COLOR_TOLERANCE,
        alpha_min=MIN_ALPHA,
        sample_rate=SAMPLE_RATE,
        canvas=canvas,
    )
    print(f"Completed drawing {drawn} points from {image}")


if __name__ == "__main__":  # pragma: no cover - manual entry
    main()
