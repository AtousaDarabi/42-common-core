*This project has been created as part of the 42 curriculum by \<TODO: your login(s), e.g. jdoe\>.*

# A-Maze-ing

## Description

A-Maze-ing is a Python 3 maze generator and solver. Given a configuration
file (width, height, entry/exit cells, and a few optional parameters), the
program generates a maze — either "perfect" (exactly one path between the
entry and the exit) or "imperfect" (with a few extra loops) — writes it to a
file using a compact hexadecimal wall encoding, and displays it either in
the terminal (ASCII) or in a graphical window (MiniLibX), with a small set
of interactive commands either way.

Every generated maze also embeds a visible "42" pattern made of fully closed
cells, unless the maze is too small (or the pattern would otherwise strand
cells) to fit it safely, in which case it is omitted with a warning.

## Instructions

```bash
make venv      # creates the .venv virtual environment
make install   # venv + installs dev dependencies (flake8, mypy, build) into it,
               # and opportunistically builds MiniLibX (make mlx) if the system
               # has gcc/X11 dev headers -- ASCII display works either way
make mlx       # compiles the vendored MiniLibX (mlx/) into mlx/libmlx.so;
               # needed only for the MLX graphical display, not the ASCII one
make run       # python3 a_maze_ing.py config.txt (inside the venv)
make debug     # same, under pdb
make lint      # flake8 . && mypy . (mandatory flag set)
make lint-strict
make build     # rebuilds mazegen-*.whl / .tar.gz and copies them to the repo root
make archive   # alias for `make build`
make clean     # removes caches, build artifacts, the venv, and mlx/libmlx.so
```

Run directly:

```bash
python3 a_maze_ing.py config.txt
```

Once running, the maze is displayed (in the terminal, or in an MLX window if
`DISPLAY=MLX` in the config -- see below) and written to the file named by
`OUTPUT_FILE`. The following commands work the same way in both display
modes (typed at the `maze>` prompt for ASCII, or as key presses for MLX):

- `r` — regenerate a new maze (with a fresh random seed) and redisplay it.
- `p` — show/hide the solution path.
- `c` — cycle through wall colours.
- `q` — quit (Escape also works in the MLX window).

### Configuration file format

One `KEY=VALUE` pair per line; lines starting with `#` are comments.

| Key | Description | Example |
| --- | --- | --- |
| `WIDTH` | Maze width, in cells | `WIDTH=20` |
| `HEIGHT` | Maze height, in cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `x,y` | `ENTRY=1,1` |
| `EXIT` | Exit coordinates `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` for a single-path maze, `False` to allow loops | `PERFECT=True` |
| `SEED` (optional) | Integer RNG seed, for reproducible mazes | `SEED=42` |
| `ALGORITHM` (optional) | `DFS`, `KRUSKAL`, `PRIM`, or `RANDOM` | `ALGORITHM=DFS` |
| `DISPLAY` (optional) | `ASCII` (default) or `MLX` (graphical) | `DISPLAY=ASCII` |
| `ANIMATE` (optional) | `True` (default) to animate maze generation, `False` to show only the finished maze | `ANIMATE=True` |
| `ANIMATE_DELAY` (optional) | Seconds paused between animation frames (default `0.03`); ignored if `ANIMATE=False` | `ANIMATE_DELAY=0.02` |

A default `config.txt` is included at the repository root. If `DISPLAY=MLX`
is set but MiniLibX isn't built or no X11 display is available, the program
prints a warning and falls back to the ASCII display instead of crashing.

### Bonus: animated maze generation (and solving, in MLX)

On by default (`ANIMATE=True`) — plays out on each **`r` (regenerate)**:

1. **Generation**: the maze gets carved out wall-by-wall instead of only
   showing the finished result, in both display modes.
2. **Solving** (MLX only): once generation finishes, the BFS solver's
   search frontier is shown expanding outward from the entry in a distinct
   colour until it reaches the exit, followed by the final shortest path
   highlighted as usual. The ASCII display just shows the final shortest
   path once solving completes, without animating the search.

Set `ANIMATE=False` to turn generation animation off. The very first maze
shown at startup is still generated before the display opens, so it always
appears instantly; only regenerating animates. `ANIMATE_DELAY` controls the
pause between frames (smaller = faster); frames are automatically throttled
to roughly 100 total regardless of maze size, so large mazes don't animate
for minutes.

### Output file format

