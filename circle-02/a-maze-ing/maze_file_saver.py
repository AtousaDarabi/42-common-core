import sys


def save_maze_to_file(grid, width, height, entry, exit_cell, path,
                      output_file):
    try:
        with open(output_file, 'w') as f:
            for y in range(height):
                row_hex = "".join(f"{grid[y][x]:X}" for x in range(width))
                f.write(row_hex + "\n")
            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_cell[0]},{exit_cell[1]}\n")
            f.write(f"{path}\n")
    except IOError as e:
        print(f"Error: Unable to save to file '{output_file}': {e}",
              file=sys.stderr)
        sys.exit(1)
