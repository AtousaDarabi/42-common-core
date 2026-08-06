"""Reads the raw KEY=VALUE lines out of a config file."""

from typing import Dict

from .errors import fail


def read_key_value_pairs(filename: str) -> Dict[str, str]:
    """!
    @brief Reads a KEY=VALUE file into a dict, skipping blanks and comments.
    @param filename Path to the KEY=VALUE configuration file.
    @return A dict mapping each key to its (stripped) value string.
    @details Splits each line on the first "=" only, so a literal "=" inside
             the value itself is kept intact.
    """
    config: Dict[str, str] = {}
    try:
        with open(filename, "r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    fail(f"invalid syntax in config line: {line!r}")
                key, val = line.split("=", 1)
                config[key.strip()] = val.strip()
    except OSError as exc:
        fail(f"unable to read configuration file '{filename}': {exc}")
    return config
