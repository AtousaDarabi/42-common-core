"""The reusable `MazeGenerator`, split across this package.

`state.py` declares the shared instance attributes; `dispatch.py`,
`pattern.py` and `loops.py` are mixins for algorithm dispatch, the '42'
pattern, and extra loop edges (imperfect mazes) respectively; `core.py`
combines them into the public `MazeGenerator` class.
"""

from .core import MazeGenerator

__all__ = ["MazeGenerator"]
