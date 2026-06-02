"""Solve-animation mixin: redraws the window as the BFS solver explores it."""

import time
from typing import Callable, Optional, Set, Tuple

from .colors import CURRENT_COLOR, ENTRY_COLOR, EXIT_COLOR, FRONTIER_COLOR, TRAIL_COLOR
from .draw import fill_cell
from .session_base import SessionAttrs


class SolveAnimationMixin(SessionAttrs):
    """!
    @brief Provides `make_solve_animators()`, the solve-animation bonus hook.
    """

    def make_solve_animators(self) -> Tuple[
        Optional[Callable[[Tuple[int, int]], None]],
        Optional[Callable[[Tuple[int, int]], None]],
    ]:
        """!
        @brief Builds the `on_visit`/`on_frontier` callback pair that redraws
               the window as the BFS solver explores it, distinguishing three
               live states -- not just a single flat "visited" colour:
               FRONTIER_COLOR (queued, not processed yet), CURRENT_COLOR (the
               one cell being processed right now), and TRAIL_COLOR (already
               fully processed) -- so the search's progress is legible, not
               just the final shortest-path highlight drawn once solving ends.
        @return `(None, None)` if animation is disabled; otherwise a
                `(on_visit, on_frontier)` pair suitable for passing as
                `regenerate(on_visit=..., on_frontier=...)`. The two share
                state (which cell is "current", which are still "frontier"),
                so they must be built and used together.
        @details Walls are already final by the time solving starts, so
                 unlike `make_animate_step` there's no grid to diff -- each
                 call already names the one cell involved, so it's redrawn
                 directly. Only the flush+sleep pause (not the redraw itself)
                 is throttled, so solving doesn't take longer to animate than
                 generation did. `on_visit` demotes the previously "current"
                 cell to the trail before promoting the new one, updating
                 state before repainting the previous cell so it correctly
                 falls through to TRAIL_COLOR instead of still matching
                 "current".
        """
        if not self.animate:
            return None, None

        total_cells = self.width * self.height
        frame_interval = max(1, total_cells // 100)
        counter = {"n": 0}
        frontier_cells: Set[Tuple[int, int]] = set()
        current_cell: dict = {"cell": None}

        def redraw_cell(cell: Tuple[int, int]) -> None:
            x, y = cell
            if cell == self.entry:
                fill_cell(self.mlx, self.win, x, y, ENTRY_COLOR)
            elif cell == self.exit_cell:
                fill_cell(self.mlx, self.win, x, y, EXIT_COLOR)
            elif cell == current_cell["cell"]:
                fill_cell(self.mlx, self.win, x, y, CURRENT_COLOR)
            elif cell in frontier_cells:
                fill_cell(self.mlx, self.win, x, y, FRONTIER_COLOR)
            else:
                fill_cell(self.mlx, self.win, x, y, TRAIL_COLOR)

        def pace_frame() -> None:
            counter["n"] += 1
            if counter["n"] % frame_interval != 0:
                return
            self.mlx.flush()
            if self.animate_delay > 0:
                time.sleep(self.animate_delay)

        def on_frontier(cell: Tuple[int, int]) -> None:
            frontier_cells.add(cell)
            redraw_cell(cell)
            pace_frame()

        def on_visit(cell: Tuple[int, int]) -> None:
            previous = current_cell["cell"]
            frontier_cells.discard(cell)
            current_cell["cell"] = cell
            if previous is not None:
                redraw_cell(previous)
            redraw_cell(cell)
            pace_frame()

        return on_visit, on_frontier
