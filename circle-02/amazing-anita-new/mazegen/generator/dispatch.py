"""Resolves and runs the spanning-tree algorithm for `generate()`."""

from typing import Callable, Optional, Tuple

from .state import GeneratorAttrs


class AlgorithmDispatchMixin(GeneratorAttrs):
    """!
    @brief Provides algorithm resolution/dispatch, used by `MazeGenerator.generate()`.
    """

    ALGORITHMS = ["DFS", "KRUSKAL", "PRIM"]

    def _resolve_algorithm(self) -> str:
        """!
        @brief Resolves "RANDOM" (or any unrecognised value) to one concrete
               algorithm, once, so the rest of generation is deterministic.
        @return One of `self.ALGORITHMS`.
        """
        active_algo = self.algorithm_flag
        if active_algo == "RANDOM" or active_algo not in self.ALGORITHMS:
            active_algo = self._rng.choice(self.ALGORITHMS)
        return active_algo

    def _run_spanning_tree(
        self,
        active_algo: str,
        entry: Tuple[int, int],
        blocked_count: int,
        on_step: Optional[Callable[[], None]],
    ) -> None:
        """!
        @brief Carves the spanning tree using the resolved algorithm.
        @param active_algo One of `self.ALGORITHMS` (already resolved).
        @param entry Starting coordinates for DFS/Prim.
        @param blocked_count Number of '42' pattern cells, for the
               algorithms' own spanning-tree edge-count sanity check.
        @param on_step Optional per-wall animation callback, forwarded to
               the chosen algorithm module.
        @details Algorithm modules are imported lazily (inside each branch)
                 to keep import cost minimal and avoid circular imports at
                 module load time.
        """
        if active_algo == "DFS":
            from ..algorithms.dfs import run_dfs

            run_dfs(self.grid, self.visited, entry, blocked_count, on_step)
        elif active_algo == "KRUSKAL":
            from ..algorithms.kruskal import run_kruskal

            run_kruskal(self.grid, self.w, self.h, self._blocked_cells, on_step)
        elif active_algo == "PRIM":
            from ..algorithms.prim import run_prim

            run_prim(self.grid, self.visited, entry, blocked_count, on_step)
