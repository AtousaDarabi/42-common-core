from typing import List, Tuple


def remove_walls(
    grid: List[List[int]],
    curr: Tuple[int, int],
    nxt: Tuple[int, int],
    bit: int
) -> None:
    """!
    @brief Removes the wall between two adjacent cells.
    @param grid The 2D maze structure representing walls as bits.
    @param curr The coordinates of the current cell.
    @param nxt The coordinates of the target neighbor cell.
    @param bit The directional bit representing the wall to remove.
    @return None.
    @details Clears the matching wall bit on both sides of the edge: `bit`
             on `curr` and its opposite (N<->S, E<->W, i.e. `(bit + 2) % 4`)
             on `nxt`.
    """
    opp_bit = (bit + 2) % 4

    grid[curr[1]][curr[0]] &= ~(1 << bit)
    grid[nxt[1]][nxt[0]] &= ~(1 << opp_bit)


def get_init_value() -> int:
    """!
    @brief Provides the initial state for a cell with all walls present.
    @return An integer representing all four walls closed (0xF/15).
    @details This value acts as the default state for unvisited cells.
    @note The value 15 corresponds to binary 1111 (N, E, S, W).
    @warning Ensure grid initialization uses this value for boundaries.
    """
    return 15
