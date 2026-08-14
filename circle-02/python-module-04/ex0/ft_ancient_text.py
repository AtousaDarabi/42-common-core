import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    for filename in sys.argv[1:]:
        print("=== Cyber Archives Recovery ===")
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


if __name__ == "__main__":
    main()

# file = open("example.txt", "r")
# print(type(file))  # output: <class '_io.TextIOWrapper'>
# file.close()

# open("cyber_data.bin", "rb") # output: <class '_io.BufferedReader'>
# open("cyber_data.bin", "wb") # output: <class '_io.BufferedWriter'>
