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
