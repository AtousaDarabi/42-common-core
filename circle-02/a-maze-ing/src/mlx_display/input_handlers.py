"""Keyboard/window-close handling mixin for `MlxSession`."""

from .colors import KEY_C, KEY_ESCAPE, KEY_P, KEY_Q, KEY_R, WALL_COLORS
from .debug_log import log
from .gen_animation import GenAnimationMixin
from .redraw_mixin import RedrawMixin
from .solve_animation import SolveAnimationMixin


class InputMixin(GenAnimationMixin, SolveAnimationMixin, RedrawMixin):
    """!
    @brief Provides `on_key()`/`on_close()`, the window's event-hook callbacks.
    """

    def on_key(self, keysym: int) -> None:
        """!
        @brief Handles a key release: mirrors the ASCII display's r/p/c/q
               commands (see `src/display/`).
        @details Wrapped in a broad `except Exception` because ctypes
                 callbacks can otherwise swallow exceptions silently
                 (Python prints "Exception ignored" at best, or nothing at
                 all depending on version) -- logging it here makes a bug
                 impossible to miss.
        """
        try:
            if keysym in (KEY_Q, KEY_ESCAPE):
                self.mlx.loop_end()
            elif keysym == KEY_R:
                solve_on_visit, solve_on_frontier = self.make_solve_animators()
                self.regenerate(
                    on_step=self.make_animate_step(),
                    on_visit=solve_on_visit,
                    on_frontier=solve_on_frontier,
                )
                self.redraw()
            elif keysym == KEY_P:
                self.show_path = not self.show_path
                self.redraw()
            elif keysym == KEY_C:
                self.color_idx = (self.color_idx + 1) % len(WALL_COLORS)
                self.redraw()
        except Exception:
            log.exception("EXCEPTION inside on_key")

    def on_close(self) -> None:
        """!
        @brief Handles the window's own X (close) button.
        @details Hooked separately from `on_key` since the window manager's
                 close click is not a keypress -- `mlx_key_hook` alone
                 leaves that button doing nothing.
        """
        self.mlx.loop_end()
