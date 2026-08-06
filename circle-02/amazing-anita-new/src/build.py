"""Glue: generates a maze via `mazegen` and writes it via `file_writer`."""

from typing import Callable, List, Optional, Tuple

from mazegen import MazeGenerator
from src.config_loader import MazeConfig
from src.file_writer import write_maze_file


def build_and_write(
    config: MazeConfig,
    seed: Optional[int],
    on_maze_created: Optional[Callable[[MazeGenerator], None]] = None,
    on_step: Optional[Callable[[], None]] = None,
    on_visit: Optional[Callable[[Tuple[int, int]], None]] = None,
    on_frontier: Optional[Callable[[Tuple[int, int]], None]] = None,
) -> MazeGenerator:
    """!
    @brief Generates a maze from `config` (optionally overriding the seed)
           and writes the required output file.
    @param config The parsed maze configuration.
    @param seed RNG seed to use for this generation (None for a random one).
    @param on_maze_created Optional callback invoked with the freshly
           constructed (not yet generated) MazeGenerator, before generation
           starts -- lets a caller grab a live reference so it can read
           `.grid` as `on_step` progressively fills it in.
    @param on_step Optional zero-argument callback forwarded to
           `MazeGenerator.generate()` (see there for the bonus "animate
           generation" hook).
    @param on_visit Optional callback forwarded to `MazeGenerator.generate()`,
           invoked with each cell the BFS solver makes "current" (see there
           for the bonus "animate solving" hook).
    @param on_frontier Optional callback forwarded to `MazeGenerator.generate()`,
           invoked with each cell the BFS solver newly discovers/enqueues.
    @return The MazeGenerator instance holding the freshly generated maze.
    """
    maze = MazeGenerator(
        w=config.width, h=config.height, seed=seed, algorithm=config.algorithm
    )
    if on_maze_created is not None:
        on_maze_created(maze)
    maze.generate(
        config.entry, config.exit_cell, perfect=config.perfect,
        on_step=on_step, on_visit=on_visit, on_frontier=on_frontier,
    )
    write_maze_file(
        maze.to_hex_rows(),
        config.entry,
        config.exit_cell,
        maze.get_solution_path(),
        config.output_file,
    )
    return maze


def path_cells_from(maze: MazeGenerator) -> List[Tuple[int, int]]:
    """!
    @brief Returns the solved path as an ordered list of (x, y) coordinates.
    @details Kept in order so the ASCII renderer can colour the corridor
             segments between consecutive steps, not just the cells
             themselves.
    """
    return list(maze.solution_coords)
