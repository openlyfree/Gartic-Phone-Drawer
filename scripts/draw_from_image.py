"""Command-line entry point to draw matching pixels from an image onto Gartic Phone."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple

from gartic_phone_drawer import CanvasConfig, draw_image_mask


DEFAULT_TARGET_COLOR = (0, 0, 0)
DEFAULT_OFFSET = (530, 334)
DEFAULT_MAX_POINT = (1120, 695)


def _parse_color(value: str) -> Tuple[int, int, int]:
    try:
        parts = [int(part) for part in value.split(",")]
    except ValueError as exc:  # pragma: no cover - defensive
        raise argparse.ArgumentTypeError("Color components must be integers") from exc
    if len(parts) != 3 or any(component < 0 or component > 255 for component in parts):
        raise argparse.ArgumentTypeError("Provide color as 'R,G,B' with values between 0 and 255")
    return parts[0], parts[1], parts[2]


def _parse_point(value: str) -> Tuple[int, int]:
    try:
        parts = [int(part) for part in value.split(",")]
    except ValueError as exc:  # pragma: no cover - defensive
        raise argparse.ArgumentTypeError("Points must contain integers") from exc
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("Provide points as 'x,y'")
    return parts[0], parts[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="Path to the source image")
    parser.add_argument("--target-color", type=_parse_color, default=DEFAULT_TARGET_COLOR, help="RGB color to track (default: 0,0,0)")
    parser.add_argument("--tolerance", type=int, default=0, help="Color tolerance (default: 0)")
    parser.add_argument("--alpha-min", type=int, default=1, help="Minimum alpha value for a pixel to be considered (default: 1)")
    parser.add_argument("--sample-rate", type=int, default=10, help="Draw every n-th matching pixel to limit total clicks (default: 10)")
    parser.add_argument("--offset", type=_parse_point, default=DEFAULT_OFFSET, help="Canvas offset in screen pixels (default: 530,334)")
    parser.add_argument("--max-point", type=_parse_point, default=DEFAULT_MAX_POINT, help="Maximum safe screen coordinate (default: 1120,695)")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.image.exists():
        parser.error(f"Image not found: {args.image}")

    canvas = CanvasConfig(offset=args.offset, max_point=args.max_point)
    drawn = draw_image_mask(
        str(args.image),
        target_color=tuple(args.target_color),
        tolerance=args.tolerance,
        alpha_min=args.alpha_min,
        sample_rate=args.sample_rate,
        canvas=canvas,
    )
    print(f"Drawn {drawn} points from {args.image}")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
