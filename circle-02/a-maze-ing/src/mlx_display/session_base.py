"""Shared attribute declarations for the MLX display session mixins."""

from typing import Callable, List, Set, Tuple

from src.mlx_bindings import MLX


class SessionAttrs:
    """!
    @brief Declares the instance attributes shared by every `MlxSession`
           mixin, so mypy knows about them without each mixin redeclaring
           its own copy.
    @details `MlxSession` (see `session.py`) is the only class that
             actually sets these, in `__init__`; the mixins in
             `redraw_mixin.py`, `gen_animation.py`, `solve_animation.py`
             and `input_handlers.py` only read (or, for `show_path`/
             `color_idx`, also write) them.
    """

    mlx: MLX
    win: int
    width: int
    height: int
    entry: Tuple[int, int]
    exit_cell: Tuple[int, int]
    regenerate: Callable[..., None]
    get_grid: Callable[[], List[List[int]]]
    get_path_cells: Callable[[], Set[Tuple[int, int]]]
    animate: bool
    animate_delay: float
    show_path: bool
    color_idx: int
