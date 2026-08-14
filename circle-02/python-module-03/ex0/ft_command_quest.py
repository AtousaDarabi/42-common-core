import sys


def main() -> None:
    print("=== Command Quest ===")

    program_name = sys.argv[0]
    print(f"Program name: {program_name}")

    args = sys.argv[1:]
    total_args = len(sys.argv)

    if not args:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(args)}")
        for index in range(len(args)):
            print(f"Argument {index + 1}: {args[index]}")

    print(f"Total arguments: {total_args}")


if __name__ == "__main__":
    main()

# from pathlib import Path
# ## File name with extension (e.g., script.py)
# file_name = Path(__file__).name
# ## File name without extension (e.g., script)
# file_stem = Path(__file__).stem
# print(file_name)

# import os
# ## Get filename with extension (e.g., script.py)
# file_name = os.path.basename(__file__)
# ## Get filename without extension (e.g., script)
# file_stem = os.path.splitext(file_name)[0]
# print(file_name)
