*This project has been created as part of the 42 curriculum by adarabi, anmakhov.*

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

### Bonus: animated maze generation and solving

On by default (`ANIMATE=True`) — two phases play out on each **`r`
(regenerate)**, in both display modes:

1. **Generation**: the maze gets carved out wall-by-wall instead of only
   showing the finished result.
2. **Solving**: once generation finishes, the BFS solver's search frontier
   is shown expanding outward from the entry (a distinct colour — blue in
   MLX, blue background in ASCII) until it reaches the exit, followed by the
   final shortest path highlighted as usual.

Set `ANIMATE=False` to turn both off. The very first maze shown at startup
is still generated before the display opens, so it always appears
instantly; only regenerating animates. `ANIMATE_DELAY` controls the pause
between frames (smaller = faster); frames in both phases are automatically
throttled to roughly 100 total regardless of maze size, so large mazes
don't animate for minutes.

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
(including the virtual-environment and archive-building targets); and
implemented the animated generation/solving bonus and the MLX display's
colour palette and BFS frontier/current/trail visualisation. See "Changelog"
below for the itemised list; every change was reviewed and tested before
being committed.

## Submission

- This Git repository *is* the submission — no separate archive/zip. Only
  what's committed here is evaluated during the defense, so double-check
  filenames match exactly what the subject and Makefile expect: `a_maze_ing.py`
  runnable as `python3 a_maze_ing.py config.txt` from the repo root,
  `config.txt`, `Makefile`, `.gitignore`, and this `README.md`.
- `make lint` (`flake8 .` plus the subject's mandated `mypy .` flag set) must
  pass — see [Instructions](#instructions) above; `make lint-strict`
  (`mypy . --strict`) is optional but recommended, and already clean here.
- The Makefile implements every required rule: `install`, `run`, `debug`,
  `clean`, `lint` (and the optional `lint-strict`) — see the subject's
  "Common Instructions" chapter for the exact list.
- **Be ready for a live modification during the defense.** The evaluator may
  ask for a small, quick (a few minutes) change to some part of the project
  — a minor behaviour tweak, a few lines to write or rewrite, an easy
  feature — to confirm real understanding rather than copy-pasted code. This
  is also why the "AI usage" section above matters: per the subject's "AI
  Instructions" chapter, only submit AI-assisted content you fully
  understand and can explain and modify live.
- Peer-evaluation, not just automated grading, decides this project — bring
  the same understanding of `mazegen/`'s algorithms, the config/output file
  formats, and the display layer that's documented throughout this README.

## Algorithm choice

`config.txt` defaults to `ALGORITHM=RANDOM`: every generation (including
each `r` regenerate) picks one of `DFS`, `KRUSKAL`, or `PRIM` at random, so
the maze's look and feel varies from run to run instead of always being the
same shape. All three are fully implemented and can also be pinned
individually via the `ALGORITHM` key if a consistent style is wanted instead:

- `DFS` (recursive backtracker): simple to reason about, and its stack-based
  implementation maps directly onto the maze's structure; produces long,
  winding corridors with few branch points.
- `KRUSKAL`: builds the maze by randomly joining disjoint regions via
  union-find, producing shorter, more uniformly distributed dead ends.
- `PRIM`: grows the maze outward from a random frontier, producing a more
  "organic", irregularly-branching feel.

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

### Roles

| Owner | Area | Files | Responsibilities |
| --- | --- | --- | --- |
| Shared | Project root | `a_maze_ing.py`, `config.txt`, `Makefile`, `README.md`, `pyproject.toml`, `.flake8` | Entry point wiring, default configuration, build/lint/packaging automation, documentation |
| **anmakhov** | Engine — reusable core (`mazegen/`) | `mazegen/__init__.py`, `generator.py`, `algorithms/dfs.py`, `algorithms/kruskal.py`, `algorithms/prim.py`, `algorithms/solver.py`, `utils/grid_ops.py`, `utils/validation.py`, `utils/wall_logic.py`, `utils/graph_math.py`, `utils/patterns.py` | `MazeGenerator` class and package exports; the three generation algorithms (DFS/Kruskal/Prim); grid neighbour lookups and connectivity/open-area validation; wall-removal and spanning-tree math; the '42' pattern placement logic; the BFS shortest-path solver; hex-encoding the grid (`to_hex_rows()`) for file output |
| **adarabi** | Infrastructure & interface (`src/`) | `config_loader.py`, `file_writer.py`, `display.py`, `mlx_bindings.py`, `mlx_display.py` | Reading and validating `config.txt` (mandatory keys, in-bounds coordinates); writing the on-disk output file format; the ASCII terminal display and its `r`/`p`/`c`/`q` interactions; the ctypes MiniLibX bindings; the MLX graphical display, its interactions, and the (bonus) step-by-step animation of generation and solving |

### Planning

The initial split was clean: anmakhov owns `mazegen/` (the algorithm-agnostic
generation/solving engine), adarabi owns `src/` (config parsing, output
writing, and both displays) — mirroring the subject's own separation between
reusable code and project-specific glue. That held for the mandatory part,
but the bonus work (animated generation/solving, the MLX colour palette, the
BFS frontier/current/trail visualisation) needed both sides changing
together: `mazegen/generator.py` and `algorithms/solver.py` had to expose
`on_step`/`on_visit`/`on_frontier` callbacks before `src/display.py` and
`src/mlx_display.py` could use them, so that work was designed and merged as
a unit rather than fully in parallel. Algorithm selection also got revisited
mid-project — briefly changed to always-random, then reverted back to
respecting the `ALGORITHM` config key once we agreed that wasn't what we
wanted — a reminder to settle on a behaviour change before implementing it.

### Retrospective

**What worked well**: the `mazegen`/`src` boundary held up — neither side
needed to reach into the other's internals, only the small set of public
hooks (`MazeGenerator.generate()`'s callbacks, `.grid`, `.get_solution_path()`).
Catching real bugs early — Kruskal ignoring the '42' pattern, the pattern
stranding cells near the grid border, `ENTRY`/`EXIT` landing inside the
pattern and crashing DFS/Prim's spanning-tree check — before they reached
the display layer kept debugging localised instead of spreading into both
halves of the codebase.

**What could improve**: a few rounds of avoidable rework came from testing
and pushing to the shared branch from separate local copies at the same
time, including one force-push that briefly dropped commits from the remote
branch (recovered by merging, but easily avoided by always pulling before
pushing). The MLX colour palette and the generation/solving animation design
also went through several live iterations rather than being sketched out
up front.

### Tools

- **Git/GitHub**, with a feature-branch + pull-request workflow
  (`claude/a-maze-ing-mlx-menu-bljor0` → `main`) rather than committing
  straight to `main`.
- **Claude Code** (Anthropic) as an AI pair-programmer for the refactor, bug
  fixes, and the animation/display bonus work — see "AI usage" above; every
  change was reviewed and tested, and is something we can explain and modify
  live.
- **flake8** and **mypy** (including `--strict`), run via `make lint`/
  `make lint-strict` throughout development, not just before submission.
- A **virtual X server (Xvfb)**, plus scripted X11 key events and
  screenshots, used to test and verify the MLX display's rendering,
  animation, and interactions in an environment without a physical display
  attached.
