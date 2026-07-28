def get_expected_edges(width: int, height: int, blocked_count: int = 0) -> int:
    """!
    @brief Calculates the number of edges required to form a Spanning Tree.
    @param width The total width of the maze grid.
    @param height The total height of the maze grid.
    @param blocked_count Number of cells excluded from the maze
           (e.g., '42' pattern).
    @return The required number of edges (V - 1), clamped to 0 so a
            degenerate 0-vertex maze doesn't go negative.
    @details In a graph, a Spanning Tree must have exactly V-1 edges to be
             connected without cycles.
    """
    total_vertices = (width * height) - blocked_count
    return max(0, total_vertices - 1)


def verify_spanning_tree(current_edges: int, expected_edges: int) -> bool:
    """!
    @brief Validates if the generated maze matches the Spanning Tree property.
    @param current_edges The actual count of edges created in the maze.
    @param expected_edges The theoretical number of edges (V - 1).
    @return True if the counts match, indicating a valid Spanning Tree.
    @details Compares the current edge count against the theoretical
             requirement to ensure the maze is perfectly connected
             and contains no cycles.
    """
    return current_edges == expected_edges
