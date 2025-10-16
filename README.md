# Gartic Phone Drawer

Draws images in [Gartic Phone](https://garticphone.com/) by automating mouse clicks on the canvas.
⚠️ **Safety note:** running the script will move and click your mouse cursor. Make sure Gartic Phone is focused and you are ready before executing it.

## Installation

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Running

Edit the values at the top of `run.py` (image path, offsets, colour, sampling) and run:

```bash
python run.py
```

Config options:

- `--target-color` to change the color you want to follow (default `0,0,0`).
- `--tolerance` to accept colors within a range.
- `--alpha-min` to control how transparent pixels may be before they are ignored.
- `--offset` and `--max-point` to match your screen layout if the default offsets do not line up.





## Testing

The refactor ships with a pytest suite. Run it after activating your virtual environment:

```bash
pytest
```

The automation tests use a fake mouse implementation, so they are safe to run on any machine.
