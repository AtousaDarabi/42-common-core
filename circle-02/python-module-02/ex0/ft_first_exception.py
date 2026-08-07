def input_temperature(temp_str: str) -> int:
    try:
        temp = int(temp_str)
        return temp
    except (ValueError, TypeError) as e:
        raise Exception(f"Caught input_temperature error: {e}\n")


def test_temperature() -> None:
    print("=== Garden Temperature ===\n")
    tests = ["25", "abc"]

    for test in tests:
        print(f"Input data is '{test}'")
        try:
            temp = input_temperature(test)
            print(f"Temperature is now {temp}°C\n")
        except Exception as e:
            print(e)

    print("All tests completed - program didn't crash!")


def main() -> None:
    test_temperature()


if __name__ == "__main__":
    main()
