"""Runs the ASCII terminal display and its interactive command loop."""

import shutil

from mazegen import MazeGenerator
from src.ascii_animate import ascii_animation_fits_terminal, make_animator
from src.build import build_and_write, path_cells_from
from src.config_loader import MazeConfig
from src.display import CELL_W, COLOR_NAMES, print_menu, render_ascii


def run_ascii(config: MazeConfig, maze: MazeGenerator) -> None:
    """!
    @brief Runs the ASCII terminal display and its interactive command loop.
    @param config The parsed maze configuration.
    @param maze The already-generated (and already-written) initial maze.
    @details Ctrl-D/Ctrl-C on the `maze>` prompt exits the loop cleanly
             instead of raising a traceback.
    """
    state = {"show_path": True, "color_idx": 0}
    current = {"maze": maze}

    def render() -> str:
        path = path_cells_from(current["maze"]) if state["show_path"] else []
        return render_ascii(
            current["maze"].grid,
            config.width,
            config.height,
            config.entry,
            config.exit_cell,
            path,
            COLOR_NAMES[state["color_idx"]],
        )

    print(render())
    print(f"Solution path: {current['maze'].get_solution_path()}")
    print(f"Maze written to '{config.output_file}'.")
    print_menu()

    while True:
        try:
            command = input("maze> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if command == "q":
            break
        elif command == "r":
            if config.animate and not ascii_animation_fits_terminal(config):
                canvas_width = config.width * (CELL_W + 1) + 1
                print(
                    f"Note: maze render is {canvas_width} columns wide, "
                    f"wider than your "
                    f"{shutil.get_terminal_size().columns}-column terminal "
                    "-- skipping animation this time to avoid corrupting "
                    "the display (the finished maze will still show "
                    "normally)."
                )
                on_step = None
            else:
                on_step = make_animator(
                    config, current, lambda: state["color_idx"]
                )
            build_and_write(
                config, seed=None,
                on_maze_created=lambda m: current.__setitem__("maze", m),
                on_step=on_step,
            )
            print(render())
            print(f"Solution path: {current['maze'].get_solution_path()}")
            print(f"Maze written to '{config.output_file}'.")
        elif command == "p":
            state["show_path"] = not state["show_path"]
            print(render())
        elif command == "c":
            state["color_idx"] = (state["color_idx"] + 1) % len(COLOR_NAMES)
            print(render())
        else:
            print("Unknown command.")
            print_menu()
