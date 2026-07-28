"""Canvas construction and wall-segment drawing for the ASCII display.

A cell with every wall closed (ALL_WALLS_CLOSED) can only be a '42' pattern
cell -- a real spanning-tree maze guarantees every other cell has at least
one open wall, so this value alone is enough to detect the pattern without
threading extra state through the display layer.
"""

from typing import FrozenSet, List, Set, Tuple

from .colors import CELL_W, PATH_BG, sgr

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
ALL_WALLS_CLOSED = 15

DIRECTIONS = [(NORTH, 0, -1), (EAST, 1, 0), (SOUTH, 0, 1), (WEST, -1, 0)]


def build_canvas(width: int, height: int, wall_slot: str) -> List[List[str]]:
    """!
    @brief Builds a blank canvas with corner posts drawn at every grid-line
           intersection, so the maze reads as one continuous structure.
    """
    canvas_w = width * (CELL_W + 1) + 1
    canvas_h = height * 2 + 1
    canvas: List[List[str]] = [
        [" " for _ in range(canvas_w)] for _ in range(canvas_h)
    ]
    for gy in range(height + 1):
        for gx in range(width + 1):
            canvas[gy * 2][gx * (CELL_W + 1)] = wall_slot
    return canvas


def draw_cell_walls(
    canvas: List[List[str]],
    grid: List[List[int]],
    x: int,
    y: int,
    row: int,
    col: int,
    wall_slot: str,
    path_edges: Set[FrozenSet[Tuple[int, int]]],
) -> None:
    """!
    @brief Draws the four wall/gap segments around cell (x, y) onto `canvas`.
    @details A corridor gap that's part of the solution path is coloured
             too (`path_edges`), so the trail looks continuous through open
             walls, not just through cells.
    """
    bits = grid[y][x]
    for bit, dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        is_open = not (bits & (1 << bit))
        slot = " "
        if is_open and frozenset(((x, y), (nx, ny))) in path_edges:
            slot = sgr(PATH_BG, " ")
        fill = wall_slot if not is_open else slot

        if bit == NORTH:
            for dxx in range(CELL_W):
                canvas[row - 1][col + dxx] = fill
        elif bit == SOUTH:
            for dxx in range(CELL_W):
                canvas[row + 1][col + dxx] = fill
        elif bit == WEST:
            canvas[row][col - 1] = fill
        elif bit == EAST:
            canvas[row][col + CELL_W] = fill
