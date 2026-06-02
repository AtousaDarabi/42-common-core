"""The `MlxSession` class: owns all MLX display state for one window."""

from typing import Callable, Set, Tuple

from src.display import print_menu
from src.mlx_bindings import MLX, CLIENT_MESSAGE_EVENT

from .debug_log import log
from .input_handlers import InputMixin


class MlxSession(InputMixin):
    """!
    @brief Owns the MLX window and all mutable display state (`show_path`,
           `color_idx`) for one `run_mlx_display()` call. Behaviour is split
           across mixins: `RedrawMixin`, `GenAnimationMixin`,
           `SolveAnimationMixin` and `InputMixin` (itself combining the
           three) -- see `session_base.py` for the shared attribute
           declarations they all rely on.
    """

    def __init__(
        self,
        mlx: MLX,
        win: int,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_cell: Tuple[int, int],
        regenerate: Callable[..., None],
        get_grid: Callable[[], list],
        get_path_cells: Callable[[], Set[Tuple[int, int]]],
        animate: bool,
        animate_delay: float,
    ) -> None:
        """!
        @brief Stores the window/maze/callback state and sets the initial
               display state (`show_path=True`, `color_idx=0`).
        """
        self.mlx = mlx
        self.win = win
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_cell = exit_cell
        self.regenerate = regenerate
        self.get_grid = get_grid
        self.get_path_cells = get_path_cells
        self.animate = animate
        self.animate_delay = animate_delay
        self.show_path = True
        self.color_idx = 0

    def run(self) -> None:
        """!
        @brief Wires up the key/close hooks, prints the command menu, and
               runs the MLX event loop until the user quits.
        @details `r`/`p`/`c`/`q` (or Escape) mirror the ASCII display's
                 commands: regenerate, toggle path, cycle wall colour, quit.
                 Clicking the window's own X (close) button also quits
                 cleanly -- this is hooked separately from key_hook, since
                 the window manager's close event is not a keypress.
        """
        print_menu()
        self.mlx.key_hook(self.win, self.on_key)
        self.mlx.hook(self.win, CLIENT_MESSAGE_EVENT, 0, self.on_close)
        self.redraw()
        log.debug("entering mlx.loop() now")
        self.mlx.loop()
        log.debug("mlx.loop() has returned -- loop ended normally")

        self.mlx.destroy_window(self.win)
        self.mlx.destroy_display()
