"""Checks the subject's "no open area wider than 2 cells" rule.

Only becomes relevant once extra (loop-creating) edges are added for an
imperfect maze -- a spanning-tree maze can never violate it on its own.
"""

from typing import List


def _is_open(grid: List[List[int]], x: int, y: int, bit: int) -> bool:
    """!
    @brief Returns True if the wall on the given side of cell (x, y) is open.
    """
    return not (grid[y][x] & (1 << bit))


def creates_oversized_open_area(
    grid: List[List[int]], x1: int, y1: int, x2: int, y2: int, max_side: int = 2
) -> bool:
    """!
    @brief Checks whether opening the wall between two adjacent cells would
           create a fully open rectangular block larger than `max_side` on
           both dimensions (e.g. a 3x3 room).
    @param grid The 2D grid representing the maze (mutated to test the edge).
    @param x1 X coordinate of the first cell.
    @param y1 Y coordinate of the first cell.
    @param x2 X coordinate of the second (adjacent) cell.
    @param y2 Y coordinate of the second (adjacent) cell.
    @param max_side Largest allowed side (in cells) of a fully open square
           block. The subject caps this at 2 (a 2x3 area is fine, 3x3 is not).
    @return True if a (max_side + 1) x (max_side + 1) fully open block would
            exist anywhere in the maze after opening this wall.
    @details Only square windows touching the newly opened (x1,y1)-(x2,y2)
             edge can possibly have changed status, so the search is bound
             to just those top-left offsets, keeping the check cheap.
    """
    height = len(grid)
    width = len(grid[0]) if height else 0
    window = max_side + 1

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    for top in range(max(0, max_y - window + 1), min(min_y, height - window) + 1):
        for left in range(max(0, max_x - window + 1), min(min_x, width - window) + 1):
            if top < 0 or left < 0:
                continue
            if top + window > height or left + window > width:
                continue
            if _is_block_fully_open(grid, left, top, window):
                return True
    return False


def _is_block_fully_open(grid: List[List[int]], left: int, top: int, size: int) -> bool:
    """!
    @brief Returns True if every internal wall inside the `size`x`size`
           block starting at (left, top) is open (i.e. the block forms one
           open room).
    @details Checks East walls (bit 1) between horizontally adjacent cells,
             then South walls (bit 2) between vertically adjacent cells.
    """
    for y in range(top, top + size):
        for x in range(left, left + size - 1):
            if not _is_open(grid, x, y, 1):
                return False
    for y in range(top, top + size - 1):
        for x in range(left, left + size):
            if not _is_open(grid, x, y, 2):
                return False
    return True
