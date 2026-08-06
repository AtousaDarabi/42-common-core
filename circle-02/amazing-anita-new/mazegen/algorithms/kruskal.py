import random
from typing import Callable, List, Optional, Set, Tuple

from ..utils.wall_logic import remove_walls
from .union_find import UnionFind


def run_kruskal(
    grid: List[List[int]],
    w: int,
    h: int,
    blocked_cells: Optional[Set[Tuple[int, int]]] = None,
    on_step: Optional[Callable[[], None]] = None,
) -> int:
    """!
    @brief Generates a perfect maze using Kruskal's algorithm.
    @param grid The 2D grid structure to modify.
    @param w Width of the maze.
    @param h Height of the maze.
    @param blocked_cells Cells (e.g. the '42' pattern) that must stay fully
           walled and excluded from the spanning tree.
    @param on_step Optional zero-argument callback invoked immediately after
           each wall is carved, so a caller can animate/observe generation
           in progress (e.g. redraw the maze after every step).
    @return The number of walls carved (spanning-tree edge count).
    @details Builds the full candidate wall list up front (each internal
             wall listed once, from its west/north cell, as bit 1 = East or
             bit 2 = South), skipping any wall touching a blocked ('42'
             pattern) cell so it stays fully closed. Walls are then
             processed in random order, keeping only those that join two
             components not already connected -- via a union-find over each
             cell's flattened `y * w + x` index -- which is what avoids
             creating cycles.
    """
    blocked_cells = blocked_cells or set()
    walls = []
    for y in range(h):
        for x in range(w):
            if (x, y) in blocked_cells:
                continue
            if x < w - 1 and (x + 1, y) not in blocked_cells:
                walls.append(((x, y), (x + 1, y), 1))
            if y < h - 1 and (x, y + 1) not in blocked_cells:
                walls.append(((x, y), (x, y + 1), 2))

    random.shuffle(walls)
    ds = UnionFind(w * h)
    edges = 0

    for (x1, y1), (x2, y2), bit in walls:
        id1, id2 = y1 * w + x1, y2 * w + x2
        if ds.union(id1, id2):
            remove_walls(grid, (x1, y1), (x2, y2), bit)
            edges += 1
            if on_step is not None:
                on_step()

    return edges
