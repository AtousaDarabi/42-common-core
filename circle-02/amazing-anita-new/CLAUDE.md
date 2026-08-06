# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A-Maze-ing: a 42 school project. A Python 3 maze generator/solver that reads
a `KEY=VALUE` config file, generates a maze (perfect or with loops), writes
it to a file in a hex wall-encoding format, and displays it in the terminal
with interactive commands. The maze generation logic is also packaged as a
standalone, pip-installable library (`mazegen`) so it's reusable outside
this project. Full requirements are in `amazing.pdf` (the 42 subject).

## Commands

All commands run through a `.venv` virtual environment managed by the Makefile.

```bash
make venv          # create .venv
make install        # venv + install flake8, mypy, build into it; also
                     # opportunistically runs `make mlx` (warns, doesn't
                     # fail, if gcc/X11 dev headers are missing)
make mlx            # compile vendored MiniLibX (mlx/) into mlx/libmlx.so
make run            # python3 a_maze_ing.py config.txt
make debug          # same, under pdb
make lint           # flake8 . && mypy . (mandatory flag set from the subject)
make lint-strict    # flake8 . && mypy . --strict
make build          # builds mazegen wheel + sdist, copies them to repo root
make archive        # alias for `make build`
make clean          # removes caches, build artifacts, .venv, and mlx/libmlx.so
```

There is no separate lint/type-check config file beyond `.flake8` (max-line-length
100, excludes `mlx/`) and the `[tool.mypy]` table in `pyproject.toml`. There
is no test suite in this submission (the subject lists tests as an optional,
ungraded guideline, not a requirement).

## Architecture

**Two clearly separated layers — do not blur them:**

1. `mazegen/` — the reusable, pip-installable package (built as
   `mazegen-1.0.0-py3-none-any.whl` / `.tar.gz`, committed at the repo
   root). This is the *only* place maze-generation/solving logic should
   live. Its public API is `mazegen.MazeGenerator` (`mazegen/generator/`):
   instantiate with `w, h, seed, algorithm`, call `.generate(entry, exit_cell, perfect)`,
   then read `.grid` (list of rows, each cell a 4-bit wall bitmask: bit0=N,
   bit1=E, bit2=S, bit3=W), `.solution_coords`, `.get_solution_path()`, or
   `.to_hex_rows()`. Every module in this project is kept to roughly
   50-80 lines by splitting along responsibility; oversized modules became
   small packages (a directory with `__init__.py` re-exporting the public
   names) instead of one large file, so import paths from outside the
   package are unaffected.
   - `mazegen/generator/` — the `MazeGenerator` class itself. `state.py`
     declares the instance attributes shared across the mixins below (so
     mypy can see them without duplication); `dispatch.py` resolves
     `RANDOM`/`DFS`/`KRUSKAL`/`PRIM` and calls the matching algorithm
     module; `pattern.py` places the '42' pattern; `loops.py` adds extra
     loop edges for imperfect mazes; `core.py` combines the three mixins
     into `MazeGenerator` (`__init__`, `generate()`, `get_solution_path()`,
     `to_hex_rows()`).
   - `mazegen/algorithms/{dfs,kruskal,prim}.py` — three interchangeable
     spanning-tree generators, selected via the `algorithm` param
     (`DFS`/`KRUSKAL`/`PRIM`/`RANDOM`). Kruskal's `UnionFind` DSU lives in
     its own `mazegen/algorithms/union_find.py`.
   - `mazegen/algorithms/solver.py` — BFS shortest-path solver.
   - `mazegen/utils/` — small single-purpose helpers: `wall_logic.py`
     (remove_walls, the only place that mutates wall bits),
     `grid_ops.py` (neighbor lookup), `graph_math.py` (spanning-tree edge
     math), `patterns.py` (the '42' pattern shape), `path_utils.py`
     (coords -> N/E/S/W string), `validation/` (structural invariants,
     see below — `open_area.py` for the corridor-width rule,
     `connectivity.py` for the two BFS reachability checks).
   - `mazegen/README.md` is the package's own README (used as the wheel's
     long description via `pyproject.toml`'s `readme` field) — keep it in
     sync with the public API if it changes.

