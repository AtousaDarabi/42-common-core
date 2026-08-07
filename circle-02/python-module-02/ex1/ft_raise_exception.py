def input_temperature(temp_str: str) -> int:
    try:
        temp = int(temp_str)
        if temp > 40:
            raise Exception(
                f"Caught input_temperature error: {temp_str}°C is too hot for"
                " plants (max 40°C)\n"
            )
        elif temp < 0:
            raise Exception(
                f"Caught input_temperature error: {temp_str}°C is too cold"
                " for plants (min 0°C)\n"
            )
        return temp
    except (ValueError, TypeError) as e:
        raise Exception(f"Caught input_temperature error: {e}\n")


def test_temperature() -> None:
    print("=== Garden Temperature Checker ===\n")
    tests = ["25", "abc", "100", "-50"]

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
