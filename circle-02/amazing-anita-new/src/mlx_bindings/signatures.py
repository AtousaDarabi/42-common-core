"""Declares the ctypes restype/argtypes for every MLX C function used here."""

import ctypes

from .constants import _EVENT_HOOK_FUNC, _KEY_HOOK_FUNC, _LOOP_HOOK_FUNC


def configure_signatures(lib: ctypes.CDLL) -> None:
    """!
    @brief Declares restype/argtypes on every MLX C function this module
           calls, before any of them are actually called.
    @details ctypes defaults to c_int for both restype and every argument,
             which corrupts 64-bit pointers -- every C function used here
             must have its real signature declared explicitly first.
             `mlx_hook()` is the generic `(win, event_number, event_mask,
             func, param)` hook, used to catch the window manager's "close"
             (X button) event, which `mlx_key_hook()` does not cover.
             `mlx_do_sync()` is what actually forces buffered X11 *output*
             (every `mlx_pixel_put` call issues an XDrawPoint request that
             Xlib normally just queues client-side) to reach the server and
             get displayed -- it wraps XSync(). This is NOT the same as
             `mlx_flush_event()`, which despite the name only drains
             *input* events and has no effect on pending drawing at all.
             Without a real sync, queued draws only become visible once
             some other blocking Xlib call happens to flush them
             incidentally -- fine for a single redraw between key presses,
             but a whole run of animation frames can sit entirely invisible
             in the client-side buffer until the end.
    """
    lib.mlx_new_window.restype = ctypes.c_void_p
    lib.mlx_new_window.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p
    ]
    lib.mlx_pixel_put.restype = ctypes.c_int
    lib.mlx_pixel_put.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int
    ]
    lib.mlx_string_put.restype = ctypes.c_int
    lib.mlx_string_put.argtypes = [
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
        ctypes.c_int, ctypes.c_char_p,
    ]
    lib.mlx_clear_window.restype = ctypes.c_int
    lib.mlx_clear_window.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    lib.mlx_key_hook.restype = ctypes.c_int
    lib.mlx_key_hook.argtypes = [ctypes.c_void_p, _KEY_HOOK_FUNC, ctypes.c_void_p]
    lib.mlx_loop_hook.restype = ctypes.c_int
    lib.mlx_loop_hook.argtypes = [ctypes.c_void_p, _LOOP_HOOK_FUNC, ctypes.c_void_p]
    lib.mlx_hook.restype = ctypes.c_int
    lib.mlx_hook.argtypes = [
        ctypes.c_void_p, ctypes.c_int, ctypes.c_int, _EVENT_HOOK_FUNC, ctypes.c_void_p
    ]
    lib.mlx_loop.restype = ctypes.c_int
    lib.mlx_loop.argtypes = [ctypes.c_void_p]
    lib.mlx_loop_end.restype = ctypes.c_int
    lib.mlx_loop_end.argtypes = [ctypes.c_void_p]
    lib.mlx_destroy_window.restype = ctypes.c_int
    lib.mlx_destroy_window.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    lib.mlx_destroy_display.restype = ctypes.c_int
    lib.mlx_destroy_display.argtypes = [ctypes.c_void_p]
    if hasattr(lib, "mlx_do_sync"):
        lib.mlx_do_sync.restype = ctypes.c_int
        lib.mlx_do_sync.argtypes = [ctypes.c_void_p]