- One line per maze row, one hexadecimal digit per cell. Each digit is a
  4-bit mask of the closed walls of that cell: bit 0 = North, bit 1 = East,
  bit 2 = South, bit 3 = West (e.g. `3` = North and East closed, South and
  West open).
- A blank line, then three lines: entry coordinates (`x,y`), exit
  coordinates (`x,y`), and the shortest entry-to-exit path as a string of
  `N`/`E`/`S`/`W` letters.

## Resources

- [Maze generation algorithms (Wikipedia)](https://en.wikipedia.org/wiki/Maze_generation_algorithm) —
  overview of recursive backtracker (DFS), Kruskal's, and Prim's algorithms
  applied to mazes.
- [Think Labyrinth: Maze algorithms](https://www.astrolog.org/labyrnth/algrithm.htm) —
  practical comparisons of maze algorithms and the shapes/textures they produce.
- Introduction to Algorithms (CLRS) — spanning tree and union-find (disjoint
  set) background used by Kruskal's algorithm.

**AI usage**: Claude (Anthropic) was used to refactor this project against
the subject. Concretely, it: merged two previously disconnected
implementations (ad-hoc top-level scripts and an unused `mazegen/` package)
into the single `mazegen` package now used by `a_maze_ing.py`; added the
missing mandatory features (seed reproducibility, `PERFECT=False` support
with loop edges that respect the "no 3x3 open area" rule, the ASCII terminal
display with regenerate/path-toggle/colour-cycle commands); fixed a real bug
in Kruskal's algorithm (it ignored the '42' pattern and could carve through
cells meant to stay walled off); fixed a structural bug where the '42'
pattern could strand cells with no legal neighbour when placed near the
grid border (now detected and the pattern is safely omitted instead); added
type hints/docstrings throughout and the `flake8`/`mypy` configuration; and
wrote the `pyproject.toml` packaging and this Makefile
(including the virtual-environment and archive-building targets). See
"Changelog" below for the itemised list. \<TODO: add your own AI usage here
too if you used it separately from this session, and be ready to explain any
of the above during your defense.\>

## Changelog (refactor summary)

- Removed the duplicate top-level modules (`maze_generator.py`,
  `maze_solver.py`, `maze_file_saver.py`, `parse_config.py`); `mazegen/` is
  now the only maze-generation code path.
- Fixed Kruskal's algorithm to respect the '42' pattern's blocked cells.
- Fixed a bug where the '42' pattern could isolate cells when placed close
  to the grid border; the generator now checks for this and safely omits
  the pattern (with a warning) instead of producing an invalid maze.
- Added `SEED` and `ALGORITHM` as optional config keys, with reproducible
  generation given a fixed seed.
- Added `PERFECT=False` support: extra loop edges are added after the
  spanning tree, each checked against the "no area wider than 2 cells may be
  fully open" rule before being applied.
- Added `display.py`: ASCII rendering plus `r`/`p`/`c`/`q` terminal
  interactions (regenerate, toggle solution path, cycle wall colour, quit).
- Added full type hints and docstrings across the codebase; the project is
  now `flake8`- and `mypy --disallow-untyped-defs`-clean.
- Added `pyproject.toml` so `mazegen` builds as a standalone wheel/sdist
  (`mazegen-1.0.0-py3-none-any.whl` / `.tar.gz`, committed at the repo root).
- Rewrote the `Makefile` with `venv`/`install`/`run`/`debug`/`lint`/
  `lint-strict`/`build`/`archive`/`clean` targets, all running inside a
  `.venv` virtual environment.
- Split project-specific glue (`config_loader.py`, `file_writer.py`,
  `display.py`) into a `src/` package; `a_maze_ing.py` stays at the repo
  root since the subject requires it be runnable as exactly
  `python3 a_maze_ing.py config.txt`.
- Re-added MiniLibX (`mlx/`, the official `42Paris/minilibx-linux` source)
  as a vendored, git-cloned C dependency built via `make mlx` (there is no
  real pip package for MiniLibX -- `pip install mlx` on PyPI is Apple's
  unrelated ML framework, not graphics). Added `src/mlx_bindings.py` (a
  ctypes wrapper around the compiled `mlx/libmlx.so`) and
  `src/mlx_display.py` (the graphical renderer + `r`/`p`/`c`/`q` key-hook
  interactions), selectable via the new `DISPLAY=MLX` config key, with a
  clean fallback to ASCII if MiniLibX isn't available.
- Fixed a crash where an `ENTRY`/`EXIT` cell landing inside the auto-centred
  '42' pattern would break DFS/Prim's spanning-tree invariant and raise an
  uncaught exception; the pattern now always excludes entry/exit instead.
- Added the "animate maze generation" bonus (subject chapter VIII):
  `MazeGenerator.generate()` takes an optional `on_step` callback fired after
  every wall carved, and both displays use it to animate the `r` (regenerate)
  command, on by default and configurable via the new `ANIMATE`/
  `ANIMATE_DELAY` config keys.
- Extended the animation to the solver too: `generate()` also takes an
  `on_visit` callback fired as `solve_bfs` explores each cell, so both
  displays show the search frontier expanding from entry to exit (not just
  the final shortest-path highlight) before revealing the solution.
- Fixed the MLX display's `flush()` calling the wrong C function
  (`mlx_flush_event`, which only drains input events) instead of
  `mlx_do_sync` (which actually calls `XSync`), which was silently making
  the animation's intermediate frames invisible.
- Removed the solve-search animation from the ASCII display (it now just
  shows the final shortest path once solving completes, same as before the
  solving-animation bonus was added); MLX keeps animating both generation
  and solving.

## Algorithm choice

`config.txt` defaults to `ALGORITHM=DFS` (recursive backtracker): it is
simple to reason about, produces long, winding corridors, and its stack-based
implementation maps directly onto the maze's structure. `KRUSKAL` and `PRIM`
are also implemented and selectable via the `ALGORITHM` key (or `RANDOM` to
pick one of the three each run) — Kruskal tends to produce shorter, more
uniformly distributed dead ends via its random edge/union-find process, while
Prim's frontier-based growth produces mazes with a more "organic",
irregularly-branching feel. \<TODO: adjust this section if you settle on a
different default or want to discuss trade-offs in more depth for your
defense.\>

## Reusable code

The maze generation logic lives entirely in the `mazegen/` package (not the
top-level scripts), so it can be reused standalone in other projects. It
exposes a single `MazeGenerator` class:

```python
from mazegen import MazeGenerator

maze = MazeGenerator(w=20, h=15, seed=42, algorithm="DFS")
maze.generate(entry=(0, 0), exit_cell=(19, 14), perfect=True)

maze.grid                 # list of rows; each cell is a 4-bit wall bitmask
maze.get_solution_path()  # e.g. "EESS..." shortest path from entry to exit
maze.solution_coords      # the same path as a list of (x, y) coordinates
```

Note that `maze.grid` is the in-memory structure, not the same format as the
project's on-disk output file (see `to_hex_rows()` for that conversion).

The package is built as a standalone, pip-installable artifact:
`mazegen-1.0.0-py3-none-any.whl` / `mazegen-1.0.0.tar.gz`, committed at the
repository root and rebuildable via `make build` (or `make archive`; both use
the `pyproject.toml` at the repo root, inside the `.venv` virtual
environment).

### Project layout

```
amazing/
├── a_maze_ing.py        # entry point (must stay at repo root, see Usage)
├── config.txt            # default configuration file
├── mazegen/               # reusable package (the only pip-installable part)
├── src/                   # project-specific glue, not part of the package
│   ├── config_loader.py   # parses config.txt into a typed MazeConfig
│   ├── file_writer.py     # writes the subject's on-disk hex output format
│   ├── display.py         # ASCII rendering + terminal interactions
│   ├── mlx_bindings.py    # ctypes wrapper around the compiled mlx/libmlx.so
│   └── mlx_display.py     # MLX graphical rendering + key-hook interactions
├── mazegen-1.0.0-py3-none-any.whl / .tar.gz   # built package archives
├── pyproject.toml, Makefile, .flake8, requirements-dev.txt
└── mlx/                   # vendored MiniLibX C source; `make mlx` compiles
                            # it into mlx/libmlx.so (not committed, see .gitignore)
```

`a_maze_ing.py` imports from both `mazegen` (generation/solving) and `src`
(config parsing, file output, display) — none of which the reusable package
depends on in the other direction.

## Team and project management

\<TODO: fill in for your team/solo submission —\>

- **Roles**: who worked on generation, solving, display, packaging, docs, etc.
- **Planning**: how you originally planned to split the work and how that
  changed as you went.
- **Retrospective**: what worked well, what you'd do differently next time.
- **Tools**: any specific tools (beyond the ones listed in Resources/AI
  usage) that shaped how you worked — pair programming setup, issue tracker,
  CI, etc.
