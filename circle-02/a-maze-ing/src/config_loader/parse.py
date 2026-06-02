"""Top-level config-file loading/validation entry point."""

from .errors import fail
from .fields import (
    parse_algorithm_and_display, parse_animation, parse_coordinates,
    parse_dimensions, parse_perfect, parse_seed,
)
from .model import REQUIRED_KEYS, MazeConfig
from .raw_parsing import read_key_value_pairs


def parse_config(filename: str) -> MazeConfig:
    """!
    @brief Loads and validates a maze configuration file.
    @param filename Path to the KEY=VALUE configuration file.
    @return A validated MazeConfig instance.
    @details Exits the process with a clear error message on any invalid,
             missing, or out-of-range configuration value, as required by
             the subject ("must never crash unexpectedly"). Required keys
             are checked first so a missing key fails with a clear message
             instead of a raw KeyError; range/consistency checks that need
             several already-parsed values (e.g. entry/exit bounds) run
             last, once every field has been parsed.
    """
    raw = read_key_value_pairs(filename)

    for key in REQUIRED_KEYS:
        if key not in raw:
            fail(f"missing required configuration key: {key}")

    width, height = parse_dimensions(raw)
    entry = parse_coordinates(raw["ENTRY"], "ENTRY")
    exit_cell = parse_coordinates(raw["EXIT"], "EXIT")
    perfect = parse_perfect(raw)
    output_file = raw["OUTPUT_FILE"]
    seed = parse_seed(raw)
    algorithm, display = parse_algorithm_and_display(raw)
    animate, animate_delay = parse_animation(raw)

    if width <= 0 or height <= 0:
        fail("WIDTH and HEIGHT must be positive integers")

    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        fail("ENTRY coordinates are out of bounds")

    if not (0 <= exit_cell[0] < width and 0 <= exit_cell[1] < height):
        fail("EXIT coordinates are out of bounds")

    if entry == exit_cell:
        fail("ENTRY and EXIT must be different cells")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit_cell=exit_cell,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        algorithm=algorithm,
        display=display,
        animate=animate,
        animate_delay=animate_delay,
    )