2. `src/` — project-specific glue that is *not* part of the reusable package
   and must not be imported by anything under `mazegen/`:
   - `config_loader/` (parses `config.txt` into a typed `MazeConfig`
     — `model.py` for the dataclass, `raw_parsing.py`/`fields.py` for
     per-key parsing, `parse.py` for the public `parse_config` orchestrator).
   - `file_writer.py` (writes the subject's on-disk hex output format —
     distinct from the in-memory `.grid` representation).
   - `display/` (ASCII rendering + wall-colour palette — `colors.py`,
     `canvas.py`/`cells.py` for drawing, `render.py` for the public
     `render_ascii`, `menu.py` for `print_menu`).
   - `mlx_bindings/` (ctypes wrapper around the compiled `mlx/libmlx.so`
     — `constants.py`/`signatures.py` for the ctypes declarations,
     `hooks.py` for event-hook registration, `core.py` for the public
     `MLX` class).
   - `mlx_display/` (MLX graphical renderer + key-hook interactions —
     `colors.py`, `draw.py`/`render.py` for pixel drawing, `session.py`
     and its mixins `redraw_mixin.py`/`gen_animation.py`/
     `solve_animation.py`/`input_handlers.py` for the interactive window
     state, all combined behind the public `run_mlx_display()`).
   - `build.py` (glue: runs `MazeGenerator` and writes the output file —
     `build_and_write()`, used by both display modes' regenerate command).
   - `ascii_animate.py` (terminal animation frame callback for the
     "animate generation" bonus -- ASCII only animates generation, not
     solving; MLX still animates both, see `mlx_display/solve_animation.py`)
     and `ascii_runner.py` (`run_ascii`, the ASCII command loop).
   - `mlx_runner.py` (`run_mlx`, wires `build_and_write` to
     `mlx_display.run_mlx_display`; imports `mlx_display` lazily so
     ASCII-only runs never touch MLX/ctypes).

   `src/__init__.py` makes it an importable package; `a_maze_ing.py`
   imports from it as `from src.config_loader import ...` etc.
   `a_maze_ing.main()` picks ASCII (`run_ascii`) or MLX (`run_mlx`) based
   on the config's `DISPLAY` key; both implement the same `r`/`p`/`c`/`q`
   interactions (typed commands for ASCII, key-hook callbacks for MLX).

3. `a_maze_ing.py` stays at the repo root, *not* inside `src/`, because the
   subject mandates the program be runnable as exactly
   `python3 a_maze_ing.py config.txt` from the repo root — moving it would
   break that literal command. It's now a thin entry point (`main()` plus
   the `if __name__ == "__main__"` guard) that wires `mazegen`
   (generation/solving) and `src` (config, output, display) together; the
   actual logic lives in `src/build.py`, `src/ascii_runner.py` and
   `src/mlx_runner.py`.

**Structural invariants enforced in `mazegen/utils/validation/` and
`mazegen/generator/` — these encode real subject requirements and have
bitten us before, so preserve them when touching generation code:**

- `pattern_leaves_maze_connected()`: before applying the '42' pattern, the
  generator checks that blocking those cells won't strand any remaining
  cell (e.g. a cell against the grid border with all neighbors either
  blocked or out of bounds). If it would, the pattern is silently omitted
  (with a printed warning) rather than producing an invalid/unconnected
  maze. This is why `MazeGenerator._blocked_cells` can be empty even for a
  maze large enough to nominally fit the pattern (`can_fit_pattern()`
  only checks raw size, not placement safety).
