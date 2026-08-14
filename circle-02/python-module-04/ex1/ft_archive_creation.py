import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    content = ""

    for filename in sys.argv[1:]:
        print("=== Cyber Archives Recovery & Preservation ===")
        print(f"Accessing file '{filename}'")

        try:
            file = open(filename, "r")
            content = file.read()
            file.close()

            print("---\n")
            print(content, end="")
            if not content.endswith("\n") and content:
                print()
            print("\n---")
            print(f"File '{filename}' closed.")

        except Exception as e:
            print(f"Error opening file '{filename}': {e}")

    lines = content.splitlines()
    transformed_lines = [f"{line}#" for line in lines]
    transformed_content = "\n".join(transformed_lines) + "\n"

    print("\nTransform data:")
    print("\n---")
    print(transformed_content, end="")
    print("---\n")

    try:
        new_filename = input("Enter new file name (or empty): ")
    except EOFError:
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
            print(f"Error saving file '{new_filename}': {e}")


if __name__ == "__main__":
    main()
