"""'42' pattern placement, split out of `MazeGenerator.generate()`."""

from typing import Tuple

from ..utils.validation import pattern_leaves_maze_connected
from .state import GeneratorAttrs


class PatternMixin(GeneratorAttrs):
    """!
    @brief Provides `_apply_42_pattern()`, used by `MazeGenerator.generate()`.
    """

    def _apply_42_pattern(
        self, entry: Tuple[int, int], exit_cell: Tuple[int, int]
    ) -> int:
        """!
        @brief Marks cells associated with the '42' pattern as
               visited to block them.
        @param entry Entry coordinates, kept free even if the pattern would
               otherwise cover them.
        @param exit_cell Exit coordinates, kept free even if the pattern would
               otherwise cover them.
        @return The count of blocked cells (0 if the pattern was omitted).
        @details Bails out early (a cheap size-only check) if the maze is
                 too small to fit the pattern's 7x5 bounding box, which is
                 otherwise centred in the grid. Entry/exit are always
                 excluded: DFS/Prim start carving from `entry`, so blocking
                 it would tear a hole in the supposedly-sealed pattern and
                 desync the expected edge count, crashing the spanning-tree
                 check in `generate()`. The pattern is only applied if it
                 leaves every remaining cell reachable from every other
                 remaining cell; a pattern placed too close to the grid
                 border can otherwise strand cells with no legal
                 (non-blocked) neighbour, making a spanning tree impossible.
                 In that case the pattern is omitted and a warning is
                 printed, per the subject. When applied, pattern cells are
                 marked as already "visited" so DFS/Prim skip carving into
                 them; Kruskal instead excludes them via `_blocked_cells`.
        """
        from ..utils.patterns import can_fit_pattern, get_42_offsets

        if not can_fit_pattern(self.w, self.h):
            print(
                f"Warning: maze size {self.w}x{self.h} is too small "
                "to display the '42' pattern; it will be omitted."
            )
            return 0

        start_x = (self.w - 7) // 2
        start_y = (self.h - 5) // 2
        reserved = {entry, exit_cell}

        candidate_blocked = set()
        for dx, dy in get_42_offsets():
            nx, ny = start_x + dx, start_y + dy
            if (
                0 <= nx < self.w
                and 0 <= ny < self.h
                and (nx, ny) not in reserved
            ):
                candidate_blocked.add((nx, ny))

        if not pattern_leaves_maze_connected(
            self.w, self.h, candidate_blocked
        ):
            print(
                f"Warning: the '42' pattern cannot be placed in a "
                f"{self.w}x{self.h} maze without isolating cells; it will "
                "be omitted."
            )
            return 0

        for nx, ny in candidate_blocked:
            self.visited[ny][nx] = True
        self._blocked_cells = candidate_blocked
        return len(candidate_blocked)
