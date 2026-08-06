"""Full-grid MLX maze rendering."""

from typing import List, Set, Tuple

from src.mlx_bindings import MLX

from .colors import (
    ALL_WALLS_CLOSED, EAST, ENTRY_COLOR, EXIT_COLOR, NORTH, PATH_COLOR,
    PATTERN_COLOR, SOUTH, WEST,
)
from .draw import draw_wall, fill_cell


def render_maze(
    mlx: MLX,
    win: int,
    grid: List[List[int]],
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int],
    path_cells: Set[Tuple[int, int]],
    wall_color: int,
) -> None:
    """!
    @brief Draws the full maze (walls, entry, exit, solution path) into the
           MLX window.
    @param mlx The MLX binding instance.
    @param win The window handle returned by `mlx.new_window`.
    @param grid The maze's wall-bitmask grid.
    @param width Maze width in cells.
    @param height Maze height in cells.
    @param entry Entry coordinates (x, y).
    @param exit_cell Exit coordinates (x, y).
    @param path_cells Cells to highlight as the solution path (may be empty).
    @param wall_color Packed 0xRRGGBB colour used for walls.
    @details Fill priority mirrors `src/display/` exactly, so both display
             modes look identical: entry/exit first, then the '42' pattern
             (fully-walled cells), then the solution path, then walls drawn
             on top of everything.
    """
    mlx.clear_window(win)
    for y in range(height):
        for x in range(width):
            bits = grid[y][x]
            if (x, y) == entry:
                fill_cell(mlx, win, x, y, ENTRY_COLOR)
            elif (x, y) == exit_cell:
                fill_cell(mlx, win, x, y, EXIT_COLOR)
            elif bits == ALL_WALLS_CLOSED:
                fill_cell(mlx, win, x, y, PATTERN_COLOR)
            elif (x, y) in path_cells:
                fill_cell(mlx, win, x, y, PATH_COLOR)

    for y in range(height):
        for x in range(width):
            bits = grid[y][x]
            if bits & (1 << NORTH):
                draw_wall(mlx, win, x, y, NORTH, wall_color)
            if bits & (1 << SOUTH):
                draw_wall(mlx, win, x, y, SOUTH, wall_color)
            if bits & (1 << WEST):
                draw_wall(mlx, win, x, y, WEST, wall_color)
            if bits & (1 << EAST):
                draw_wall(mlx, win, x, y, EAST, wall_color)
