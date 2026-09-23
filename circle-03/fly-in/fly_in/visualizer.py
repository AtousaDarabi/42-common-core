"""Terminal output helpers for Fly-in.

Zones carry an optional, free-form ``color=`` tag (red, blue, gold,
rainbow, ...). Rather than ignoring it, this visualizer maps whatever
string the map author chose to a real ANSI color -- a fixed table for
common names, and a stable hash-based 256-color fallback for anything
else, so every map's own color scheme actually shows up in the
terminal instead of a generic three-color UI palette.
"""

from typing import Optional

from .models import MapData

RESET = "\033[0m"
BOLD = "\033[1m"

_NAMED_COLORS = {
    "black": "\033[90m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "gray": "\033[37m",
    "grey": "\033[37m",
    "orange": "\033[38;5;208m",
    "purple": "\033[38;5;135m",
    "violet": "\033[38;5;177m",
    "brown": "\033[38;5;130m",
    "maroon": "\033[38;5;88m",
    "darkred": "\033[38;5;124m",
    "gold": "\033[38;5;220m",
    "lime": "\033[38;5;154m",
    "crimson": "\033[38;5;161m",
    "rainbow": "\033[38;5;213m",
}


def _fallback_color(name: str) -> str:
    """Deterministically map an unknown color name to a 256-color code."""
    code = 17 + (sum(ord(char) for char in name) % 214)
    return f"\033[38;5;{code}m"


def color_for(name: Optional[str]) -> str:
    """Return the ANSI escape for a zone's color tag, or no color."""
    if not name:
        return ""
    return _NAMED_COLORS.get(name.lower(), _fallback_color(name.lower()))


class TerminalVisualizer:
    """Render turns with readable, map-defined terminal colors."""

    HEADER = "\033[96m"
    ROUTE = "\033[93m"
    TURN = "\033[92m"

    def __init__(self, plain: bool = False) -> None:
        """Choose colored or plain output."""
        self.plain = plain

    def print_map_summary(self, map_data: MapData) -> None:
        """Print a compact map summary and a per-zone color legend."""
        print(self._color(self.HEADER, "Map loaded"))
        print(f"  drones: {map_data.drone_count}")
        print(f"  route:  {map_data.start} -> {map_data.end}")
        print(f"  zones:  {len(map_data.zones)}")
        for name in sorted(map_data.zones):
            zone = map_data.zones[name]
            label = f"{name} ({zone.kind})"
            if zone.color and not self.plain:
                print(f"    {color_for(zone.color)}{label}{RESET}")
            else:
                print(f"    {label}")

    def print_route(self, path: list[str], cost: int) -> None:
        """Print one example shortest route and its turn cost."""
        heading = self._color(self.ROUTE, "Reference shortest path: ")
        print(f"{heading}{' -> '.join(path)}  (cost {cost} turns)")
        print(
            "  (drones may spread across other equally-short routes "
            "during the run)"
        )

    def print_turns(self, turns: list[str], map_data: MapData) -> None:
        """Print each simulation turn, coloring known destination zones."""
        for number, line in enumerate(turns, 1):
            prefix = self._color(self.TURN, f"turn {number:02d}: ")
            print(prefix + self._colorize_line(line, map_data))

    def print_drone_routes(self, routes: dict[int, list[str]]) -> None:
        """Print the actual path each drone travelled (BONUS)."""
        print(self._color(self.HEADER, "Routes taken:"))
        for identifier in sorted(routes):
            path = " -> ".join(routes[identifier])
            print(f"  D{identifier}: {path}")

    def _colorize_line(self, line: str, map_data: MapData) -> str:
        """Color each move token by its destination zone, if known."""
        if self.plain:
            return line
        tokens = []
        for token in line.split(" "):
            drone_id, _, target = token.partition("-")
            zone = map_data.zones.get(target)
            if zone and zone.color:
                tokens.append(
                    f"{drone_id}-{color_for(zone.color)}{target}{RESET}"
                )
            else:
                tokens.append(token)
        return " ".join(tokens)

    def _color(self, color: str, text: str) -> str:
        """Apply ANSI color unless plain output was requested."""
        if self.plain:
            return text
        return f"{color}{text}{RESET}"
