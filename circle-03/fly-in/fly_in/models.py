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
        return RESTRICTED_COST if self.kind == "restricted" else NORMAL_COST

    @property
    def blocked(self) -> bool:
        """Return whether drones are forbidden from entering this zone."""
        return self.kind == "blocked"

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

    def name(self) -> str:
        """Return the display name used in simulation output."""
        return f"{self.first}-{self.second}"

    def connects(self, first: str, second: str) -> bool:
        """Return whether this connection joins two given zones."""
        return {self.first, self.second} == {first, second}


@dataclass
class MapData:
    """Complete parsed map and its routing metadata."""

    drone_count: int
    zones: dict[str, Zone]
    connections: dict[frozenset[str], Connection]
    start: str
    end: str

    def add_connection(self, connection: Connection) -> None:
        """Add a connection and update both adjacency lists."""
        self.connections[connection.key] = connection
        self.zones[connection.first].neighbors.append(connection.second)
        self.zones[connection.second].neighbors.append(connection.first)

    def connection_between(self, first: str, second: str) -> Connection:
        """Return the connection joining two zones."""
        return self.connections[frozenset((first, second))]


@dataclass
class Drone:
    """Mutable state for one drone during simulation.

    Unlike a fixed pre-computed route, a drone only remembers where it
    currently is. Its next hop is decided turn by turn by the
    simulation's greedy router, which is what lets different drones end
    up taking different paths through the map.
    """

    identifier: int
    zone: str
    transit_to: Optional[str] = None
    transit_connection: Optional[str] = None
    route: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Seed the travel log with the drone's starting zone."""
        if not self.route:
            self.route = [self.zone]

    def is_delivered(self, end: str) -> bool:
        """Return whether this drone has arrived at the end zone."""
        return self.transit_to is None and self.zone == end

    def arrive(self, destination: str) -> None:
        """Move the drone directly into an adjacent zone."""
        self.zone = destination
        self.route.append(destination)

    def begin_transit(self, destination: str, connection_name: str) -> None:
        """Commit the drone to a two-turn move into a restricted zone."""
        self.transit_to = destination
        self.transit_connection = connection_name

    def complete_transit(self) -> str:
        """Finish an in-flight move and return the drone's new zone."""
        assert self.transit_to is not None
        destination = self.transit_to
        self.zone = destination
        self.route.append(destination)
        self.transit_to = None
        self.transit_connection = None
        return destination
