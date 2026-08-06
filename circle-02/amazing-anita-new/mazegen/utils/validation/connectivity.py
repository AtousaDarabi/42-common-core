"""BFS connectivity checks used before and after generation."""

from collections import deque
from typing import List, Set, Tuple


def pattern_leaves_maze_connected(
    width: int, height: int, blocked_cells: Set[Tuple[int, int]]
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
    @return True if the reachable component covers width*height - blocked
            cells; if every cell is fully walled (grid value 15), that's
            only valid when the whole maze is blocked.
    @details Starts the BFS flood-fill from any cell with at least one open
             wall (grid value != 15).
    """
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
