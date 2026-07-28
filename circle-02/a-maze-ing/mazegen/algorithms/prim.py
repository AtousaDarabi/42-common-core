import random
from typing import Callable, List, Optional, Tuple
from ..utils.grid_ops import get_unvisited_neighbors
from ..utils.wall_logic import remove_walls
from ..utils.graph_math import get_expected_edges, verify_spanning_tree


def run_prim(
    grid: List[List[int]],
    visited: List[List[bool]],
    start: Tuple[int, int],
    blocked: int = 0,
    on_step: Optional[Callable[[], None]] = None,
) -> None:
    """!
    @brief Generates a maze using Prim's algorithm to create a spanning tree.
    @param grid The 2D grid structure.
    @param visited A 2D boolean array to track visited cells.
    @param start The starting (x, y) coordinate.
    @param blocked The number of blocked cells to be excluded.
    @param on_step Optional zero-argument callback invoked immediately after
           each wall is carved, so a caller can animate/observe generation
           in progress (e.g. redraw the maze after every step).
    @return None.
    @details Maintains a frontier of candidate edges (cx, cy, nx, ny, bit)
             from an already-visited cell to an as-yet-unvisited neighbour,
             picking a random one on each step (rather than first/last) so
             the maze grows outward instead of in DFS-like straight lines.
             A frontier edge is skipped if its neighbour was already
             visited via a different edge, to avoid creating a cycle. A
             perfect maze must end with exactly |V| - 1 edges; that's
             checked at the end.
    """
    h = len(grid)
    w = len(grid[0])

    frontier: List[Tuple[int, int, int, int, int]] = []
    visited[start[1]][start[0]] = True
    edge_count = 0

    for nx, ny, bit in get_unvisited_neighbors(
        start[0], start[1], w, h, visited
    ):
        frontier.append((start[0], start[1], nx, ny, bit))

    while frontier:
        idx = random.randrange(len(frontier))
        cx, cy, nx, ny, bit = frontier.pop(idx)

        if not visited[ny][nx]:
            remove_walls(grid, (cx, cy), (nx, ny), bit)
            visited[ny][nx] = True
            edge_count += 1
            if on_step is not None:
                on_step()

            for nnx, nny, nbit in get_unvisited_neighbors(
                nx, ny, w, h, visited
            ):
                frontier.append((nx, ny, nnx, nny, nbit))

    expected = get_expected_edges(w, h, blocked)
    if not verify_spanning_tree(edge_count, expected):
        raise ValueError(
            "Prim's algorithm failed to generate a perfect spanning tree."
        )
