from collections import deque
from typing import Callable, List, Optional, Tuple


def solve_bfs(
    grid: List[List[int]],
    start: Tuple[int, int],
    end: Tuple[int, int],
    on_visit: Optional[Callable[[Tuple[int, int]], None]] = None,
    on_frontier: Optional[Callable[[Tuple[int, int]], None]] = None,
) -> List[Tuple[int, int]]:
    """!
    @brief Finds the unique path between two points in a perfect maze
           using BFS.
    @param grid A 2D list where each cell stores wall status as bitmasks.
    @param start The starting coordinate (x, y).
    @param end The destination coordinate (x, y).
    @param on_visit Optional callback invoked with each cell's (x, y) the
           moment it's dequeued and becomes the "current" cell being
           processed, in BFS order -- lets a caller animate/observe the
           search progressing outward from `start`, not just the final path.
    @param on_frontier Optional callback invoked with each cell's (x, y) the
           moment it's discovered and enqueued (including `start` itself,
           before the loop begins) -- lets a caller show the frontier of
           "known but not yet processed" cells, distinct from cells BFS has
           already fully processed (`on_visit`).
    @return A list of coordinates representing the shortest path from start
            to end, or an empty list if no path exists (not expected in a
            connected maze).
    @details BFS is ideal here as it traverses the graph level by level,
             guaranteeing the shortest path in a perfect maze. Each queue
             entry carries the full path taken to reach it. Directions are
             North(0), East(1), South(2), West(3), encoded as (dx, dy, bit).
    """
    queue = deque([(start, [start])])
    visited = {start}
    if on_frontier is not None:
        on_frontier(start)

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    while queue:
        (cx, cy), path = queue.popleft()
        if on_visit is not None:
            on_visit((cx, cy))

        if (cx, cy) == end:
            return path

        directions = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]

        for dx, dy, bit in directions:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < width and 0 <= ny < height:
                if not (grid[cy][cx] & (1 << bit)) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
                    if on_frontier is not None:
                        on_frontier((nx, ny))

    return []
