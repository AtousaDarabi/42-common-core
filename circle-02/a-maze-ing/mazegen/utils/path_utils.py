from typing import List, Tuple


def get_direction_letter(start: Tuple[int, int], end: Tuple[int, int]) -> str:
    """!
    @brief Determines the cardinal direction (N, E, S, W) between two
           adjacent cells.
    @param start The coordinates of the starting cell (x, y).
    @param end The coordinates of the target cell (x, y).
    @return A string character representing the direction ('N', 'E', 'S', or
            'W'), or "" if `start`/`end` are not exactly one adjacent
            step apart.
    @details Maps the (dx, dy) coordinate difference to a single
             compass letter.
    """
    dx = end[0] - start[0]
    dy = end[1] - start[1]

    mapping = {(0, -1): "N", (1, 0): "E", (0, 1): "S", (-1, 0): "W"}
    return mapping.get((dx, dy), "")


def format_path(path_coords: List[Tuple[int, int]]) -> str:
    """!
    @brief Converts a sequence of coordinates into a path string.
    @param path_coords A list of (x, y) tuples representing the path.
    @return A concatenated string of direction characters.
    @details Iterates through consecutive points to determine
             movement and joins them.
    """
    if not path_coords:
        return ""

    letters = []
    for i in range(len(path_coords) - 1):
        letter = get_direction_letter(path_coords[i], path_coords[i + 1])
        letters.append(letter)
    return "".join(letters)
