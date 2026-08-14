def secure_archive(
    filename: str, mode: str = "read", content: str = ""
) -> tuple[bool, str]:
    try:
        if mode == "read":
            with open(filename, "r") as file:
                data = file.read()
                return (True, data)
        elif mode == "write":
            with open(filename, "w") as file:
                file.write(content)
                return (True, "Content successfully written to file")
        else:
            return (False, f"Invalid mode '{mode}'")
    except Exception as e:
        return (False, str(e))


def main() -> None:
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to read from a nonexistent file:")
    res1 = secure_archive("/not/existing/file", "read")
    print(res1)
    print("\n")

    print("Using 'secure_archive' to read from an inaccessible file:")
    res2 = secure_archive("/etc/master.passwd", "read")
    print(res2)
    print("\n")

    print("Using 'secure_archive' to read from a regular file:")
    res3 = secure_archive("ancient_fragment.txt", "read")
    print(res3)

    if res3[0]:
        print("Using 'secure_archive' to write previous content to a new "
              "file:")
        res4 = secure_archive("new_fragment.txt", "write", res3[1])
        print(res4)


if __name__ == "__main__":
    main()
