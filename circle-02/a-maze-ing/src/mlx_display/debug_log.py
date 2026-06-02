"""TEMP diagnostics logger for the MLX display.

Everything also goes to this file, so nothing is lost to terminal
scrollback/buffering. Remove this whole module once the close/regenerate
issue is confirmed fixed.
"""

import logging

logging.basicConfig(
    filename="/tmp/mlx_debug.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)
log = logging.getLogger("mlx_display")
