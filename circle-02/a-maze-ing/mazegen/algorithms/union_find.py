"""Disjoint Set Union (DSU), used by Kruskal's algorithm to avoid cycles."""


class UnionFind:
    """!
    @brief A Disjoint Set Union (DSU) data structure.
    @details Used to keep track of connected components to prevent cycles during
             maze generation.
    """

    def __init__(self, n: int) -> None:
        """!
        @brief Initializes n singleton sets, one per index from 0 to n-1.
        """
        self.parent = list(range(n))

    def find(self, i: int) -> int:
        """!
        @brief Finds the representative of the set containing i with path compression.
        @details Path compression points i directly at the root so future
                 find() calls on i (and anything under it) are close to O(1).
        """
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """!
        @brief Unions the sets containing i and j.
        @return True if they were in different sets and are now merged, False otherwise.
        """
        root_i, root_j = self.find(i), self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False
