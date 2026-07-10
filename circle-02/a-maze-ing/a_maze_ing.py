import sys
import random
from collections import deque

def parse_config(filename):
    """Parses the configuration file and returns a validated dictionary."""
    config = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    print(f"Error: Invalid syntax in config line: {line}", file=sys.stderr)
                    sys.exit(1)
                key, val = line.split('=', 1)
                config[key.strip()] = val.strip()
    except FileNotFoundError:
        print(f"Error: Configuration file '{filename}' not found.", file=sys.stderr)
        sys.exit(1)

    # Validate required keys
    required = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for req in required:
        if req not in config:
            print(f"Error: Missing required configuration key: {req}", file=sys.stderr)
            sys.exit(1)

    try:
        width = int(config['WIDTH'])
        height = int(config['HEIGHT'])
        entry_x, entry_y = map(int, config['ENTRY'].split(','))
        exit_x, exit_y = map(int, config['EXIT'].split(','))
        perfect = config['PERFECT'].lower() == 'true'
        output_file = config['OUTPUT_FILE']
    except ValueError:
        print("Error: Invalid numeric value formats in configuration file.", file=sys.stderr)
        sys.exit(1)

    if width <= 0 or height <= 0:
        print("Error: Width and Height must be positive integers.", file=sys.stderr)
        sys.exit(1)
        
    if not (0 <= entry_x < width and 0 <= entry_y < height):
        print("Error: Entry coordinates out of bounds.", file=sys.stderr)
        sys.exit(1)
        
    if not (0 <= exit_x < width and 0 <= exit_y < height):
        print("Error: Exit coordinates out of bounds.", file=sys.stderr)
        sys.exit(1)
        
    if (entry_x, entry_y) == (exit_x, exit_y):
        print("Error: Entry and Exit coordinates must be different.", file=sys.stderr)
        sys.exit(1)

    return width, height, (entry_x, entry_y), (exit_x, exit_y), output_file, perfect

def carve_42_pattern(grid, width, height):
    """
    Carves a '42' pattern using fully closed cells (value 15 / 0xF).
    Returns a set of coordinates that belong to the '42' pattern.
    """
    # 42 pattern definition in a local bounding box grid
    # 1 = Wall cell, 0 = Empty space
    pattern = [
        [1,0,1,0,1,1,1],
        [1,0,1,0,0,0,1],
        [1,1,1,0,1,1,1],
        [0,0,1,0,1,0,0],
        [0,0,1,0,1,1,1]
    ]
    p_h = len(pattern)
    p_w = len(pattern[0])
    
    if width < p_w + 2 or height < p_h + 2:
        print("Warning: Maze size too small to display the '42' pattern securely.", file=sys.stderr)
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
    """Generates the maze grid layout while protecting coherence."""
    # Start with all walls closed: 15 (binary 1111)
    grid = [[15 for _ in range(width)] for _ in range(height)]
    
    # Insert 42 shape
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

    # Randomized DFS starting from Entry
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
                    if 0 <= nx < width and 0 <= ny < height and (nx, ny) in visited:
                        grid[y][x] &= ~(1 << d)
                        grid[ny][nx] &= ~(1 << opposite[d])
                        visited.add((x, y))
                        break

    return grid

def solve_maze(grid, width, height, entry, exit_cell):
    """Finds the shortest path from entry to exit using BFS."""
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    dir_chars = ['N', 'E', 'S', 'W']
    
    queue = deque([ (entry[0], entry[1], "") ])
    visited = set([entry])
    
    while queue:
        cx, cy, path = queue.popleft()
        
        if (cx, cy) == exit_cell:
            return path
            
        for d in range(4):
            # Check if wall is open in direction d
            if not (grid[cy][cx] & (1 << d)):
                nx, ny = cx + dx[d], cy + dy[d]
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + dir_chars[d]))
                    
    return "" # No path found (isolated by 42 pattern or error)

def save_maze_to_file(grid, width, height, entry, exit_cell, path, output_file):
    """Saves the output cleanly formatted to match project specifications."""
    try:
        with open(output_file, 'w') as f:
            # Write hexadecimal matrix
            for y in range(height):
                row_hex = "".join(f"{grid[y][x]:X}" for x in range(width))
                f.write(row_hex + "\n")
                
            f.write("\n") # Blank line separating grid from metadata
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_cell[0]},{exit_cell[1]}\n")
            f.write(f"{path}\n")
    except IOError as e:
        print(f"Error: Unable to save to file '{output_file}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)
        
    config_file = sys.argv[1]
    
    # 1. Parse and validate parameters
    width, height, entry, exit_cell, output_file, perfect = parse_config(config_file)
    
    # Optional Seed handling can go here if provided in config
    # random.seed(42) 

    # 2. Build the maze structural architecture
    grid = generate_maze(width, height, entry, exit_cell, perfect)
    
    # 3. Solve the path mapping
    path = solve_maze(grid, width, height, entry, exit_cell)
    
    # 4. Export structure matrix records
    save_maze_to_file(grid, width, height, entry, exit_cell, path, output_file)

if __name__ == "__main__":
    main()
    