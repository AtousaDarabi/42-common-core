from typing import List, Tuple


def get_42_offsets() -> List[Tuple[int, int]]:
    """!
    @brief Returns the relative coordinates for the '42' pattern shape.
    @return A list of (dx, dy) tuples representing the cells of the pattern.
    @details Offsets are relative to the pattern's top-left corner: columns
             0-2 form the digit '4', column 3 is left blank as a one-cell
             gap, and columns 4-6 form the digit '2'.
    """
    four = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (2, 4)]
    two = [(4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2), (4, 2), (4, 3),
           (4, 4), (5, 4), (6, 4)]
    return four + two


def can_fit_pattern(w: int, h: int) -> bool:
    """!
    @brief Validates if the maze dimensions can accommodate the '42' pattern.
    @param w Maze width.
    @param h Maze height.
    @return True if the maze is at least 7x5, False otherwise.
    @details The pattern requires a minimum bounding box of 7x5 to be placed.
    """
    return w >= 7 and h >= 5
