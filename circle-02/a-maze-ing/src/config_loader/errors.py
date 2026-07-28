"""Small error-reporting helper for config parsing."""

import sys


def fail(message: str) -> None:
    """!
    @brief Prints an error to stderr and exits the process with a
           non-zero status.
    """
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)
