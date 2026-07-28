"""Low-level pixel drawing helpers for the MLX display."""

from typing import Tuple

from src.mlx_bindings import MLX

from .colors import (
    ALL_WALLS_CLOSED, BACKGROUND_COLOR, CELL_SIZE, EAST, ENTRY_COLOR,
    EXIT_COLOR, NORTH, PATTERN_COLOR, SOUTH, WEST,
)


def fill_cell(mlx: MLX, win: int, cx: int, cy: int, color: int) -> None:
    """!
    @brief Fills cell (cx, cy)'s interior (inset by 1px so wall lines
           stay visible).
    """
    x0, y0 = cx * CELL_SIZE + 1, cy * CELL_SIZE + 1
    for dy in range(CELL_SIZE - 2):
        for dx in range(CELL_SIZE - 2):
            mlx.pixel_put(win, x0 + dx, y0 + dy, color)


def draw_wall(
    mlx: MLX, win: int, cx: int, cy: int, side: int, color: int
) -> None:
    """!
    @brief Draws a single wall segment on the given side of cell (cx, cy).
    """
    x0, y0 = cx * CELL_SIZE, cy * CELL_SIZE
    if side == NORTH:
        for dx in range(CELL_SIZE + 1):
            mlx.pixel_put(win, x0 + dx, y0, color)
    elif side == SOUTH:
        for dx in range(CELL_SIZE + 1):
            mlx.pixel_put(win, x0 + dx, y0 + CELL_SIZE, color)
    elif side == WEST:
        for dy in range(CELL_SIZE + 1):
            mlx.pixel_put(win, x0, y0 + dy, color)
    elif side == EAST:
        for dy in range(CELL_SIZE + 1):
            mlx.pixel_put(win, x0 + CELL_SIZE, y0 + dy, color)


def redraw_cell(
    mlx: MLX,
    win: int,
    x: int,
    y: int,
    bits: int,
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int],
    wall_color: int,
) -> None:
    """!
    @brief Repaints a single cell's interior and all four wall edges from
           scratch, based purely on its current bitmask -- no path highlight
           (generation isn't finished yet, so there's nothing to highlight).
    @details Used by the generation-animation step instead of `render.py`'s
             full-grid redraw: since each carved wall only ever changes the
             two cells it connects, repainting just those cells is orders of
             magnitude cheaper than clearing and redrawing the whole window
             on every animation frame (see `gen_animation.make_animate_step`).
             A cell that's neither entry/exit/pattern is filled with
             `BACKGROUND_COLOR`, representing carved-open floor.
    """
    if (x, y) == entry:
        fill_cell(mlx, win, x, y, ENTRY_COLOR)
    elif (x, y) == exit_cell:
        fill_cell(mlx, win, x, y, EXIT_COLOR)
    elif bits == ALL_WALLS_CLOSED:
        fill_cell(mlx, win, x, y, PATTERN_COLOR)
    else:
        fill_cell(mlx, win, x, y, BACKGROUND_COLOR)

    for side in (NORTH, EAST, SOUTH, WEST):
        color = wall_color if bits & (1 << side) else BACKGROUND_COLOR
        draw_wall(mlx, win, x, y, side, color)
