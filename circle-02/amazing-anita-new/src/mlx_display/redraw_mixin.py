"""Redraw-on-demand mixin for `MlxSession`."""

from .colors import WALL_COLORS
from .debug_log import log
from .render import render_maze
from .session_base import SessionAttrs


class RedrawMixin(SessionAttrs):
    """!
    @brief Provides `redraw()`: repaints the whole window from current state.
    """

    def redraw(self) -> None:
        """!
        @brief Repaints the whole window from the current grid/path/colour
               state, then flushes so the new pixels actually reach the
               screen.
        """
        path = self.get_path_cells() if self.show_path else set()
        render_maze(
            self.mlx, self.win, self.get_grid(), self.width, self.height,
            self.entry, self.exit_cell, path, WALL_COLORS[self.color_idx],
        )
        self.mlx.flush()
        log.debug("redraw(): render_maze + flush completed")
