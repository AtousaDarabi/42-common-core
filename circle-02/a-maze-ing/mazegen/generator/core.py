"""The `MazeGenerator` class itself."""

import random
from typing import Callable, List, Optional, Set, Tuple

from ..utils.path_utils import format_path
from ..utils.validation import is_fully_connected
from .dispatch import AlgorithmDispatchMixin
from .loops import LoopMixin
from .pattern import PatternMixin

ALL_WALLS_CLOSED = 15


class MazeGenerator(AlgorithmDispatchMixin, PatternMixin, LoopMixin):
    """!
    @brief Generates and stores a maze grid, reusable across projects.
    @details Instantiate with the desired dimensions, call `generate()` with
             an entry/exit pair, then read `grid` and `get_solution_path()`.
             Behaviour is split across mixins: `AlgorithmDispatchMixin`
             (`dispatch.py`), `PatternMixin` (`pattern.py`) and `LoopMixin`
             (`loops.py`) -- see `state.py` for the shared attribute
             declarations they all rely on.
    """

    def __init__(
        self, w: int, h: int, seed: Optional[int] = None, algorithm: str = "DFS"
    ) -> None:
        """!
        @brief Initializes the MazeGenerator with dimensions and configuration.
        @param w Maze width.
        @param h Maze height.
        @param seed Optional seed for reproducible generation.
        @param algorithm One of "DFS", "KRUSKAL", "PRIM" or "RANDOM".
        @details Every cell starts fully walled (`grid[y][x] == ALL_WALLS_CLOSED`).
                 `self._rng` is a private `random.Random` used only to pick
                 an algorithm for "RANDOM"; the algorithm modules themselves
                 draw from the seeded global `random` module instead.
        """
        self.w, self.h = w, h
        self.grid: List[List[int]] = [
            [ALL_WALLS_CLOSED for _ in range(w)] for _ in range(h)
        ]
        self.visited: List[List[bool]] = [[False for _ in range(w)] for _ in range(h)]
        self.algorithm_flag = algorithm.upper()
        self.solution_coords: List[Tuple[int, int]] = []
        self._blocked_cells: Set[Tuple[int, int]] = set()
        self._rng = random.Random(seed)
        if seed is not None:
            random.seed(seed)

    def generate(
        self,
        entry: Tuple[int, int],
        exit_cell: Tuple[int, int],
        perfect: bool = True,
        on_step: Optional[Callable[[], None]] = None,
        on_visit: Optional[Callable[[Tuple[int, int]], None]] = None,
        on_frontier: Optional[Callable[[Tuple[int, int]], None]] = None,
    ) -> None:
        """!
        @brief Generates the maze using the selected algorithm and
        finds the solution path.
        @param entry Starting coordinates of the maze.
        @param exit_cell Target coordinates of the maze.
        @param perfect If True, the maze is a spanning tree (exactly one path
               between any two cells). If False, extra loop edges are added
               afterward while still respecting the "no 3x3 open area" rule.
        @param on_step Optional zero-argument callback invoked immediately
               after every wall is carved (during both the spanning-tree pass
               and, for imperfect mazes, the extra loop-edge pass), letting a
               caller animate the generation process step by step.
        @param on_visit Optional callback invoked with each cell's (x, y) the
               moment the BFS solver dequeues it and makes it the "current"
               cell being processed (see `algorithms.solver.solve_bfs`).
        @param on_frontier Optional callback invoked with each cell's (x, y)
               the moment the BFS solver discovers and enqueues it, before
               it's actually processed.
        @details After the spanning tree is carved, `is_fully_connected()` is
                 run as a defensive sanity check -- every algorithm should
                 already guarantee full connectivity, but this verifies it
                 before the grid is trusted any further.
        """
        blocked_count = self._apply_42_pattern(entry, exit_cell)
        active_algo = self._resolve_algorithm()
        self._run_spanning_tree(active_algo, entry, blocked_count, on_step)

        if not is_fully_connected(
            self.grid, self.w, self.h, blocked_count
        ):
            raise ValueError(
                "Generated maze is not fully connected; this indicates a bug "
                "in the generation algorithm."
            )

        if not perfect:
            self._add_loop_edges(on_step=on_step)

        from ..algorithms.solver import solve_bfs

        self.solution_coords = solve_bfs(
            self.grid, entry, exit_cell, on_visit, on_frontier
        )

    def get_solution_path(self) -> str:
        """!
        @brief Formats the solution coordinates into a directional string.
        @return A string representing the path (e.g. 'NEESS').
        """
        if not self.solution_coords:
            return ""
        return format_path(self.solution_coords)

    def to_hex_rows(self) -> List[str]:
        """!
        @brief Renders the grid as one hexadecimal string per row.
        @return A list of strings, one per row, one hex digit per cell.
        """
        return [
            "".join(f"{self.grid[y][x]:X}" for x in range(self.w))
            for y in range(self.h)
        ]
