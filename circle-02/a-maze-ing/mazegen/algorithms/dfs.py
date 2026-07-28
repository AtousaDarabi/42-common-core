import random
from typing import Callable, List, Optional, Tuple
from ..utils.grid_ops import get_unvisited_neighbors
from ..utils.wall_logic import remove_walls
from ..utils.graph_math import get_expected_edges, verify_spanning_tree


def run_dfs(grid: List[List[int]], visited: List[List[bool]],
            start: Tuple[int, int], blocked: int = 0,
            on_step: Optional[Callable[[], None]] = None) -> None:
    """!
    @brief Generates a perfect maze (spanning tree) using Depth-First Search.
    @param grid The 2D grid representing the maze.
    @param visited A 2D array tracking visited cells.
    @param start The starting (x, y) coordinate.
    @param blocked The number of blocked cells (for expected edge calculation).
    @param on_step Optional zero-argument callback invoked immediately after
           each wall is carved, so a caller can animate/observe generation
           in progress (e.g. redraw the maze after every step).
    @details Uses an explicit stack instead of recursion, so generation
             can't hit Python's recursion limit on large mazes. Each step
             carves into a random unvisited neighbour of the cell on top of
             the stack and pushes it, backtracking (popping) once a cell
             has no unvisited neighbours left. A perfect maze is a spanning
             tree, so the final edge count must equal the vertex count
             minus one; that's checked at the end.
    """
    h, w = len(grid), len(grid[0])
    stack = [start]
    edges = 0
    visited[start[1]][start[0]] = True

    while stack:
        cx, cy = stack[-1]
        neighbors = get_unvisited_neighbors(cx, cy, w, h, visited)
        if neighbors:
            nx, ny, direction = random.choice(neighbors)
            remove_walls(grid, (cx, cy), (nx, ny), direction)
            visited[ny][nx] = True
            edges += 1
            stack.append((nx, ny))
            if on_step is not None:
                on_step()
        else:
            stack.pop()

    if not verify_spanning_tree(edges, get_expected_edges(w, h, blocked)):
        raise ValueError("Maze is not a perfect Spanning Tree.")
