"""Extra loop-edge carving for imperfect mazes, split out of `generate()`."""

from typing import Callable, Optional

from ..utils.validation import creates_oversized_open_area
from ..utils.wall_logic import remove_walls
from .state import GeneratorAttrs


class LoopMixin(GeneratorAttrs):
    """!
    @brief Provides `_add_loop_edges()`, used by `MazeGenerator.generate()`.
    """

    def _add_loop_edges(
        self,
        density: float = 0.08,
        max_attempts: int = 500,
        on_step: Optional[Callable[[], None]] = None,
    ) -> None:
        """!
        @brief Adds random extra connections to turn the spanning tree into an
               imperfect maze (multiple paths between some cells).
        @param density Fraction of internal walls to attempt to open.
        @param max_attempts Safety cap on the number of candidate walls tried.
        @param on_step Optional zero-argument callback invoked after each
               extra wall is carved (see `generate()`).
        @details Every internal East/South wall (each one listed only once,
                 from its west/north side) is a loop-edge candidate.
                 Candidates that would create a fully open area of 3x3 cells
                 or larger are skipped, keeping the maze within the subject's
                 corridor-width constraint.
        """
        candidates = []
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) in self._blocked_cells:
                    continue
                if x < self.w - 1 and (x + 1, y) not in self._blocked_cells:
                    candidates.append((x, y, x + 1, y, 1))
                if y < self.h - 1 and (x, y + 1) not in self._blocked_cells:
                    candidates.append((x, y, x, y + 1, 2))

        self._rng.shuffle(candidates)
        target = int(len(candidates) * density)
        added = 0
        attempts = 0

        for x1, y1, x2, y2, bit in candidates:
            if added >= target or attempts >= max_attempts:
                break
            attempts += 1
            if self.grid[y1][x1] & (1 << bit):
                if not creates_oversized_open_area(self.grid, x1, y1, x2, y2):
                    remove_walls(self.grid, (x1, y1), (x2, y2), bit)
                    added += 1
                    if on_step is not None:
                        on_step()
