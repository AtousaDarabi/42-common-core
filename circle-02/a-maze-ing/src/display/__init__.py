"""Terminal ASCII visual representation of a maze, with basic interactions.

Satisfies the subject's chapter V (Visual representation) mandatory
requirement using plain ASCII rendering (no MLX dependency required).

Rendering style matches the subject's own example screenshot: solid
coloured wall blocks on a black background rather than box-drawing
characters, with the entry, exit, '42' pattern, and solution path each
picked out in their own colour (see the "Terminal default rendering of the
maze" / "Different maze, shortest path and wall colours" figures).

Split across this package: `colors.py` (palette + `sgr`), `canvas.py`
(blank canvas + wall drawing), `cells.py` (interior fill), `render.py`
(`render_ascii`, the public entry point), `menu.py` (`print_menu`).
"""

from .colors import CELL_W, COLOR_NAMES
from .menu import print_menu
from .render import render_ascii

__all__ = ["CELL_W", "COLOR_NAMES", "print_menu", "render_ascii"]
