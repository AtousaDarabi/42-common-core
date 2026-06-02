"""Colour palette and small constants for the MLX display.

`ALL_WALLS_CLOSED` matches `src/display/` -- a fully-walled cell is a '42'
pattern cell. `KEY_*` are X11 keysyms (`mlx_key_hook` receives a keysym,
not a raw keycode). `WALL_COLORS` cycles through warm ivory, terracotta,
sage green, sky blue, warm gold, orchid, and muted teal -- a softer, more
cohesive "flat UI" palette for the MLX window (the ASCII display keeps its
own separate ANSI colours in `src/display/colors.py`; the two no longer
need to match hue-for-hue). `ENTRY_COLOR` is pink, `EXIT_COLOR` is coral
(doubling as `CURRENT_COLOR` during solving), `PATTERN_COLOR` is a muted
plum-charcoal, and `PATH_COLOR` (gold) highlights the final shortest path.
`FRONTIER_COLOR` (amber) marks cells discovered/queued but not processed
yet, `TRAIL_COLOR` (violet) marks cells the solver has already fully
processed, and `BACKGROUND_COLOR` matches `mlx_clear_window`'s black, used
to erase.
"""

CELL_SIZE = 20
NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
ALL_WALLS_CLOSED = 15

KEY_R = 114
KEY_P = 112
KEY_C = 99
KEY_Q = 113
KEY_ESCAPE = 65307

WALL_COLORS = [
    0xEDE7DA,
    0xE07856,
    0x8FBF6B,
    0x6FA8DC,
    0xF2C14E,
    0xC98BC9,
    0x6FC2C2,
]
ENTRY_COLOR = 0xE84393
EXIT_COLOR = 0xE8590C
PATTERN_COLOR = 0x3D3548
PATH_COLOR = 0xE8B23D
CURRENT_COLOR = EXIT_COLOR
FRONTIER_COLOR = 0xD9A441
TRAIL_COLOR = 0x6C5CE7
BACKGROUND_COLOR = 0x000000
