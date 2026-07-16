from collections import deque


def solve_maze(grid, width, height, entry, exit_cell):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    dir_chars = ['N', 'E', 'S', 'W']
    queue = deque([(entry[0], entry[1], "")])
    visited = set([entry])
    while queue:
        cx, cy, path = queue.popleft()
        if (cx, cy) == exit_cell:
            return path
        for d in range(4):
            if not (grid[cy][cx] & (1 << d)):
                nx, ny = cx + dx[d], cy + dy[d]
                if (0 <= nx < width and 0 <= ny < height and
                        (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + dir_chars[d]))
    return ""
