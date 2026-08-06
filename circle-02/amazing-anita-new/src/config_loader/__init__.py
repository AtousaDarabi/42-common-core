"""Parses the KEY=VALUE configuration file used by a_maze_ing.py.

Split across this package: `model.py` (`MazeConfig`, `REQUIRED_KEYS`),
`errors.py` (`fail`), `raw_parsing.py` (reads the file into a dict),
`fields.py` (per-key parsing/validation), `parse.py` (`parse_config`, the
public orchestrator).
"""

from .model import MazeConfig
from .parse import parse_config

__all__ = ["MazeConfig", "parse_config"]
