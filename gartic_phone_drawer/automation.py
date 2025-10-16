"""Utilities for controlling the Gartic Phone drawing canvas via pyautogui.

The original project exposed a couple of loosely related helper functions in a
single module.  This refactor groups together the automation-specific logic and
offers a small façade that is easier to test and reason about.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol
import random

import pyautogui

from .image_processing import find_pixels_matching_color

Point = tuple[int, int]


class MouseController(Protocol):
    """Protocol that encapsulates the small subset of mouse operations we need."""

    def move(self, x: int, y: int) -> None:
        ...

    def click(self) -> None:
        ...


class _PyAutoMouse:
    """Concrete ``MouseController`` backed by ``pyautogui``."""

    def __init__(self) -> None:
        pyautogui.PAUSE = 0

    def move(self, x: int, y: int) -> None:  # pragma: no cover - passthrough
        pyautogui.moveTo(x, y)

    def click(self) -> None:  # pragma: no cover - passthrough
        pyautogui.click()


@dataclass(slots=True)
class CanvasConfig:
    """Describe how the in-game canvas maps to screen coordinates."""

    offset: Point = (530, 334)
    max_point: Point = (1120, 695)

    def to_screen(self, point: Point) -> Point:
        """Translate a canvas-relative point to an absolute screen coordinate."""
        return self.offset[0] + point[0], self.offset[1] + point[1]

    def in_bounds(self, screen_point: Point) -> bool:
        """Check whether a screen coordinate is still inside the drawing area."""
        return screen_point[0] <= self.max_point[0] and screen_point[1] <= self.max_point[1]


def _resolve_mouse(mouse: MouseController | None) -> MouseController:
    return mouse if mouse is not None else _PyAutoMouse()


def draw_point(point: Point, *, canvas: CanvasConfig | None = None, mouse: MouseController | None = None) -> bool:
    """Move the cursor to ``point`` (canvas-relative) and click if it is safe.

    Returns ``True`` when the click happens, allowing callers to keep track of
    how many points were actually drawn.
    """
    cfg = canvas or CanvasConfig()
    controller = _resolve_mouse(mouse)
    screen_point = cfg.to_screen(point)
    if not cfg.in_bounds(screen_point):
        return False

    controller.move(*screen_point)
    controller.click()
    return True


def draw_points(points: Iterable[Point], *, canvas: CanvasConfig | None = None, mouse: MouseController | None = None, sample_rate: int = 1) -> int:
    """Click a collection of canvas points, optionally down-sampling them."""
    if sample_rate <= 0:
        raise ValueError("sample_rate must be a positive integer")

    cfg = canvas or CanvasConfig()
    controller = _resolve_mouse(mouse)
    drawn = 0
    for index, point in enumerate(points):
        if index % sample_rate != 0:
            continue
        screen_point = cfg.to_screen(point)
        if not cfg.in_bounds(screen_point):
            continue
        controller.move(*screen_point)
        controller.click()
        drawn += 1
    return drawn


def draw_random_walk(*, start: Point = (10, 10), steps: int = 10, dx_range: tuple[int, int] = (30, 50), dy_range: tuple[int, int] = (30, 60), canvas: CanvasConfig | None = None, mouse: MouseController | None = None) -> int:
    """Replicate the ad-hoc random test scribble from the legacy code."""
    cfg = canvas or CanvasConfig()
    controller = _resolve_mouse(mouse)

    point_x, point_y = start
    drawn = 0
    for _ in range(steps):
        screen_point = cfg.to_screen((point_x, point_y))
        if cfg.in_bounds(screen_point):
            controller.move(*screen_point)
            controller.click()
            drawn += 1
        point_x += random.randint(dx_range[0], dx_range[1])
        point_y += random.randint(dy_range[0], dy_range[1])
    return drawn


def draw_image_mask(image_path: str, *, target_color: tuple[int, int, int] = (0, 0, 0), tolerance: int = 0, alpha_min: int = 1, sample_rate: int = 10, canvas: CanvasConfig | None = None, mouse: MouseController | None = None) -> int:
    """Draw the pixels that match ``target_color`` from an image onto the canvas."""
    points = find_pixels_matching_color(image_path, target_color=target_color, tolerance=tolerance, alpha_min=alpha_min)
    return draw_points(points, canvas=canvas, mouse=mouse, sample_rate=sample_rate)
