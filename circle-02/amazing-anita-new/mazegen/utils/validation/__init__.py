"""Structural validation helpers for generated mazes.

These checks enforce the subject's structural constraints that are not
automatically guaranteed by a spanning-tree generation algorithm, in
particular the "no open area wider than 2 cells" rule that only becomes
relevant once extra (loop-creating) edges are added for an imperfect maze.

Split across this package: `open_area.py` (the open-area rule) and
`connectivity.py` (the two BFS reachability checks).
"""

from .connectivity import is_fully_connected, pattern_leaves_maze_connected
from .open_area import creates_oversized_open_area

__all__ = [
    "creates_oversized_open_area",
    "is_fully_connected",
    "pattern_leaves_maze_connected",
]
