# mazegen

A small, dependency-free maze generation and solving library, extracted from
the A-Maze-ing 42 project so it can be reused in other programs.

## Install

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

## Usage

```python
from mazegen import MazeGenerator

# Instantiate: 20x15 maze, reproducible via seed, using the DFS algorithm.
maze = MazeGenerator(w=20, h=15, seed=42, algorithm="DFS")

# Generate: pick entry/exit cells, perfect=True for a single-path maze.
maze.generate(entry=(0, 0), exit_cell=(19, 14), perfect=True)

# Optional: pass on_step to animate/observe generation one carved wall at a
# time (called after every wall removal, including extra loop edges for
# imperfect mazes) -- useful for a caller that wants to redraw progressively
# instead of only once generation is complete.
maze.generate(entry=(0, 0), exit_cell=(19, 14), on_step=lambda: print(maze.grid))

# Optional: pass on_visit/on_frontier to animate/observe the BFS solver
# itself. on_visit fires with each cell (x, y) the instant it's dequeued and
# becomes the "current" cell being processed; on_frontier fires the instant
# a cell is discovered/enqueued, before it's actually processed -- together
# they let a caller distinguish "already processed" / "known but pending" /
# "currently being processed" cells, not just the final path once solving
# is done.
maze.generate(
    entry=(0, 0), exit_cell=(19, 14),
    on_visit=lambda cell: print("current:", cell),
    on_frontier=lambda cell: print("frontier:", cell),
)

# Access the structure: maze.grid[y][x] is a bitmask of closed walls
# (bit 0 = North, 1 = East, 2 = South, 3 = West).
print(maze.grid[0][0])

# Access a solution: the shortest entry -> exit path as N/E/S/W letters,
# or the raw list of (x, y) coordinates via maze.solution_coords.
print(maze.get_solution_path())
```

Supported algorithms: `DFS`, `KRUSKAL`, `PRIM`, or `RANDOM` (picks one of the
three each time `generate()` runs).

Note: the in-memory `grid` structure (a list of rows of wall bitmasks) is
not the same as the project's on-disk output file format — callers that need
that format should encode `grid` themselves (see `to_hex_rows()` for a
convenience helper).
