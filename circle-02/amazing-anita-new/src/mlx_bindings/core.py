"""The `MLX` ctypes wrapper class itself."""

import ctypes
import os
from typing import List, Optional

from .constants import _DEFAULT_LIB_PATH, MLXUnavailableError
from .hooks import HooksMixin
from .signatures import configure_signatures


class MLX(HooksMixin):
    """!
    @brief Thin ctypes wrapper around the MiniLibX C API.
    @details Every method that can fail on the C side raises
             `MLXUnavailableError` instead of letting ctypes call into a NULL
             pointer (which segfaults the whole process without a Python
             traceback) -- this is what lets the caller fall back to the
             ASCII display cleanly instead of crashing.
    """

    def __init__(self, lib_path: Optional[str] = None) -> None:
        """!
        @brief Loads `libmlx.so` and initializes MiniLibX.
        @param lib_path Optional override for the compiled library's path
               (defaults to `mlx/libmlx.so` at the repo root).
        @details `self._callbacks` keeps every registered ctypes closure
                 alive for the lifetime of the instance, since ctypes does
                 not do this on its own -- without it the GC could collect a
                 callback while C still holds a pointer to it, crashing on
                 the next event. `mlx_init()` returns NULL (falsy) instead
                 of raising when there's no usable X display; calling into a
                 NULL pointer would segfault the whole process, so that
                 return value is checked here and turned into
                 `MLXUnavailableError` instead of crashing with no Python
                 traceback.
        """
        path = lib_path or _DEFAULT_LIB_PATH
        if not os.path.exists(path):
            raise MLXUnavailableError(
                f"MiniLibX shared library not found at '{path}'. Run "
                "'make mlx' to compile it (requires gcc, make, and the X11 "
                "development headers: xorg, libxext-dev, libbsd-dev)."
            )
        self._lib = ctypes.CDLL(path)
        configure_signatures(self._lib)
        self._callbacks: List[object] = []

        self._lib.mlx_init.restype = ctypes.c_void_p
        mlx_ptr = self._lib.mlx_init()
        if not mlx_ptr:
            raise MLXUnavailableError(
                "mlx_init() failed -- no usable X11 display found. Set "
                "DISPLAY to a running X server (e.g. via Xquartz/XQuartz on "
                "macOS, or plain X11 on Linux) or use the ASCII display "
                "instead (DISPLAY=ASCII in config.txt)."
            )
        self.ptr = mlx_ptr

    def new_window(self, width: int, height: int, title: str) -> int:
        """!
        @brief Creates a new MLX window and returns its handle.
        """
        win = self._lib.mlx_new_window(self.ptr, width, height, title.encode())
        if not win:
            raise MLXUnavailableError("mlx_new_window() failed.")
        return int(win)

    def pixel_put(self, win: int, x: int, y: int, color: int) -> None:
        """!
        @brief Sets a single pixel's colour in the given window.
        """
        self._lib.mlx_pixel_put(self.ptr, win, x, y, color)

    def string_put(self, win: int, x: int, y: int, color: int, text: str) -> None:
        """!
        @brief Draws `text` at (x, y) in the given window.
        """
        self._lib.mlx_string_put(self.ptr, win, x, y, color, text.encode())

    def clear_window(self, win: int) -> None:
        """!
        @brief Clears the given window to black.
        """
        self._lib.mlx_clear_window(self.ptr, win)

    def flush(self) -> None:
        """!
        @brief Forces any pending drawing to actually reach the screen (XSync).
        """
        if hasattr(self._lib, "mlx_do_sync"):
            self._lib.mlx_do_sync(self.ptr)

    def loop(self) -> None:
        """!
        @brief Runs the MLX event loop until `loop_end()` is called.
        """
        self._lib.mlx_loop(self.ptr)

    def loop_end(self) -> None:
        """!
        @brief Requests the running event loop (`loop()`) to stop.
        """
        self._lib.mlx_loop_end(self.ptr)

    def destroy_window(self, win: int) -> None:
        """!
        @brief Destroys the given window.
        """
        self._lib.mlx_destroy_window(self.ptr, win)

    def destroy_display(self) -> None:
        """!
        @brief Releases the underlying X11 display connection.
        """
        self._lib.mlx_destroy_display(self.ptr)
