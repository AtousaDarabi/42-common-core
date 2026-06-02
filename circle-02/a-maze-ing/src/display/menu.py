"""Interactive command menu shared by the ASCII and MLX displays."""


def print_menu() -> None:
    """!
    @brief Prints the available interactive commands.
    """
    print(
        "\n=== A-Maze-ing ===\n"
        "[r] regenerate   [p] toggle path   [c] cycle wall colour   [q] quit\n"
    )
