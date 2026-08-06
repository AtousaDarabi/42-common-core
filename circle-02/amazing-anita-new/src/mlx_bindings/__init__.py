"""Minimal ctypes bindings over the compiled MiniLibX shared library.

MiniLibX (see `mlx/`) is a vendored C library; it is never distributed via
pip, so there is no venv/pip dependency to install here. `make mlx` (see the
root Makefile) compiles the vendored C sources into `mlx/libmlx.so`, which
this package loads with ctypes at runtime.

This wraps only the handful of C functions the graphical maze display
(`src/mlx_display/`) actually needs; see `mlx/mlx.h` for the full API if
more is needed later.

Split across this package: `constants.py` (callback signatures, event
numbers, `MLXUnavailableError`), `signatures.py` (ctypes restype/argtypes
declarations), `hooks.py` (event-hook registration mixin), `core.py` (the
`MLX` class itself, the public entry point).
"""

from .constants import CLIENT_MESSAGE_EVENT, MLXUnavailableError
from .core import MLX

__all__ = ["MLX", "MLXUnavailableError", "CLIENT_MESSAGE_EVENT"]
