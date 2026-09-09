"""Domain models for the Fly-in drone simulator."""

from dataclasses import dataclass, field
from enum import Enum


class ZoneType(str, Enum):
    """Supported zone types."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    @property
    def movement_cost(self) -> int:
        """Return the number of turns required to enter the zone."""
        return 2 if self is ZoneType.RESTRICTED else 1


@dataclass
class Hub:
    """A named zone in the network."""

    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    max_drones: int = 1
    color: str | None = None


@dataclass
class Connection:
    """A bidirectional connection between two hubs."""

    zone1: str
    zone2: str
    max_link_capacity: int = 1


@dataclass
class MapData:
    """A fully parsed drone map."""

    nb_drones: int
    start_hub: str
    end_hub: str
    hubs: dict[str, Hub] = field(default_factory=dict)
    connections: list[Connection] = field(default_factory=list)
