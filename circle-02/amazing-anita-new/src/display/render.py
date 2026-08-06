"""Top-level ASCII maze renderer."""

from typing import List, Optional, Sequence, Tuple

from .canvas import build_canvas, draw_cell_walls
from .cells import fill_cell_interior
from .colors import CELL_W, WALL_CHAR, WALL_COLOR_CODES, sgr


def render_ascii(
    grid: List[List[int]],
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int],
    path: Optional[Sequence[Tuple[int, int]]] = None,
    wall_color: str = "default",
    visited: Optional[Sequence[Tuple[int, int]]] = None,
) -> str:
    """!
    @brief Renders the maze as a block-style ASCII grid: solid coloured
           wall blocks on black, with entry/exit/'42' pattern/path cells
           picked out in their own colour, matching the subject's example.
    @param grid The 2D grid representing wall bitmasks per cell.
    @param width Maze width.
    @param height Maze height.
    @param entry Entry coordinates (x, y), shown as a magenta 'S' cell.
    @param exit_cell Exit coordinates (x, y), shown as a red 'X' cell.
    @param path Optional ordered entry-to-exit solution path. Both the
           cells and the corridor gaps between consecutive cells are
           coloured, so the path reads as one continuous trail rather than
           a series of disconnected dots.
    @param wall_color Key into WALL_COLOR_CODES used for the wall blocks.
    @param visited Optional cells the BFS solver has explored so far (see
           the "animate solving" bonus) -- drawn in a distinct colour from
           `path` so a solve-in-progress frame (no `path` yet) still shows
           the search frontier, without being confused with the eventual
           shortest-path highlight.
    @return The full multi-line string ready to print.
    """
    path = list(path or [])
    path_cells = set(path)
    path_edges = {frozenset((path[i], path[i + 1])) for i in range(len(path) - 1)}
    visited_cells = set(visited or [])

    wall_code = WALL_COLOR_CODES.get(wall_color, WALL_COLOR_CODES["default"])
    wall_slot = sgr(wall_code, WALL_CHAR)
    canvas = build_canvas(width, height, wall_slot)

    for y in range(height):
        for x in range(width):
            row, col = y * 2 + 1, x * (CELL_W + 1) + 1
            draw_cell_walls(canvas, grid, x, y, row, col, wall_slot, path_edges)
            fill_cell_interior(
                canvas, row, col, x, y, grid[y][x], entry, exit_cell,
                path_cells, visited_cells,
            )

    return "\n".join("".join(cell_row) for cell_row in canvas)
