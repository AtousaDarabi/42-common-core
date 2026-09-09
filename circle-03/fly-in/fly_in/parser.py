"""Parser and validation for Fly-in map files."""

import re
from pathlib import Path

from .models import Connection, Hub, MapData, ZoneType


class MapParseError(ValueError):
    """Raised when a map file is invalid."""


_ALLOWED_METADATA = {"zone", "color", "max_drones", "max_link_capacity"}


def _metadata(content: str) -> dict[str, str]:
    match = re.search(r"\[(.*?)\]", content)
    if match is None:
        if "[" in content or "]" in content:
            raise MapParseError("malformed metadata block")
        return {}

    metadata: dict[str, str] = {}
    for item in match.group(1).split():
        if "=" not in item:
            raise MapParseError(f"metadata item '{item}' must use key=value")
        key, value = item.split("=", 1)
        if not key or not value:
            raise MapParseError("metadata keys and values cannot be empty")
        if key not in _ALLOWED_METADATA:
            raise MapParseError(f"unknown metadata key '{key}'")
        if key in metadata:
            raise MapParseError(f"duplicate metadata key '{key}'")
        metadata[key] = value
    return metadata


def _parse_hub(line: str) -> tuple[Hub, str]:
    prefixes = (("start_hub:", "start"), ("end_hub:", "end"), ("hub:", "hub"))
    for prefix, kind in prefixes:
        if line.startswith(prefix):
            content = line[len(prefix):].strip()
            break
    else:
        raise MapParseError("invalid hub definition")

    parts = content.split()
    if len(parts) < 3:
        raise MapParseError("hub requires a name and two coordinates")
    name = parts[0]
    if "-" in name or " " in name:
        raise MapParseError("hub names cannot contain '-' or spaces")
    try:
        x, y = int(parts[1]), int(parts[2])
    except ValueError as error:
        raise MapParseError("hub coordinates must be integers") from error

    metadata = _metadata(content)
    try:
        zone_type = ZoneType(metadata.get("zone", ZoneType.NORMAL.value))
    except ValueError as error:
        message = f"invalid zone type '{metadata.get('zone')}'"
        raise MapParseError(message) from error
    try:
        max_drones = int(metadata.get("max_drones", "1"))
    except ValueError as error:
        raise MapParseError("max_drones must be an integer") from error
    if max_drones <= 0:
        raise MapParseError("max_drones must be positive")

    return (
        Hub(name, x, y, zone_type, max_drones, metadata.get("color")),
        kind,
    )


def _parse_connection(line: str) -> Connection:
    content = line.removeprefix("connection:").strip()
    parts = content.split()
    if not parts:
        raise MapParseError("connection requires two hub names")
    endpoints = parts[0].split("-")
    if len(endpoints) != 2 or not all(endpoints):
        raise MapParseError("connection must contain exactly two hub names")

    metadata = _metadata(content)
    try:
        capacity = int(metadata.get("max_link_capacity", "1"))
    except ValueError as error:
        raise MapParseError("max_link_capacity must be an integer") from error
    if capacity <= 0:
        raise MapParseError("max_link_capacity must be positive")
    return Connection(endpoints[0], endpoints[1], capacity)


def parse_map_file(file_path: str | Path) -> MapData:
    """Parse and validate a map file."""
    path = Path(file_path)
    if not path.is_file():
        raise MapParseError(f"file not found: {file_path}")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise MapParseError(f"cannot read map: {error}") from error

    data = MapData(0, "", "")
    starts = 0
    ends = 0
    seen: set[tuple[str, str]] = set()

    for line_number, raw_line in enumerate(lines, 1):
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        try:
            if line.startswith("nb_drones:"):
                if data.nb_drones != 0:
                    raise MapParseError("nb_drones may only appear once")
                data.nb_drones = int(line.split(":", 1)[1].strip())
                if data.nb_drones <= 0:
                    raise MapParseError("nb_drones must be positive")
            elif line.startswith(("start_hub:", "end_hub:", "hub:")):
                hub, kind = _parse_hub(line)
                if hub.name in data.hubs:
                    raise MapParseError(f"duplicate hub '{hub.name}'")
                data.hubs[hub.name] = hub
                if kind == "start":
                    starts += 1
                    data.start_hub = hub.name
                elif kind == "end":
                    ends += 1
                    data.end_hub = hub.name
            elif line.startswith("connection:"):
                connection = _parse_connection(line)
                first, second = connection.zone1, connection.zone2
                if first not in data.hubs or second not in data.hubs:
                    raise MapParseError("connection references an unknown hub")
                key = (first, second) if first <= second else (second, first)
                if key in seen:
                    raise MapParseError("duplicate connection")
                seen.add(key)
                data.connections.append(connection)
            else:
                raise MapParseError("unrecognised syntax")
        except (MapParseError, ValueError) as error:
            raise MapParseError(f"line {line_number}: {error}") from error

    if data.nb_drones <= 0:
        raise MapParseError("nb_drones must be a positive integer")
    if starts != 1 or ends != 1:
        raise MapParseError(
            "map must contain exactly one start_hub and end_hub"
        )
    return data
