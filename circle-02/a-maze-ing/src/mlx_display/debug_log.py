"""Module-level logger for the MLX display.

Uses the standard `logging` pattern for libraries: no handlers or level
are configured here, so this is silent by default. An application (or
the user, for debugging) can opt in with e.g.
`logging.basicConfig(level=logging.DEBUG)` before running the MLX
display, and messages logged via `log` will start showing up.
"""

import logging

log = logging.getLogger(__name__)
