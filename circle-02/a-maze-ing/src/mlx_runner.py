"""Runs the MiniLibX graphical display and its interactive loop."""

import sys
from typing import Callable, List, Optional, Set, Tuple

from mazegen import MazeGenerator
from src.build import build_and_write, path_cells_from
from src.config_loader import MazeConfig


def run_mlx(config: MazeConfig, maze: MazeGenerator) -> bool:
    """!
    @brief Runs the MiniLibX graphical display and its interactive loop.
    @param config The parsed maze configuration.
    @param maze The already-generated (and already-written) initial maze.
    @return True if the MLX window ran (and was closed normally); False if
            MiniLibX could not be initialised, so the caller should fall
            back to the ASCII display instead of crashing.
    @details `mlx_display` is imported lazily (inside the function body)
             so ASCII-only runs never need to import MLX bindings.
    """
    from src.mlx_display import run_mlx_display

    state = {"maze": maze}

    def regenerate(
        on_step: Optional[Callable[[], None]] = None,
        on_visit: Optional[Callable[[Tuple[int, int]], None]] = None,
        on_frontier: Optional[Callable[[Tuple[int, int]], None]] = None,
    ) -> None:
        build_and_write(
            config,
            seed=None,
            on_maze_created=lambda m: state.__setitem__("maze", m),
            on_step=on_step,
            on_visit=on_visit,
            on_frontier=on_frontier,
        )

    def get_grid() -> List[List[int]]:
        return state["maze"].grid

    def get_path_cells() -> Set[Tuple[int, int]]:
        return set(path_cells_from(state["maze"]))

    error = run_mlx_display(
        config.width,
        config.height,
        config.entry,
        config.exit_cell,
        regenerate,
        get_grid,
        get_path_cells,
        animate=config.animate,
        animate_delay=config.animate_delay,
    )
    if error is not None:
        print(f"Warning: MLX display unavailable ({error}); "
              "falling back to ASCII.", file=sys.stderr)
        return False
    return True
