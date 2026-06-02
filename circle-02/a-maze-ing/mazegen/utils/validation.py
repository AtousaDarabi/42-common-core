"""Structural validation helpers for generated mazes.

These checks enforce the subject's structural constraints that are not
automatically guaranteed by a spanning-tree generation algorithm, in
particular the "no open area wider than 2 cells" rule that only becomes
relevant once extra (loop-creating) edges are added for an imperfect maze.
"""

from typing import List


def _is_open(grid: List[List[int]], x: int, y: int, bit: int) -> bool:
    """Return True if the wall on the given side of cell (x, y) is open."""
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
    @details Every candidate square window that contains the (x1,y1)-(x2,y2)
             edge is checked; only windows touching the newly opened wall can
             possibly change status, so the check stays cheap. The candidate
             wall is temporarily opened (and always restored afterwards,
             regardless of the check's outcome) so the "would create" check
             actually reflects the state *after* opening it -- otherwise the
             one wall that would complete an already-almost-open block is
             never flagged, since it's still closed at check time.
    """
    height = len(grid)
    width = len(grid[0]) if height else 0
    window = max_side + 1

    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    # Determine which bit connects (x1, y1) -> (x2, y2) so we can simulate
    # opening it (dx/dy is always a unit step in exactly one axis, since
    # callers only pass adjacent cells).
    dx, dy = x2 - x1, y2 - y1
    bit = {(0, -1): 0, (1, 0): 1, (0, 1): 2, (-1, 0): 3}[(dx, dy)]
    opp_bit = (bit + 2) % 4

    original_1 = grid[y1][x1]
    original_2 = grid[y2][x2]
    grid[y1][x1] &= ~(1 << bit)
    grid[y2][x2] &= ~(1 << opp_bit)

    try:
        for top in range(max(0, max_y - window + 1), min(min_y, height - window) + 1):
            for left in range(
                max(0, max_x - window + 1), min(min_x, width - window) + 1
            ):
                if top < 0 or left < 0:
                    continue
                if top + window > height or left + window > width:
                    continue
                if _is_block_fully_open(grid, left, top, window):
                    return True
        return False
    finally:
        # Always restore -- this function only *checks*; the caller decides
        # whether to actually call remove_walls() for real.
        grid[y1][x1] = original_1
        grid[y2][x2] = original_2


def _is_block_fully_open(grid: List[List[int]], left: int, top: int, size: int) -> bool:
    """Return True if every internal wall inside the `size`x`size` block
    starting at (left, top) is open (i.e. the block forms one open room)."""
    for y in range(top, top + size):
        for x in range(left, left + size - 1):
            if not _is_open(grid, x, y, 1):
                return False
    for y in range(top, top + size - 1):
        for x in range(left, left + size):
            if not _is_open(grid, x, y, 2):
                return False
    return True


def pattern_leaves_maze_connected(
    width: int, height: int, blocked_cells: "set[tuple[int, int]]"
) -> bool:
    """!
    @brief Checks, before generation, whether removing `blocked_cells` (the
           '42' pattern) from the grid would still leave a single connected
           region of remaining cells.
    @param width Maze width.
    @param height Maze height.
    @param blocked_cells Candidate cells to exclude (kept fully walled).
    @return False if any non-blocked cell would have no non-blocked neighbour
            at all, or if the remaining cells split into more than one
            component -- in both cases no spanning tree covering every
            non-blocked cell is possible, so the pattern must be omitted.
    """
    from collections import deque

    all_cells = {(x, y) for y in range(height) for x in range(width)}
    free_cells = all_cells - blocked_cells
    if not free_cells:
        return True

    start = next(iter(free_cells))
    seen = {start}
    queue = deque([start])
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    while queue:
        cx, cy = queue.popleft()
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if (nx, ny) in free_cells and (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append((nx, ny))
    return len(seen) == len(free_cells)


def is_fully_connected(
    grid: List[List[int]], width: int, height: int, blocked: int
) -> bool:
    """!
    @brief Verifies that every non-blocked cell is reachable from any other,
           used as a sanity check after generation.
    @param grid The 2D grid representing the maze.
    @param width Maze width.
    @param height Maze height.
    @param blocked Number of cells excluded from the maze (e.g. '42' pattern).
    @return True if the reachable component covers width*height - blocked cells.
    """
    from collections import deque

    start = None
    for y in range(height):
        for x in range(width):
            if grid[y][x] != 15:
                start = (x, y)
                break
        if start:
            break
    if start is None:
        return blocked >= width * height

    seen = {start}
    queue = deque([start])
    directions = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]
    while queue:
        cx, cy = queue.popleft()
        for dx, dy, bit in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in seen:
                if not (grid[cy][cx] & (1 << bit)):
                    seen.add((nx, ny))
                    queue.append((nx, ny))
    return len(seen) == width * height - blocked
