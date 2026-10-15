"""Parser for Fly-in map files."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional, Union

from .models import Connection, MapData, VALID_ZONE_TYPES, Zone

_ZONE_METADATA_KEYS = {"zone", "color", "max_drones"}
_CONNECTION_METADATA_KEYS = {"max_link_capacity"}


class MapParseError(ValueError):
    """Raised when a map file cannot be read or breaks the format."""


@dataclass
class _MapBuilder:
    """Everything collected so far while reading a map."""

    drone_count: Optional[int] = None
    zones: dict[str, Zone] = field(default_factory=dict)
    connections: dict[frozenset[str], Connection] = field(
        default_factory=dict
    )
    start: Optional[str] = None
    end: Optional[str] = None


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
        """Read and validate a map file.

        Raises:
            MapParseError: If the file cannot be read or is invalid.
        """
        try:
            with Path(path).open(encoding="utf-8") as map_file:
                return self.parse_lines(map_file)
        except UnicodeDecodeError as error:
            raise MapParseError(
                f"cannot read '{path}': not a UTF-8 text file"
            ) from error
        except OSError as error:
            reason = error.strerror or str(error)
            raise MapParseError(f"cannot read '{path}': {reason}") from error

    def parse_lines(self, lines: Iterable[str]) -> MapData:
        """Parse map lines, reporting the offending line number."""
        builder = _MapBuilder()
        for line_number, raw_line in enumerate(lines, 1):
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue
            try:
                self._parse_line(line, builder)
            except MapParseError as error:
                raise MapParseError(f"line {line_number}: {error}") from None
        if builder.drone_count is None:
            raise MapParseError("the map does not define nb_drones")
        if builder.start is None:
            raise MapParseError("the map needs exactly one start_hub")
        if builder.end is None:
            raise MapParseError("the map needs exactly one end_hub")
        return MapData(
            builder.drone_count,
            builder.zones,
            builder.connections,
            builder.start,
            builder.end,
        )

    def _parse_line(self, line: str, builder: _MapBuilder) -> None:
        """Dispatch one non-empty, comment-free line."""
        if line.startswith("nb_drones:"):
            if builder.drone_count is not None:
                raise MapParseError("nb_drones is defined more than once")
            value = line.split(":", 1)[1].strip()
            builder.drone_count = self._positive_int(value, "nb_drones")
            return
        if builder.drone_count is None:
            raise MapParseError("the first line must define nb_drones")
        zone_match = self._zone_pattern.match(line)
        if zone_match:
            self._add_zone(zone_match, builder)
            return
        connection_match = self._connection_pattern.match(line)
        if connection_match:
            self._add_connection(connection_match, builder)
            return
        raise MapParseError(f"unrecognized syntax '{line}'")

    def _add_zone(self, match: "re.Match[str]", builder: _MapBuilder) -> None:
        """Validate and store a ``start_hub``, ``end_hub`` or ``hub``."""
        prefix, name, x, y, metadata = match.groups()
        if self._bad_name_pattern.search(name):
            raise MapParseError(
                f"zone name '{name}' must not contain dashes or spaces"
            )
        if name in builder.zones:
            raise MapParseError(f"duplicate zone '{name}'")
        if prefix == "start_hub":
            if builder.start is not None:
                raise MapParseError("more than one start_hub")
            builder.start = name
        elif prefix == "end_hub":
            if builder.end is not None:
                raise MapParseError("more than one end_hub")
            builder.end = name
        builder.zones[name] = self._make_zone(name, int(x), int(y), metadata)

    def _add_connection(
        self, match: "re.Match[str]", builder: _MapBuilder
    ) -> None:
        """Validate and store a connection between two known zones."""
        first, second, metadata = match.groups()
        if first == second:
            raise MapParseError(f"zone '{first}' cannot connect to itself")
        for name in (first, second):
            if name not in builder.zones:
                raise MapParseError(
                    f"connection uses undefined zone '{name}'"
                )
        connection = Connection(first, second, self._capacity(metadata))
        if connection.key in builder.connections:
            raise MapParseError(f"duplicate connection {first}-{second}")
        builder.connections[connection.key] = connection
        builder.zones[first].neighbors.append(second)
        builder.zones[second].neighbors.append(first)

    def _make_zone(
        self, name: str, x: int, y: int, metadata: Optional[str]
    ) -> Zone:
        """Build a zone from its coordinates and metadata."""
        values = self._metadata(metadata)
        unknown = sorted(set(values) - _ZONE_METADATA_KEYS)
        if unknown:
            raise MapParseError(f"unknown zone metadata '{unknown[0]}'")
        kind = values.get("zone", "normal")
        if kind not in VALID_ZONE_TYPES:
            raise MapParseError(f"invalid zone type '{kind}'")
        capacity = self._positive_int(
            values.get("max_drones", "1"), "max_drones"
        )
        return Zone(name, x, y, kind, values.get("color"), capacity)

    @staticmethod
    def _metadata(metadata: Optional[str]) -> dict[str, str]:
        """Parse whitespace-separated ``key=value`` metadata."""
        if not metadata:
            return {}
        values: dict[str, str] = {}
        for item in metadata.split():
            key, separator, value = item.partition("=")
            if not separator or not key or not value:
                raise MapParseError(f"invalid metadata '{item}'")
            if key in values:
                raise MapParseError(f"metadata '{key}' is repeated")
            values[key] = value
        return values

    def _capacity(self, metadata: Optional[str]) -> int:
        """Read a connection capacity from metadata."""
        values = self._metadata(metadata)
        unknown = sorted(set(values) - _CONNECTION_METADATA_KEYS)
        if unknown:
            raise MapParseError(
                f"unknown connection metadata '{unknown[0]}'"
            )
        return self._positive_int(
            values.get("max_link_capacity", "1"), "max_link_capacity"
        )

    @staticmethod
    def _positive_int(value: str, field_name: str) -> int:
        """Convert a positive integer field or raise a useful error."""
        try:
            number = int(value)
        except ValueError:
            raise MapParseError(
                f"{field_name} must be an integer, got '{value}'"
            ) from None
        if number <= 0:
            raise MapParseError(f"{field_name} must be positive, got {number}")
        return number
