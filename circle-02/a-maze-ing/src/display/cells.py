"""Cell-interior fill logic for the ASCII display."""

from typing import List, Set, Tuple

from .canvas import ALL_WALLS_CLOSED
from .colors import (
    CELL_W,
    ENTRY_BG,
    EXIT_BG,
    PATH_BG,
    PATTERN_BG,
    VISITED_BG,
    sgr,
)


def fill_cell_interior(
    canvas: List[List[str]],
    row: int,
    col: int,
    x: int,
    y: int,
    bits: int,
    entry: Tuple[int, int],
    exit_cell: Tuple[int, int],
    path_cells: Set[Tuple[int, int]],
    visited_cells: Set[Tuple[int, int]],
) -> None:
    """!
    @brief Fills cell (x, y)'s interior.
    @details Priority order: entry/exit, then the '42' pattern (fully-walled
             cells), then the solution path, then cells the solver has
             visited so far (only relevant mid-solve).
    """
    if (x, y) == entry:
        canvas[row][col] = sgr(ENTRY_BG, "S")
        for dxx in range(1, CELL_W):
            canvas[row][col + dxx] = sgr(ENTRY_BG, " ")
    elif (x, y) == exit_cell:
        canvas[row][col] = sgr(EXIT_BG, "X")
        for dxx in range(1, CELL_W):
            canvas[row][col + dxx] = sgr(EXIT_BG, " ")
    elif bits == ALL_WALLS_CLOSED:
        for dxx in range(CELL_W):
            canvas[row][col + dxx] = sgr(PATTERN_BG, " ")
    elif (x, y) in path_cells:
        for dxx in range(CELL_W):
            canvas[row][col + dxx] = sgr(PATH_BG, " ")
    elif (x, y) in visited_cells:
        for dxx in range(CELL_W):
            canvas[row][col + dxx] = sgr(VISITED_BG, " ")
    else:
        for dxx in range(CELL_W):
            canvas[row][col + dxx] = " "
