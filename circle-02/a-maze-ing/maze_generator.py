import sys
import random


def carve_42_pattern(grid, width, height):
    # 1 = Wall cell, 0 = Empty space
    pattern = [
        [1, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]
    ]
    p_h = len(pattern)
    p_w = len(pattern[0])

    if width < p_w + 2 or height < p_h + 2:
        print("Warning: Maze size too small to display the '42' pattern "
              "securely.", file=sys.stderr)
        return set()

    # Center the pattern in the maze
    start_x = (width - p_w) // 2
    start_y = (height - p_h) // 2

    pattern_cells = set()
    for y in range(p_h):
        for x in range(p_w):
            if pattern[y][x] == 1:
                mx = start_x + x
                my = start_y + y
                grid[my][mx] = 15  # 15 in binary is 1111 (all walls closed)
                pattern_cells.add((mx, my))

    return pattern_cells


def generate_maze(width, height, entry, exit_cell, perfect):
    grid = [[15 for _ in range(width)] for _ in range(height)]
    pattern_cells = carve_42_pattern(grid, width, height)

    # Directions and bit flags
    # 0: North (-y), 1: East (+x), 2: South (+y), 3: West (-x)
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    opposite = {0: 2, 1: 3, 2: 0, 3: 1}
    visited = set(pattern_cells)

    def get_unvisited_neighbors(cx, cy):
        neighbors = []
        for d in range(4):
            nx, ny = cx + dx[d], cy + dy[d]
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    neighbors.append((nx, ny, d))
        return neighbors
    stack = [entry]
    visited.add(entry)
    while stack:
        cx, cy = stack[-1]
        neighbors = get_unvisited_neighbors(cx, cy)
        if neighbors:
            nx, ny, direction = random.choice(neighbors)
            # Carve wall between current and neighbor
            grid[cy][cx] &= ~(1 << direction)
            grid[ny][nx] &= ~(1 << opposite[direction])
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()
    # For all leftover unreachable cells outside pattern, connect them randomly
    for y in range(height):
        for x in range(width):
            if (x, y) not in visited:
                # Force connection to an adjacent processed cell if possible
                for d in range(4):
                    nx, ny = x + dx[d], y + dy[d]
                    if (0 <= nx < width and 0 <= ny < height and
                            (nx, ny) in visited):
                        grid[y][x] &= ~(1 << d)
                        grid[ny][nx] &= ~(1 << opposite[d])
                        visited.add((x, y))
                        break
    return grid
