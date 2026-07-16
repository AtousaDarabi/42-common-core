import sys
from parse_config import parse_config
from maze_generator import generate_maze
from maze_solver import solve_maze
from maze_file_saver import save_maze_to_file


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)
    config_file = sys.argv[1]
    config_data = parse_config(config_file)
    width, height, entry, exit_cell, output_file, perfect = config_data
    grid = generate_maze(width, height, entry, exit_cell, perfect)
    path = solve_maze(grid, width, height, entry, exit_cell)
    save_maze_to_file(grid, width, height, entry, exit_cell, path, output_file)


if __name__ == "__main__":
    main()
