"""Typed representation of a parsed configuration file."""

from dataclasses import dataclass
from typing import Optional, Tuple

REQUIRED_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")


@dataclass
class MazeConfig:
    """!
    @brief Typed representation of a parsed configuration file.
    @param width Maze width, in cells.
    @param height Maze height, in cells.
    @param entry Entry cell coordinates (x, y).
    @param exit_cell Exit cell coordinates (x, y).
    @param output_file Path of the file the maze will be written to.
    @param perfect Whether the maze must have exactly one path entry<->exit.
    @param seed Optional RNG seed for reproducible generation.
    @param algorithm Optional generation algorithm name (DFS/KRUSKAL/PRIM/RANDOM).
    @param display Optional display mode, "ASCII" (default) or "MLX".
    @param animate Optional bonus: animate maze generation step by step
           instead of showing only the finished maze (default True).
    @param animate_delay Optional seconds paused between animation frames
           (default 0.03; ignored if animate is False).
    """

    width: int
    height: int
    entry: Tuple[int, int]
    exit_cell: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    algorithm: str = "DFS"
    display: str = "ASCII"
    animate: bool = True
    animate_delay: float = 0.03
