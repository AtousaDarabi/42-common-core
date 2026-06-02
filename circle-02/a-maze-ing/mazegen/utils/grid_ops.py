from typing import List, Tuple


def is_in_bounds(x: int, y: int, width: int, height: int) -> bool:
    """!
    @brief Checks if the given coordinates are within the maze boundaries.
    @param x The x-coordinate of the cell.
    @param y The y-coordinate of the cell.
    @param width The total width of the maze.
    @param height The total height of the maze.
    @return True if the coordinates are within bounds, False otherwise.
    """
    return 0 <= x < width and 0 <= y < height


def get_unvisited_neighbors(
    x: int, y: int, width: int, height: int, visited: List[List[bool]]
) -> List[Tuple[int, int, int]]:
    """!
    @brief Identifies adjacent cells that have not yet been visited.
    @param x The current cell's x-coordinate.
    @param y The current cell's y-coordinate.
    @param width The total width of the maze.
    @param height The total height of the maze.
    @param visited A 2D list tracking visited status of cells.
    @return A list of tuples containing (nx, ny, bit), where (nx, ny)
            are neighbor coordinates and 'bit' is the direction index.
    @details Checks the four cardinal directions (0=North, 1=East, 2=South,
             3=West as (dx, dy, bit)), offering only neighbours that are on
             the grid and not yet carved into -- visited cells are already
             part of the tree or blocked by the '42' pattern.
    """
    neighbors = []
    directions = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]

    for dx, dy, bit in directions:
        nx, ny = x + dx, y + dy
        if is_in_bounds(nx, ny, width, height) and not visited[ny][nx]:
            neighbors.append((nx, ny, bit))

    return neighbors
