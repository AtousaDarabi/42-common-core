"""Domain objects used by the Fly-in simulation."""

from dataclasses import dataclass, field
from typing import Optional


VALID_ZONE_TYPES = {"normal", "blocked", "restricted", "priority"}
RESTRICTED_COST = 2
NORMAL_COST = 1


@dataclass
class Zone:
    """A map zone that can contain drones."""

    name: str
    x: int
    y: int
    kind: str = "normal"
    color: Optional[str] = None
    capacity: int = 1
    neighbors: list[str] = field(default_factory=list)

    @property
    def movement_cost(self) -> int:
        """Return the number of turns needed to enter this zone."""
        return RESTRICTED_COST if self.is_restricted else NORMAL_COST

    @property
    def blocked(self) -> bool:
        """Return whether drones are forbidden from entering this zone."""
        return self.kind == "blocked"

    @property
    def is_restricted(self) -> bool:
        """Return whether entering this zone takes two turns."""
        return self.kind == "restricted"

    @property
    def is_priority(self) -> bool:
        """Return whether this zone should be preferred when routes tie."""
        return self.kind == "priority"


@dataclass
class Connection:
    """A bidirectional connection between two zones."""

    first: str
    second: str
    capacity: int = 1

    @property
    def key(self) -> frozenset[str]:
        """Return an order-independent key for duplicate detection."""
        return frozenset((self.first, self.second))


@dataclass
class MapData:
    """Complete parsed map: zones, connections, start and end."""

    drone_count: int
    zones: dict[str, Zone]
    connections: dict[frozenset[str], Connection]
    start: str
    end: str

    def connection_between(self, first: str, second: str) -> Connection:
        """Return the connection joining two zones."""
        return self.connections[frozenset((first, second))]

    def has_unlimited_capacity(self, zone: str) -> bool:
        """Return whether a zone ignores max_drones (start and end)."""
        return zone in (self.start, self.end)


@dataclass(frozen=True)
class Move:
    """One action a drone performs during one simulation turn.

    Attributes:
        turn: The simulation turn (1-based) the action happens in.
        token: The output text after ``D<id>-``: a zone name, or
            ``<from>-<to>`` while flying toward a restricted zone.
        origin: The zone the drone was in when the action started.
        destination: The zone the drone is heading to.
        in_flight: True when the drone ends this turn on the
            connection (first half of a restricted move).
    """

    turn: int
    token: str
    origin: str
    destination: str
    in_flight: bool = False

    @property
    def link(self) -> frozenset[str]:
        """Return the key of the connection used by this action."""
        return frozenset((self.origin, self.destination))


@dataclass
class Drone:
    """A drone and the flight plan computed for it."""

    identifier: int
    moves: list[Move] = field(default_factory=list)

    @property
    def label(self) -> str:
        """Return the drone name used in the output, e.g. ``D3``."""
        return f"D{self.identifier}"

    @property
    def arrival_turn(self) -> int:
        """Return the turn in which the drone reaches the end zone."""
        return self.moves[-1].turn if self.moves else 0

    def route(self, start: str) -> list[str]:
        """Return the zones visited, from the start zone to the end."""
        visited = [start]
        for move in self.moves:
            if not move.in_flight:
                visited.append(move.destination)
        return visited
