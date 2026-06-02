"""Generation-animation mixin: redraws the window as the maze is carved."""

import time
from typing import Callable, Optional

from .colors import ALL_WALLS_CLOSED, WALL_COLORS
from .draw import redraw_cell
from .render import render_maze
from .session_base import SessionAttrs


class GenAnimationMixin(SessionAttrs):
    """!
    @brief Provides `make_animate_step()`, the generation-animation bonus hook.
    """

    def make_animate_step(self) -> Optional[Callable[[], None]]:
        """!
        @brief Builds an `on_step` callback that redraws the window as the
               new maze is carved, for the subject's "Add animation during
               maze generation" bonus.
        @return None if animation is disabled; otherwise a zero-argument
                callback suitable for passing as `regenerate(on_step=...)`.
        @details Frames are throttled to roughly 100 total regardless of
                 maze size -- but even so, redrawing the *entire* grid with
                 `render_maze()` on every one of those frames used to take
                 tens of thousands of mlx_pixel_put calls per frame (nearly
                 every cell starts fully walled early in generation), which
                 made the window look frozen/unresponsive for large mazes.
                 Instead, each frame diffs the live grid against a snapshot
                 of what was last drawn and repaints only the handful of
                 cells that actually changed (`draw.redraw_cell`) -- a
                 carved wall only ever touches the two cells it connects, so
                 this is orders of magnitude cheaper than a full redraw. The
                 snapshot starts as a blank, fully-walled canvas (matching
                 every cell's real initial state) so the window visibly
                 resets before carving begins, and so the first diff only
                 picks up genuinely new cuts.
        """
        if not self.animate:
            return None

        width, height = self.width, self.height
        frame_interval = max(1, (width * height) // 100)
        counter = {"n": 0}
        wall_color = WALL_COLORS[self.color_idx]

        prev_grid = [[ALL_WALLS_CLOSED] * width for _ in range(height)]
        render_maze(
            self.mlx, self.win, prev_grid, width, height, self.entry,
            self.exit_cell, set(), wall_color,
        )
        self.mlx.flush()

        def on_step() -> None:
            counter["n"] += 1
            if counter["n"] % frame_interval != 0:
                return
            grid = self.get_grid()
            changed = False
            for y in range(height):
                row, prev_row = grid[y], prev_grid[y]
                for x in range(width):
                    bits = row[x]
                    if bits != prev_row[x]:
                        redraw_cell(
                            self.mlx, self.win, x, y, bits, self.entry,
                            self.exit_cell, wall_color,
                        )
                        prev_row[x] = bits
                        changed = True
            if not changed:
                return
            self.mlx.flush()
            if self.animate_delay > 0:
                time.sleep(self.animate_delay)

        return on_step
