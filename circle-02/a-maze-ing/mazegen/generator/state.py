"""Shared instance-attribute declarations for the MazeGenerator mixins."""

import random
from typing import List, Set, Tuple


class GeneratorAttrs:
    """!
    @brief Declares the instance attributes shared by every `MazeGenerator`
           mixin, so mypy knows about them without each mixin redeclaring
           its own copy.
    @details `MazeGenerator` (see `core.py`) is the only class that
             actually sets these, in `__init__`.
    """

    w: int
    h: int
    grid: List[List[int]]
    visited: List[List[bool]]
    algorithm_flag: str
    solution_coords: List[Tuple[int, int]]
    _blocked_cells: Set[Tuple[int, int]]
    _rng: random.Random
