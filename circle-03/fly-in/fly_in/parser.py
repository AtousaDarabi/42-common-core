"""Parser for Fly-in map files."""

import re
from pathlib import Path
from typing import Iterable, Optional, Union

from .models import Connection, MapData, VALID_ZONE_TYPES, Zone

_ZONE_METADATA_KEYS = {"zone", "color", "max_drones"}
_CONNECTION_METADATA_KEYS = {"max_link_capacity"}


class MapParseError(ValueError):
    """Raised when a map line does not follow the project format."""


class MapParser:
    """Parse and validate a Fly-in map file."""

    _zone_pattern = re.compile(
        r"^(start_hub|end_hub|hub):\s+(\S+)\s+(-?\d+)\s+"
        r"(-?\d+)(?:\s+\[(.*)\])?$"
    )
    _connection_pattern = re.compile(
        r"^connection:\s+(\S+)-(\S+)(?:\s+\[(.*)\])?$"
    )
    _bad_name_pattern = re.compile(r"[-\s]")

    def parse_file(self, path: Union[str, Path]) -> MapData:
        """Read and validate a map file."""
        with Path(path).open(encoding="utf-8") as map_file:
            return self.parse_lines(map_file)

    def parse_lines(self, lines: Iterable[str]) -> MapData:
        """Parse map lines while reporting the offending line number."""
        drone_count: Optional[int] = None
        zones: dict[str, Zone] = {}
        connections: dict[frozenset[str], Connection] = {}
        start: Optional[str] = None
        end: Optional[str] = None
        first_content_line = True
        for line_number, raw_line in enumerate(lines, 1):
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue
            try:
                if line.startswith("nb_drones:"):
                    if drone_count is not None:
                        raise MapParseError(
                            "nb_drones is defined more than once"
                        )
                    value = line.split(":", 1)[1].strip()
                    drone_count = self._positive_int(value, "nb_drones")
                    first_content_line = False
                    continue
                if first_content_line:
                    raise MapParseError(
                        "the first line must define nb_drones"
                    )
                zone_match = self._zone_pattern.match(line)
                if zone_match:
                    kind_prefix, name, x, y, metadata = zone_match.groups()
                    self._validate_name(name)
                    if name in zones:
                        raise MapParseError(f"duplicate zone '{name}'")
                    zone = self._make_zone(name, int(x), int(y), metadata)
                    zones[name] = zone
                    if kind_prefix == "start_hub":
                        if start is not None:
                            raise MapParseError("more than one start_hub")
                        start = name
                    elif kind_prefix == "end_hub":
                        if end is not None:
                            raise MapParseError("more than one end_hub")
                        end = name
                    continue
                connection_match = self._connection_pattern.match(line)
                if connection_match:
                    first, second, metadata = connection_match.groups()
                    if first not in zones or second not in zones:
                        raise MapParseError(
                            "connection references an undefined zone"
                        )
                    connection = Connection(
                        first, second, self._capacity(metadata)
                    )
                    if connection.key in connections:
                        raise MapParseError("duplicate connection")
                    connections[connection.key] = connection
                    zones[first].neighbors.append(second)
                    zones[second].neighbors.append(first)
                    continue
                raise MapParseError("unrecognized syntax")
            except (ValueError, TypeError) as error:
                if isinstance(error, MapParseError):
                    message = f"line {line_number}: {error}"
                    raise MapParseError(message) from error
                raise MapParseError(f"line {line_number}: {error}") from error
        if drone_count is None or start is None or end is None:
            raise MapParseError(
                "map needs nb_drones, exactly one start_hub and one end_hub"
            )
        return MapData(drone_count, zones, connections, start, end)

    def _validate_name(self, name: str) -> None:
        """Reject zone names containing dashes or whitespace."""
        if self._bad_name_pattern.search(name):
            raise MapParseError(
                f"zone name '{name}' must not contain dashes or spaces"
            )

    def _make_zone(
        self, name: str, x: int, y: int, metadata: Optional[str]
    ) -> Zone:
        """Build a zone from its coordinates and metadata."""
        values = self._metadata(metadata)
        unknown = set(values) - _ZONE_METADATA_KEYS
        if unknown:
            unknown_key = next(iter(unknown))
            raise MapParseError(f"unknown zone metadata '{unknown_key}'")
        kind = values.get("zone", "normal")
        if kind not in VALID_ZONE_TYPES:
            raise MapParseError(f"invalid zone type '{kind}'")
        capacity = self._positive_int(
            values.get("max_drones", "1"), "max_drones"
        )
        return Zone(name, x, y, kind, values.get("color"), capacity)

    @staticmethod
    def _metadata(metadata: Optional[str]) -> dict[str, str]:
        """Parse whitespace-separated key-value metadata."""
        if not metadata:
            return {}
        values: dict[str, str] = {}
        for item in metadata.split():
            if "=" not in item:
                raise MapParseError(f"invalid metadata '{item}'")
            key, value = item.split("=", 1)
            if not key or not value or key in values:
                raise MapParseError("invalid or repeated metadata")
            values[key] = value
        return values

    def _capacity(self, metadata: Optional[str]) -> int:
        """Read a connection capacity from metadata."""
        values = self._metadata(metadata)
        unknown = set(values) - _CONNECTION_METADATA_KEYS
        if unknown:
            unknown_key = next(iter(unknown))
            raise MapParseError(
                f"unknown connection metadata '{unknown_key}'"
            )
        return self._positive_int(
            values.get("max_link_capacity", "1"), "max_link_capacity"
        )

    @staticmethod
    def _positive_int(value: str, field: str) -> int:
        """Convert a positive integer field or raise a useful error."""
        try:
            number = int(value)
        except ValueError as error:
            raise MapParseError(f"{field} must be an integer") from error
        if number <= 0:
            raise MapParseError(f"{field} must be positive")
        return number