- `creates_oversized_open_area()`: when `perfect=False`, extra loop edges
  (`LoopMixin._add_loop_edges`, mixed into `MazeGenerator`) are only added
  if they don't create a fully-open block of 3x3 cells or larger, per the
  subject's corridor-width rule. Perfect (spanning-tree) mazes satisfy this
  automatically since any 2x2+ fully-open block would require a cycle.
- Kruskal (`algorithms/kruskal.py`, DSU in `algorithms/union_find.py`) must
  exclude blocked/pattern cells from its wall list and union-find id space,
  or it will carve straight through the '42' pattern. DFS/Prim exclude them
  implicitly by pre-marking pattern cells as `visited`.

**Seeding**: `MazeGenerator.__init__` seeds the *global* `random` module
(`random.seed(seed)`) because the algorithm modules call `random.choice` /
`random.shuffle` / `random.randrange` directly on the global module, not on
`self._rng`. `self._rng` (a private `random.Random` instance) is only used
for the `RANDOM` algorithm-choice branch. Keep this in mind if adding new
randomized behavior — use the global `random` module for anything that
should be affected by the config's `SEED` key.

**Config file** (`config.txt`): mandatory keys `WIDTH`, `HEIGHT`, `ENTRY`,
`EXIT`, `OUTPUT_FILE`, `PERFECT`; optional `SEED`, `ALGORITHM`, `DISPLAY`
(`ASCII` or `MLX`). All parsing/validation lives in
`config_loader.parse_config` (`src/config_loader/parse.py`), which exits
the process with a clear stderr message on any invalid input (never raises).

**Output file format** (written by `file_writer.write_maze_file`): one hex
digit per cell per row, blank line, then `entry`, `exit`, and the solution
path (`N`/`E`/`S`/`W` string) each on their own line. This is a different
representation from `MazeGenerator.grid` (Python ints) and is intentionally
kept out of the `mazegen` package since it's project-specific.

**`mlx/`** is the vendored, git-cloned MiniLibX C source (`42Paris/minilibx-linux`)
plus its man pages and bundled C test program; it's unrelated to this
project's Python code and is excluded from `flake8`/`mypy` (see `.flake8`
and `[tool.mypy] exclude` in `pyproject.toml`). There is no real pip package
for MiniLibX (`pip install mlx` on PyPI is Apple's unrelated ML framework),
so it must stay a vendored C dependency built via `make mlx`, which compiles
the sources with `-fPIC` into `mlx/libmlx.so` (not the static `.a` the
upstream `./configure` script would produce -- `src/mlx_bindings/core.py`
needs a shared object to `ctypes.CDLL()` at runtime). That build target is best-effort
from `make install` (a missing compiler/X11 headers prints a warning but
doesn't fail the rest of the setup); the ASCII display never depends on it.
Don't lint or package `mlx/` alongside `mazegen`.

**MLX quirks worth knowing if touching `src/mlx_bindings/` /
`src/mlx_display/`:** `mlx_init()` returns NULL instead of raising when
there's no usable X display -- calling any other mlx function with that NULL
pointer segfaults the whole Python process with no traceback, so
`MLX.__init__` (`src/mlx_bindings/core.py`) checks the return value and
raises `MLXUnavailableError` immediately rather than letting that happen;
callers (`src/mlx_runner.run_mlx`) catch it and fall back to ASCII. Also,
despite its name, this MiniLibX version's `mlx_key_hook` binds to X11
`KeyRelease` (not `KeyPress`), and the callback receives an X11 *keysym*
(via `XkbKeycodeToKeysym`), not a raw keycode -- for latin letters these
equal ASCII codes (`r`=114, `p`=112, `c`=99, `q`=113), which is what
`KEY_R`/`KEY_P`/etc. in `src/mlx_display/colors.py` rely on.

## Known TODOs left for the human author

`README.md` has a few `<TODO: ...>` placeholders (42 login, AI-usage
detail, algorithm-choice rationale, team/planning section) that only the
project author can fill in honestly — don't auto-fill these.
