"""ctypes callback signatures and small constants for the MLX bindings.

`_EVENT_HOOK_FUNC` is the generic hook signature used for window-manager
events like the X ("close window") button -- these carry no int/int
params, just the opaque param pointer passed to `mlx_hook()`.
`CLIENT_MESSAGE_EVENT` is the X11 event mask constant for "window manager
sent a ClientMessage" (i.e. the user clicked the window's own close
button), which is what `mlx_hook()` expects as its event-number argument
to catch that.
"""

import ctypes
import os

_KEY_HOOK_FUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_void_p)
_LOOP_HOOK_FUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
_EVENT_HOOK_FUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)

CLIENT_MESSAGE_EVENT = 17

_DEFAULT_LIB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "mlx",
    "libmlx.so",
)


class MLXUnavailableError(RuntimeError):
    """!
    @brief Raised whenever MiniLibX can't be used (not built, or no X display).
    """
