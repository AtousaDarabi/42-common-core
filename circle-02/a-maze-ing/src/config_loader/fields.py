"""Individual KEY=VALUE field parsers used by `parse_config`.

Each parser calls `fail()` (which exits the process) and then re-raises on
invalid input; the `raise` is unreachable at runtime but keeps mypy from
flagging a missing return.
"""

from typing import Dict, Optional, Tuple

from .errors import fail


def parse_dimensions(raw: Dict[str, str]) -> Tuple[int, int]:
    """!
    @brief Parses and validates the WIDTH/HEIGHT keys as integers.
    @param raw The raw KEY=VALUE dict.
    @return The (width, height) pair.
    """
    try:
        width = int(raw["WIDTH"])
        height = int(raw["HEIGHT"])
    except ValueError:
        fail("WIDTH and HEIGHT must be integers")
        raise
    return width, height


def parse_coordinates(value: str, label: str) -> Tuple[int, int]:
    """!
    @brief Parses an "x,y" string into an (x, y) integer coordinate pair.
    @param value The raw "x,y" value string.
    @param label Human-readable field name, used in the error message.
    @return The (x, y) coordinate pair.
    """
    try:
        x_str, y_str = value.split(",")
        return int(x_str), int(y_str)
    except ValueError:
        fail(f"invalid {label} coordinates: {value!r}")
        raise


def parse_perfect(raw: Dict[str, str]) -> bool:
    """!
    @brief Parses the mandatory PERFECT key.
    @param raw The raw KEY=VALUE dict.
    @return True/False for an exact "true"/"false" spelling (case-insensitive).
    @details Any other spelling (typos, "maybe", "1", ...) is treated as a
             configuration error, not a silent default.
    """
    perfect_raw = raw["PERFECT"].strip().lower()
    if perfect_raw not in ("true", "false"):
        fail(f"PERFECT must be True or False, got {raw['PERFECT']!r}")
    return perfect_raw == "true"


def parse_seed(raw: Dict[str, str]) -> Optional[int]:
    """!
    @brief Parses the optional SEED key.
    @param raw The raw KEY=VALUE dict.
    @return The integer seed, or None if SEED is absent or blank (a fresh
            random seed will be used each run).
    """
    if "SEED" not in raw or raw["SEED"] == "":
        return None
    try:
        return int(raw["SEED"])
    except ValueError:
        fail(f"SEED must be an integer, got {raw['SEED']!r}")
        raise


def parse_algorithm_and_display(raw: Dict[str, str]) -> Tuple[str, str]:
    """!
    @brief Parses the optional ALGORITHM/DISPLAY keys.
    @param raw The raw KEY=VALUE dict.
    @return The (algorithm, display) pair, defaulting to ("DFS", "ASCII")
            if omitted or left blank in the config file.
    """
    algorithm = raw.get("ALGORITHM", "DFS").strip().upper() or "DFS"
    display = raw.get("DISPLAY", "ASCII").strip().upper() or "ASCII"
    if display not in ("ASCII", "MLX"):
        fail(f"DISPLAY must be ASCII or MLX, got {display!r}")
    return algorithm, display


def parse_animation(raw: Dict[str, str]) -> Tuple[bool, float]:
    """!
    @brief Parses the optional ANIMATE/ANIMATE_DELAY bonus keys.
    @param raw The raw KEY=VALUE dict.
    @return The (animate, animate_delay) pair, defaulting to (True, 0.03)
            so the "animate maze generation" bonus is visible without extra
            config.
    """
    animate = True
    if "ANIMATE" in raw and raw["ANIMATE"] != "":
        animate_raw = raw["ANIMATE"].strip().lower()
        if animate_raw not in ("true", "false"):
            fail(f"ANIMATE must be True or False, got {raw['ANIMATE']!r}")
        animate = animate_raw == "true"

    animate_delay = 0.03
    if "ANIMATE_DELAY" in raw and raw["ANIMATE_DELAY"] != "":
        try:
            animate_delay = float(raw["ANIMATE_DELAY"])
        except ValueError:
            fail(
                "ANIMATE_DELAY must be a number, "
                f"got {raw['ANIMATE_DELAY']!r}"
            )
        if animate_delay < 0:
            fail("ANIMATE_DELAY must not be negative")
    return animate, animate_delay
