"""Image helper utilities used by the Gartic Phone drawing automation."""
from __future__ import annotations

from pathlib import Path
from typing import List, Sequence, Tuple, cast

from PIL import Image, ImageFilter, ImageOps

Point = tuple[int, int]
Color = tuple[int, int, int]


def _ensure_path(path: str | Path) -> Path:
    result = Path(path)
    if not result.exists():
        raise FileNotFoundError(f"Image not found: {result}")
    return result


def _within_tolerance(color: Sequence[int], target: Color, tolerance: int) -> bool:
    return all(abs(component - target[idx]) <= tolerance for idx, component in enumerate(color[:3]))


def find_pixels_matching_color(image_path: str | Path, *, target_color: Color = (0, 0, 0), tolerance: int = 0, alpha_min: int = 1) -> List[Point]:
    """Return a list of coordinates whose color matches ``target_color`` within ``tolerance``."""
    path = _ensure_path(image_path)
    with Image.open(path).convert("RGBA") as img:
        width, height = img.size
        matches: List[Point] = []
        for y in range(height):
            for x in range(width):
                r, g, b, a = cast(Tuple[int, int, int, int], img.getpixel((x, y)))
                if a < alpha_min:
                    continue
                if _within_tolerance((r, g, b), target_color, tolerance):
                    matches.append((x, y))
    return matches


def create_outline_image(image_path: str | Path, output_path: str | Path, threshold_value: int = 128) -> Path:
    """Generate a high-contrast outline for ``image_path`` and persist it to ``output_path``."""
    if not 0 <= threshold_value <= 255:
        raise ValueError("threshold_value must be between 0 and 255")

    source = _ensure_path(image_path)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as img:
        img_gray = ImageOps.grayscale(img)
        img_binary = img_gray.point(lambda pixel: 255 if pixel > threshold_value else 0, "1")  # type: ignore[arg-type]
        img_inverted = ImageOps.invert(img_binary.convert("L"))
        img_outline = img_inverted.filter(ImageFilter.FIND_EDGES)
        img_outline_final = ImageOps.invert(img_outline)
        img_outline_final.save(destination)
    return destination


def make_transparent_background(input_image_path: str | Path, output_image_path: str | Path, *, target_color: Color = (255, 255, 255), tolerance: int = 10) -> Path:
    """Replace occurrences of ``target_color`` with transparency and save the result."""
    source = _ensure_path(input_image_path)
    destination = Path(output_image_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source).convert("RGBA") as img:
        data = cast(Sequence[Tuple[int, int, int, int]], img.getdata())
        new_pixels: List[Tuple[int, int, int, int]] = []
        for r, g, b, _a in data:
            if _within_tolerance((r, g, b), target_color, tolerance):
                new_pixels.append((r, g, b, 0))
            else:
                new_pixels.append((r, g, b, _a))
        img.putdata(new_pixels)  # type: ignore[arg-type]
        img.save(destination)
    return destination
