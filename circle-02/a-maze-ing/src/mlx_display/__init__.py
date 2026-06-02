"""Graphical maze display using MiniLibX (see mlx/ and src/mlx_bindings/).

This is the "graphical display using the MiniLibX (MLX) library" option
from the subject's chapter V, as an alternative to the ASCII terminal
display in `src/display/`. Same interactions: regenerate, show/hide path,
cycle wall colour, quit -- plus the window's own X (close) button.

Split across this package: `colors.py` (palette + constants), `debug_log.py`
(TEMP diagnostics logger), `draw.py`/`render.py` (pixel drawing), `session.py`
and its mixins (`redraw_mixin.py`, `gen_animation.py`, `solve_animation.py`,
`input_handlers.py`) for the interactive window state, and this module for
the public `run_mlx_display()` entry point.
"""

from typing import Callable, Optional, Set, Tuple

from src.mlx_bindings import MLX, MLXUnavailableError

from .colors import CELL_SIZE
from .session import MlxSession

__all__ = ["run_mlx_display"]


def run_mlx_display(
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int],
    regenerate: Callable[..., None],
    get_grid: Callable[[], list],
    get_path_cells: Callable[[], Set[Tuple[int, int]]],
    animate: bool = False,
    animate_delay: float = 0.03,
) -> Optional[MLXUnavailableError]:
    """!
    @brief Opens an MLX window and runs the interactive display loop.
    @param width Maze width in cells.
    @param height Maze height in cells.
    @param entry Entry coordinates.
    @param exit_cell Exit coordinates.
    @param regenerate Callback that regenerates the maze in-place (the
           caller owns the MazeGenerator state); accepts three optional
           keyword arguments: `on_step`, `on_visit` and `on_frontier` --
           used together to animate generation and then solving.
    @param get_grid Zero-argument callback returning the current grid --
           during animation this returns the in-progress grid, since the
           caller updates its live maze reference before generation starts.
    @param get_path_cells Zero-argument callback returning the current
           solution path as a set of coordinates.
    @param animate Bonus: if True, redraw the window as the maze is carved
           and then solved on each regenerate, instead of only once it's
           finished.
    @param animate_delay Seconds paused between animation frames.
    @return None on a normal quit, or the MLXUnavailableError if MiniLibX
            could not be initialised (so the caller can fall back to ASCII).
    """
    try:
        mlx = MLX()
        win = mlx.new_window(width * CELL_SIZE + 1, height * CELL_SIZE + 1, "A-Maze-ing")
    except MLXUnavailableError as exc:
        return exc

    session = MlxSession(
        mlx, win, width, height, entry, exit_cell, regenerate, get_grid,
        get_path_cells, animate, animate_delay,
    )
    session.run()
    return None
