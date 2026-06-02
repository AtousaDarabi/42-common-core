"""Main entry point: python3 a_maze_ing.py config.txt

Generates a maze from a configuration file, writes it to the configured
output file, and displays it in the terminal with basic interactions.

The actual generation/display logic lives in `src/build.py`,
`src/ascii_runner.py` and `src/mlx_runner.py`; this file stays a thin CLI
entry point at the repo root because the subject mandates the program be
runnable as exactly `python3 a_maze_ing.py config.txt`.
"""

import sys

from src.ascii_runner import run_ascii
from src.build import build_and_write
from src.config_loader import parse_config
from src.mlx_runner import run_mlx


def main() -> None:
    """!
    @brief Program entry point: validates CLI args, generates the maze, and
           runs the interactive display loop (ASCII or MLX per config).
    @details If `run_mlx()` returns False, MiniLibX was unavailable, so
             execution falls through to the ASCII display instead of exiting.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    config = parse_config(sys.argv[1])
    maze = build_and_write(config, config.seed)

    if config.display == "MLX":
        if run_mlx(config, maze):
            return

    run_ascii(config, maze)


if __name__ == "__main__":
    main()
