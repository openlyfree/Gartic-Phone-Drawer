"""High-level helpers for automating Gartic Phone drawing workflows."""

from .automation import CanvasConfig, draw_image_mask, draw_point, draw_points, draw_random_walk
from .image_processing import create_outline_image, find_pixels_matching_color, make_transparent_background

__all__ = [
    "CanvasConfig",
    "draw_image_mask",
    "draw_point",
    "draw_points",
    "draw_random_walk",
    "create_outline_image",
    "find_pixels_matching_color",
    "make_transparent_background",
]
