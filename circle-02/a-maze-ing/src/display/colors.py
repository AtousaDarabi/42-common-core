"""Colour codes and small formatting helpers for the ASCII display.

ENTRY_BG is magenta, EXIT_BG is red, PATTERN_BG is a light background for
the '42' pattern's closed cells, PATH_BG is cyan for the highlighted
solution trail, and VISITED_BG is blue for cells the solver has explored
so far (see the "animate solving" bonus) -- distinct from PATH_BG so the
final shortest path still stands out once solving finishes. CELL_W is
wider than tall since terminal characters are usually taller than they are
wide, which keeps cells looking roughly square.
"""

WALL_COLOR_CODES = {
    "default": "97",
    "red": "91",
    "green": "92",
    "yellow": "93",
    "blue": "94",
    "magenta": "95",
    "cyan": "96",
}
COLOR_NAMES = list(WALL_COLOR_CODES.keys())

RESET = "\033[0m"
ENTRY_BG = "45"
EXIT_BG = "41"
PATTERN_BG = "47"
PATH_BG = "46"
VISITED_BG = "44"

WALL_CHAR = "█"
CELL_W = 2


def sgr(code: str, text: str) -> str:
    """!
    @brief Wraps `text` in the given SGR colour code, resetting
           immediately after.
    """
    return f"\033[{code}m{text}{RESET}"
