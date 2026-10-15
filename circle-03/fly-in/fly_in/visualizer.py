"""Terminal output for Fly-in.

Two views are offered:

* the default view prints exactly the subject's output format, one line
  per turn (``D1-roof1 D2-corridorA``), with each destination zone
  painted in the color given by its ``color=`` tag when writing to a
  terminal;
* ``--visual`` adds a dashboard around it: a zone legend with types and
  capacities, the reference shortest route, and after every turn the
  state of each occupied zone (a capacity bar), the drones still in
  flight toward restricted zones, and the delivery progress.

Zone colors are free-form words. Common names map to fixed ANSI codes;
any other word gets a stable 256-color code derived from its letters,
so every map's own color scheme shows up instead of a fixed palette.
"""

from typing import Optional

from .models import Drone, MapData
from .pathfinder import RouteInfo
from .simulation import TurnRecord

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"


class ColorPalette:
    """Translate map color names into ANSI escape sequences."""

    NAMED = {
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

    @classmethod
    def code_for(cls, name: Optional[str]) -> str:
        """Return the ANSI escape for a color tag ('' for no color)."""
        if not name:
            return ""
        normalized = name.lower()
        if normalized in cls.NAMED:
            return cls.NAMED[normalized]
        return cls._fallback(normalized)

    @staticmethod
    def _fallback(name: str) -> str:
        """Deterministically map an unknown name to a 256-color code."""
        code = 17 + (sum(ord(char) for char in name) % 214)
        return f"\033[38;5;{code}m"


class TerminalVisualizer:
    """Render the simulation as plain lines or as a colored dashboard."""

    def __init__(self, map_data: MapData, color: bool) -> None:
        """Choose the map to describe and whether to emit ANSI colors."""
        self.map_data = map_data
        self.color = color

    def paint(self, code: str, text: str) -> str:
        """Wrap text in an ANSI code when colors are enabled."""
        if not self.color or not code:
            return text
        return f"{code}{text}{RESET}"

    def zone(self, name: str) -> str:
        """Return a zone name painted in its own map color."""
        zone = self.map_data.zones.get(name)
        color = zone.color if zone else None
        return self.paint(ColorPalette.code_for(color), name)

    def turn_line(self, record: TurnRecord) -> str:
        """Return one turn in the subject's format, zones colored."""
        if not self.color:
            return record.line
        painted = []
        for token in record.moves:
            drone, _, target = token.partition("-")
            if target in self.map_data.zones:
                painted.append(f"{drone}-{self.zone(target)}")
            else:
                origin, _, destination = target.partition("-")
                painted.append(
                    f"{drone}-{self.zone(origin)}-{self.zone(destination)}"
                )
        return " ".join(painted)

    def print_turns(self, records: list[TurnRecord]) -> None:
        """Print the simulation output: one line per turn, nothing else."""
        for record in records:
            print(self.turn_line(record))

    def print_dashboard(
        self, route_info: RouteInfo, records: list[TurnRecord]
    ) -> None:
        """Print the full ``--visual`` view of the simulation."""
        self._print_header(route_info)
        total = self.map_data.drone_count
        for record in records:
            title = self.paint(BOLD, f"Turn {record.number:>3}")
            print(f"{title} | {self.turn_line(record)}")
            print(f"{'':8}| {self._zone_states(record)}")
            if record.in_flight:
                flights = ", ".join(
                    f"{drone} {self.zone(origin)}->{self.zone(target)}"
                    for drone, origin, target in record.in_flight
                )
                print(f"{'':8}| in flight: {flights}")
            print(f"{'':8}| delivered {record.delivered}/{total}")
        summary = f"All {total} drones delivered in {len(records)} turns."
        print(self.paint(BOLD, summary))

    def print_routes(self, drones: list[Drone]) -> None:
        """Print the full route each drone flew."""
        print(self.paint(BOLD, "Routes taken:"))
        for drone in drones:
            route = " -> ".join(
                self.zone(name) for name in drone.route(self.map_data.start)
            )
            print(f"  {drone.label} (arrives turn {drone.arrival_turn}): "
                  f"{route}")

    def print_statistics(self, statistics: dict[str, float | int]) -> None:
        """Print the secondary performance metrics."""
        print(self.paint(BOLD, "Statistics:"))
        for key, value in statistics.items():
            print(f"  {key.replace('_', ' ')}: {value}")

    def _print_header(self, route_info: RouteInfo) -> None:
        """Print the map overview and the zone legend."""
        data = self.map_data
        print(self.paint(BOLD, "Fly-in simulation"))
        print(f"  drones: {data.drone_count}   zones: {len(data.zones)}   "
              f"connections: {len(data.connections)}")
        print(f"  from {self.zone(data.start)} to {self.zone(data.end)}")
        print(self.paint(BOLD, "Zones:"))
        for name in sorted(data.zones):
            zone = data.zones[name]
            capacity = (
                "unlimited" if data.has_unlimited_capacity(name)
                else f"max {zone.capacity}"
            )
            role = (
                " (start)" if name == data.start
                else " (end)" if name == data.end else ""
            )
            print(f"  {self.zone(name)}{role}: {zone.kind}, {capacity}")
        path = " -> ".join(
            self.zone(name) for name in route_info.reference_path
        )
        print(self.paint(BOLD, "Shortest route: ") + path
              + f" ({route_info.reference_cost} turns for one drone)")
        print()

    def _zone_states(self, record: TurnRecord) -> str:
        """Describe every occupied zone with a small capacity bar."""
        data = self.map_data
        parts = []
        for name in sorted(record.occupancy):
            count = record.occupancy[name]
            if data.has_unlimited_capacity(name):
                parts.append(f"{self.zone(name)} {count}")
                continue
            capacity = data.zones[name].capacity
            if capacity <= 8:
                bar = "#" * count + "." * (capacity - count)
                parts.append(f"{self.zone(name)} [{bar}]")
            else:
                parts.append(f"{self.zone(name)} {count}/{capacity}")
        return "  ".join(parts) if parts else self.paint(DIM, "(all clear)")
