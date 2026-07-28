"""Terminal-animation helpers for the ASCII display's regenerate command."""

import shutil
import sys
import time
from typing import Callable, Dict, Optional

from mazegen import MazeGenerator
from src.config_loader import MazeConfig
from src.display import CELL_W, COLOR_NAMES, render_ascii


def ascii_animation_fits_terminal(config: MazeConfig) -> bool:
    """!
    @brief Checks whether `render_ascii`'s output for this maze is narrower
           than the current terminal, so animation frames won't wrap.
    @details Each animation frame clears the screen and moves the cursor
             back to the top-left, then reprints -- if a row is wider than
             the terminal, it wraps onto the next line instead, so "cursor
             home" no longer lines up with where the previous frame's
             content actually ended up. Repeated over many throttled frames,
             that stacks into unreadable overlapping garbage rather than a
             clean redraw. Skipping animation (and just showing the final
             maze once finished) avoids that entirely.
    """
    canvas_width = config.width * (CELL_W + 1) + 1
    return canvas_width <= shutil.get_terminal_size().columns


def make_animator(
    config: MazeConfig,
    current: Dict[str, MazeGenerator],
    color_idx: Callable[[], int],
) -> Optional[Callable[[], None]]:
    """!
    @brief Builds an `on_step` callback that redraws the in-progress maze in
           the terminal as it's carved, satisfying the subject's "Add
           animation during maze generation" bonus.
    @param config The parsed maze configuration (animate/animate_delay).
    @param current A one-entry {"maze": MazeGenerator} box holding a live
           reference to the maze currently being generated -- a plain local
           variable can't be used here since `on_step` fires *during*
           `build_and_write()`, before its return value could be assigned.
    @param color_idx Zero-argument callback returning the current wall-colour
           index, so the animation matches whatever colour is selected.
    @return None if animation is disabled; otherwise a zero-argument callback
            suitable for `MazeGenerator.generate(on_step=...)`.
    @details Redrawing on literally every single carved wall would be far
             too slow for large mazes (thousands of terminal repaints), so
             frames are throttled to roughly 100 total regardless of maze
             size. Each frame moves the cursor home and clears the screen so
             it overwrites the previous frame instead of scrolling the
             terminal, then renders with an empty solution path since
             generation isn't finished yet.
    """
    if not config.animate:
        return None

    total_cells = config.width * config.height
    frame_interval = max(1, total_cells // 100)
    counter = {"n": 0}

    def on_step() -> None:
        counter["n"] += 1
        if counter["n"] % frame_interval != 0:
            return
        sys.stdout.write("\033[H\033[J")
        sys.stdout.write(
            render_ascii(
                current["maze"].grid,
                config.width,
                config.height,
                config.entry,
                config.exit_cell,
                [],
                COLOR_NAMES[color_idx()],
            )
        )
        sys.stdout.write("\n(generating...)\n")
        sys.stdout.flush()
        if config.animate_delay > 0:
            time.sleep(config.animate_delay)

    return on_step
