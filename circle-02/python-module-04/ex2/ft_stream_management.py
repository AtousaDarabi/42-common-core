import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: ft_stream_management.py <filename>")
        return

    filename = sys.argv[1]

    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    try:
        file = open(filename, "r")
        content = file.read()
        file.close()

        print("---\n")
        print(content, end="")
        if not content.endswith("\n"):
            print()
        print("\n---")
        print(f"File '{filename}' closed.\n")

    except Exception as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")
        return

    lines = content.splitlines()
    transformed_lines = [f"{line}#" for line in lines]
    transformed_content = "\n".join(transformed_lines) + "\n"

    print("Transform data:")
    print("---\n")
    print(transformed_content, end="")
    print("\n---")

    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()

    try:
        input_line = sys.stdin.readline()
        if input_line:
            new_filename = input_line.rstrip("\r\n")
        else:
            new_filename = ""
    except Exception:
        new_filename = ""

    if not new_filename:
        print("Not saving data.")
    else:
        print(f"Saving data to '{new_filename}'")
        try:
            save_file = open(new_filename, "w")
            save_file.write(transformed_content)
            save_file.close()
            print(f"Data saved in file '{new_filename}'.")
        except Exception as e:
            sys.stderr.write(f"[STDERR] Error opening file '{new_filename}': "
                             f"{e}\n")
            print("Data not saved")


if __name__ == "__main__":
    main()
