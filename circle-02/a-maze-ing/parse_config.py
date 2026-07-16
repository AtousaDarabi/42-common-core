import sys


def parse_config(filename):
    config = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    print(f"Error: Invalid syntax in config line: {line}",
                          file=sys.stderr)
                    sys.exit(1)
                key, val = line.split('=', 1)
                config[key.strip()] = val.strip()
    except FileNotFoundError:
        print(f"Error: Configuration file '{filename}' not found.",
              file=sys.stderr)
        sys.exit(1)

    required = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for req in required:
        if req not in config:
            print(f"Error: Missing required configuration key: {req}",
                  file=sys.stderr)
            sys.exit(1)

    try:
        width = int(config['WIDTH'])
        height = int(config['HEIGHT'])
        entry_x, entry_y = map(int, config['ENTRY'].split(','))
        exit_x, exit_y = map(int, config['EXIT'].split(','))
        perfect = config['PERFECT'].lower() == 'true'
        output_file = config['OUTPUT_FILE']
    except ValueError:
        print("Error: Invalid numeric value formats in configuration file.",
              file=sys.stderr)
        sys.exit(1)

    if width <= 0 or height <= 0:
        print("Error: Width and Height must be positive integers.",
              file=sys.stderr)
        sys.exit(1)

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        print("Error: Entry coordinates out of bounds.", file=sys.stderr)
        sys.exit(1)

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        print("Error: Exit coordinates out of bounds.", file=sys.stderr)
        sys.exit(1)

    if (entry_x, entry_y) == (exit_x, exit_y):
        print("Error: Entry and Exit coordinates must be different.",
              file=sys.stderr)
        sys.exit(1)

    return (width, height, (entry_x, entry_y), (exit_x, exit_y), output_file,
            perfect)
