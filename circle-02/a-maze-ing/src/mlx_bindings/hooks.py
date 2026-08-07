"""Event-hook registration methods, mixed into the MLX class."""

import ctypes
from typing import Callable, List

from .constants import _EVENT_HOOK_FUNC, _KEY_HOOK_FUNC, _LOOP_HOOK_FUNC


class HooksMixin:
    """!
    @brief Provides key/loop/generic event-hook registration for `MLX`.
    @details Expects the including class to set `self._lib` (the loaded
             `ctypes.CDLL`), `self.ptr` (the MLX display pointer), and
             `self._callbacks` (a list kept around so ctypes closures aren't
             garbage-collected while C still holds a pointer to them).
    """

    _lib: ctypes.CDLL
    ptr: object
    _callbacks: List[object]

    def key_hook(self, win: int, callback: Callable[[int], None]) -> None:
        """!
        @brief Registers `callback(keysym)` to run on every key release.
        @details The C side calls back into a plain function pointer, so
                 the Python callback is wrapped in a matching-signature
                 trampoline (C expects an int return) that adapts it to the
                 simpler `callback(keysym)` API.
        """

        def _trampoline(keysym: int, _param: int) -> int:
            callback(keysym)
            return 0

        wrapped = _KEY_HOOK_FUNC(_trampoline)
        self._callbacks.append(wrapped)
        self._lib.mlx_key_hook(win, wrapped, None)

    def loop_hook(self, callback: Callable[[], None]) -> None:
        """!
        @brief Registers `callback()` to run once per idle loop iteration.
        """

        def _trampoline(_param: int) -> int:
            callback()
            return 0

        wrapped = _LOOP_HOOK_FUNC(_trampoline)
        self._callbacks.append(wrapped)
        self._lib.mlx_loop_hook(self.ptr, wrapped, None)

    def hook(
        self, win: int, event: int, mask: int, callback: Callable[[], None]
    ) -> None:
        """!
        @brief Registers `callback()` on a raw MLX/X11 event number.
        @param win The window handle.
        @param event The X11 event number (e.g. CLIENT_MESSAGE_EVENT for
               the window manager's close/X button).
        @param mask The X11 event mask (0 is fine for ClientMessage).
        @param callback Zero-argument function to run when the event fires.
        @details This is what makes the window's own close button work --
                 mlx_key_hook only ever sees keyboard input, never the
                 window manager's "close" click, so without this the
                 window can only be closed via a key (e.g. q/Escape).
        """

        def _trampoline(_param: int) -> int:
            callback()
            return 0

        wrapped = _EVENT_HOOK_FUNC(_trampoline)
        self._callbacks.append(wrapped)
        self._lib.mlx_hook(win, event, mask, wrapped, None)
